from pathlib import Path
from typing import Dict, List

import astropy.units as u
import pandas as pd
from astropy.table import Table
from astroquery.ipac.irsa.irsa_dust import IrsaDust
from astroquery.simbad import Simbad
from astroquery.vizier import Vizier

from ..config.options import OPTIONS
from .utils import add_space, remove_parenthesis

TARGET_INFO_FILE = list((Path(__file__).parent.parent / "config").glob("*.xlsx"))[0]
TARGET_INFO_MAPPING = {
    "local.RA": "RA [hms]",
    "local.DEC": "DEC [dms]",
    "local.propRa": "PMA [arcsec/yr]",
    "local.propDec": "PMD [arcsec/yr]",
    "Lflux": "Flux L-band [Jy]",
    "Nflux": "Flux N-band [Jy]",
    "Hmag": "H mag",
    "Kmag": "K mag",
    "GSname": "GS Name",
    "GSdist": 'GS Distance (")',
    "GSRa": "GS RA [hms]",
    "GSDec": "GS DEC [dms]",
    "GSpropRa": "GS Off-axis Coude PMA [arcsec/yr]",
    "GSpropDec": "GS Off-axis Coude PMD [arcsec/yr]",
    "GSepoch": "GS Epoch",
    "GSequinox": "GS Equinox",
    "GSmag": "GS mag",
    "LResAT": "L-Resolution (AT)",
    "LResUT": "L-Resolution (UT)",
}


def query_dust_extinction(name: str) -> Dict:
    """Queries the dust extinctions for the specified target.

    Parameters
    ----------
    name : str
        The target's name.

    Returns
    -------
    target : dict
        The target's queried information.
    """
    extinctions = {}
    table = IrsaDust.get_extinction_table(name)
    for band in OPTIONS.catalogs.irsa.query:
        extinction = table[OPTIONS.catalogs.irsa.fields][table["Filter_name"] == band]
        extinctions[f"A_{band[-1]}"] = extinction[0][0]
    return extinctions


# TODO: Implement match statement here
def query_local_catalog(name: str):
    """

    Parameters
    ----------
    name : str
        The target's name.

    Returns
    -------
    target : Dict
    """
    if OPTIONS.catalogs.local.active == "standard":
        sheet_name = OPTIONS.catalogs.local.standard
    elif OPTIONS.catalogs.local.active == "ciao":
        sheet_name = OPTIONS.catalogs.local.ciao

    catalog = pd.read_excel(TARGET_INFO_FILE, sheet_name=sheet_name)
    catalog = Table.from_pandas(catalog)
    if not any(
        name in catalog[column_name] for column_name in ["Target Name", "Other Names"]
    ):
        return {}

    if name in catalog["Target Name"]:
        row = catalog[catalog["Target Name"] == name]
    elif name in catalog["Other Names"]:
        row = catalog[catalog["Other Names"] == name]

    target = {}
    for query_key, query_mapping in TARGET_INFO_MAPPING.items():
        if query_mapping in row.columns:
            target[query_key] = row[query_mapping].data.tolist()[0]
    return {key: value for key, value in target.items() if value is not None}


# TODO: Add query of the magnitude from Simbad?
def get_best_match(target: Dict, catalog: str, catalog_table: Table) -> Table:
    """Gets the best match from the catalog entries

    Parameters
    ----------
    target : dict
        The target's queried information.
    catalog : str
        The catalog's name.
    catalog_table : Table
        The table containing the queried catalog's results.

    Returns
    -------
    best_match : Table
        The best match from the queried catalog's table.
    """
    best_matches = {}
    if not catalog_table:
        return best_matches

    for query_key in getattr(OPTIONS.catalogs, catalog).query:
        if query_key in catalog_table.columns:
            if len(catalog_table) == 1:
                value = catalog_table[query_key][0]
            else:
                # NOTE: Get lowest element in case magnitude is queried
                if "mag" in query_key:
                    value = catalog_table[query_key].min()
                else:
                    value = catalog_table[query_key].max()

            if query_key in target:
                if "mag" in query_key:
                    if target[query_key] > value:
                        best_matches[query_key] = value
                else:
                    if target[query_key] < value:
                        best_matches[query_key] = value
            else:
                best_matches[query_key] = value
    return best_matches


def get_catalog(name: str, catalog: str, match_radius: u.arcsec = 5.0):
    """Queries the specified catalog.

    Parameters
    ----------
    name : str
        The target's name.
    catalog : str
        The catalog's name.
    match_radius : astropy.units.arcsec
        The radius in which is queried.
        Default is 5.

    Returns
    -------
    catalog_table : Table
        The table containing the queried catalog's results.
    """
    if not isinstance(match_radius, u.Quantity):
        match_radius *= u.arcsec
    else:
        if match_radius.unit != u.arcsec:
            raise ValueError(
                "The match radius has to be in" " astropy.units.arcsecond."
            )

    if catalog == "simbad":
        query_site = Simbad()
        simbad_fields = OPTIONS.catalogs.simbad.fields
        query_site.add_votable_fields(*simbad_fields)
        catalog_table = query_site.query_object(name)
    else:
        data = getattr(OPTIONS.catalogs, catalog)
        query_site = Vizier(catalog=data.catalog, columns=data.fields)
        catalog_table = query_site.query_object(name, radius=match_radius)

        # NOTE: Only get table from TableList if not empty
        if catalog_table:
            catalog_table = catalog_table[0]
    return catalog_table


# TODO: Make a pretty print built in functionality for the dictionary.
def query(
    target_name: str,
    catalogs: List | None = None,
    exclude_catalogs: List | None = None,
    match_radius: float | None = 5.0,
    query_exinction: bool | None = False,
) -> Dict:
    """Queries information for an astronomical target by its name from
    various catalogs.

    Parameters
    ----------
    target_name : str
        The target's name.
    catalogs : list of str, optional
        The catalogs to query. By default the catalogs "gaia",
        "tycho", "nomad", "2mass", "wise", "mdfc" and "simbad"
        as well as local catalogs (with "local") are included.
    exclude_catalogs : list of str
        A list of catalog to be excluded. Can be any of the catalogs
        listed as default for the catalogs parameter.
    match_radius : float, optional
        The radius in which the target queried. Default is 5.

    Returns
    -------
    target : dict
        The target's queried information.
    """
    target_name = add_space(target_name)
    target = {"name": target_name}
    if catalogs is None:
        catalogs = OPTIONS.catalogs.available[:]

    if exclude_catalogs is not None:
        catalogs = [catalog for catalog in catalogs if catalog not in exclude_catalogs]
    if "local" in catalogs:
        local_target = query_local_catalog(target_name)
        catalogs.remove("local")
    else:
        local_target = {}

    for catalog in catalogs:
        catalog_table = get_catalog(target_name, catalog, match_radius)
        best_matches = get_best_match(target, catalog, catalog_table)
        target = {**target, **best_matches}

    target["name"] = remove_parenthesis(target["name"])
    dust_target = query_dust_extinction(target["name"]) if query_exinction else {}
    return {**target, **local_target, **dust_target}
