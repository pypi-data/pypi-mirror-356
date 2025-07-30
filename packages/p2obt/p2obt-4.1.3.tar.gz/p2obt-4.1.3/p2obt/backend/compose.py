from pathlib import Path
from typing import Dict, Tuple, Union

import astropy.units as u
import numpy as np
import toml
from astropy.coordinates import SkyCoord

from ..config.options import OPTIONS
from .query import query
from .utils import convert_proper_motions, remove_parenthesis, remove_spaces

TEMPLATE_FILE = Path(__file__).parent.parent / "config" / "templates.toml"
TURBULENCE = {
    10: "10%  (Seeing < 0.6 arcsec, t0 > 5.2 ms)",
    30: "30%  (Seeing < 0.8 arcsec, t0 > 4.1 ms)",
    70: "70%  (Seeing < 1.15 arcsec, t0 > 2.2 ms)",
}
SKY_TRANSPARENCY = {
    "photometric": "Photometric",
    "clear": "Clear",
    "thin": "Variable, thin cirrus",
    "thick": "Variable, thick cirrus",
}


def load_template(
    file: Path,
    header: str,
    sub_header: str | None = None,
    operational_mode: str | None = None,
) -> Dict:
    """Loads a template from a (.toml)-file.

    Parameters
    ----------
    file : path
        A (.toml)-file containing templates.
    header : str
        The name of the specific template.
    sub_header : str, optional
        The name of a sub-template.
    operational_mode : str, optional
        The mode in which MATISSE is operated, either
        "gra4mat" or "matisse".

    Returns
    -------
    template : dict
        A dictionary that is the template.
    """
    with open(file, "r+", encoding="utf-8") as toml_file:
        if operational_mode is not None:
            return toml.load(toml_file)[operational_mode][header]
        return toml.load(toml_file)[header][sub_header]


def write_dict(file, dictionary: Dict):
    """Iterates over the key and value pairs of a
    dictionary and writes them."""
    for key, value in dictionary.items():
        file.write(f'{key.ljust(40)}"{str(value)}"' + "\n")


def write_ob(ob: Dict, ob_name: str, output_dir: Path) -> None:
    """Writes the (.obx)-file to the specified directory"""
    out_file = Path(output_dir) / f"{ob_name}.obx"
    with open(out_file, "w+", encoding="utf-8") as obx_file:
        for dictionary in ob.values():
            if any(isinstance(value, dict) for value in dictionary.values()):
                for sub_dict in dictionary.values():
                    write_dict(obx_file, sub_dict)
                    obx_file.write("\n\n")
            else:
                write_dict(obx_file, dictionary)
                obx_file.write("\n\n")
    print(f"Created OB: '{ob_name}'.")


# TODO: 'add_space' makes to many spaces. Fix at some point.
def set_ob_name(
    target: Dict | str,
    observation_type: str,
    sci_name: str | None = None,
    tag: str | None = None,
) -> str:
    """Sets the OB's name.

    Parameters
    ----------
    target : dict or str
    observation_type : str
    sci_name : str, optional
    tag : str, Optional

    Returns
    -------
    ob_name : str

    Examples
    --------
    """
    ob_name = f"{observation_type.upper()}"
    if isinstance(target, dict):
        target_name = target["name"]
    else:
        target_name = remove_parenthesis(target)

    ob_name += f"_{remove_spaces(target_name).replace(' ', '_')}"
    if sci_name is not None:
        ob_name += f"_{remove_spaces(sci_name).replace(' ', '_')}"
    return ob_name if tag is None else f"{ob_name}_{tag}"


def get_observation_settings(
    resolution: str, operational_mode: str, array_configuration: str
) -> Tuple[str, float]:
    """Gets the observation settings from the `options` corresponding
    to the resolution, operational mode and array configuration.

    Parameters
    ----------
    resolution : str
    operational_mode : str
    array_configuration : str

    Returns
    -------
    resolution : str
    integration_time : float
    central_wl : float
    """
    array = "uts" if "ut" in array_configuration else "ats"
    photometry = getattr(getattr(OPTIONS.photometry, operational_mode), array)
    integration_time = getattr(
        getattr(getattr(OPTIONS.dit, operational_mode), array), resolution
    )
    central_wl = getattr(
        getattr(getattr(OPTIONS.wl0, operational_mode), array), resolution
    )
    return resolution.upper(), integration_time, central_wl, photometry


def format_proper_motions(target: Dict) -> Tuple[float, float]:
    """Correctly formats the right ascension's and declination's
    proper motions."""
    pmra, pmdec = convert_proper_motions(target.get("pmra", 0), target.get("pmdec", 0))
    if "local.propRa" in target:
        pmra = (target.get("local.propRa", 0),)
    if "local.propDEC" in target:
        pmdec = target.get("local.propDec", 0)
    return pmra, pmdec


def format_ra_and_dec(target: Dict) -> Tuple[str, str]:
    """Correctly formats the right ascension and declination."""
    if "local.RA" in target:
        return target["local.RA"], target["local.DEC"]

    coordinates = SkyCoord(f"{target['ra']} {target['dec']}", unit=(u.deg, u.deg))
    ra_hms = coordinates.ra.to_string(unit=u.hourangle, sep=":", pad=True, precision=3)
    dec_dms = coordinates.dec.to_string(sep=":", pad=True, precision=3)
    return ra_hms, dec_dms


def format_fluxes(target: Dict) -> Tuple[float, float]:
    """Correctly gets and formats the fluxes from the queried data."""
    flux_lband, flux_nband = None, None
    lband_keys, nband_keys = ["Lflux", "med-Lflux", "W1mag"], [
        "Nflux",
        "med-Nflux",
        "W3mag",
    ]

    for lband_key, nband_key in zip(lband_keys, nband_keys):
        if lband_key in target and flux_lband is None:
            flux_lband = target[lband_key]
            if "mag" in lband_key:
                flux_lband = 309.54 * 10.0 ** (-flux_lband / 2.5)

        if nband_key in target and flux_nband is None:
            flux_nband = target[nband_key]
            if "mag" in nband_key:
                flux_nband = 31.674 * 10.0 ** (-flux_nband / 2.5)
    return round(flux_lband, 2) if flux_lband is not None else 0.0, (
        round(flux_nband, 2) if flux_nband is not None else 0.0
    )


def fill_header(
    target: Dict,
    observation_type: str,
    array_configuration: str,
    sci_name: str | None = None,
    tag: str | None = None,
) -> Dict:
    """Fill header dictionary with the information from the query.

    Parameters
    ----------
    target : dict
    observation_type : str
    array_configuration : str
    sci_name : str, optional
    tag : str, optional

    Returns
    -------
    header : dict
    """
    header = {}
    header_user = load_template(TEMPLATE_FILE, "header", sub_header="user")
    header_target = load_template(TEMPLATE_FILE, "header", sub_header="target")
    header_constraints = load_template(
        TEMPLATE_FILE, "header", sub_header="constraints"
    )
    header_observation = load_template(
        TEMPLATE_FILE, "header", sub_header="observation"
    )
    ob_name = set_ob_name(target, observation_type, sci_name, tag)
    ra_hms, dec_dms = format_ra_and_dec(target)
    prop_ra, prop_dec = format_proper_motions(target)

    header_user["name"] = ob_name
    user_comments = []
    if "GSname" in target:
        user_comments.append(f"GS: {target['GSname']}")
    if "GSdist" in target:
        gs_distance = float(target["GSdist"])
        user_comments.append(f"GS Distance: {gs_distance:.2f} arcsec")
    header_user["userComments"] = ". ".join(user_comments)
    header_target["TARGET.NAME"] = target["name"].replace(" ", "_")
    header_target["ra"], header_target["dec"] = ra_hms, dec_dms
    header_target["propRA"], header_target["propDec"] = prop_ra, prop_dec
    header_observation["OBSERVATION.DESCRIPTION.NAME"] = ob_name

    header_constraints["atm"] = TURBULENCE[OPTIONS.constraints.turbulence]
    header_constraints["sky_transparency"] = SKY_TRANSPARENCY[
        OPTIONS.constraints.transparency
    ]
    header_constraints["watervapour"] = OPTIONS.constraints.pwv
    if "ut" in array_configuration:
        header_constraints["moon_angular_distance"] = 10

    header["user"] = header_user
    header["target"] = header_target
    header["constraints"] = header_constraints
    header["observation"] = header_observation
    return header


def fill_acquisition(
    target: Dict, operational_mode: str, array_configuration: str
) -> Dict:
    """Gets the for the operational mode correct acquisition template
    and then fills it in with the information from the query.

    Parameters
    ----------
    target : dict
    operational_mode : str
    array_configuration : str

    Returns
    -------
    acquisition : dict
    """
    acquisition = load_template(
        TEMPLATE_FILE, "acquisition", operational_mode=operational_mode
    )

    flux_lband, flux_nband = format_fluxes(target)

    if "GSRa" in target:
        acquisition["COU.AG.ALPHA"] = target["GSRa"]
        acquisition["COU.AG.DELTA"] = target["GSDec"]
        acquisition["COU.AG.GSSOURCE"] = "SETUPFILE"

    if "GSpropRa" in target:
        acquisition["COU.AG.PMA"] = target["GSpropRa"]
    if "GSpropDec" in target:
        acquisition["COU.AG.PMD"] = target["GSpropDec"]

    if "GSepoch" in target:
        acquisition["COU.AG.EPOCH"] = target["GSepoch"]
    if "GSequinox" in target:
        acquisition["COU.AG.EQUINOX"] = target["GSequinox"]

    if "GSmag" in target:
        acquisition["COU.GS.MAG"] = target["GSmag"]
    elif "Vmag" in target:
        acquisition["COU.GS.MAG"] = target["Vmag"]
    elif "FLUX_V" in target:
        acquisition["COU.GS.MAG"] = target["FLUX_V"]

    if "ut" in array_configuration:
        array_configuration = "UTs"

    acquisition["ISS.BASELINE"] = array_configuration

    if flux_lband is not None:
        acquisition["SEQ.TARG.FLUX.L"] = flux_lband
    if flux_nband is not None:
        acquisition["SEQ.TARG.FLUX.N"] = flux_nband

    if "Kmag" in target:
        acquisition["SEQ.TARG.MAG.K"] = np.round(np.ma.filled(target["Kmag"], 0), 2)

    if operational_mode == "gra4mat" and "Hmag" in target:
        acquisition["SEQ.TARG.MAG.H"] = np.round(np.ma.filled(target["Hmag"], 0), 2)
    return acquisition


def fill_observation(
    target: Dict,
    resolution: str,
    observation_type: str,
    operational_mode: str,
    array_configuration: str,
) -> Dict:
    """Gets the for the operational mode correct acquisition template
    and then fills it in with the information from the query.

    Parameters
    ----------
    target : dict
    resolution : str
    observation_type : str
    operational_mode : str
    array_configuration : str

    Returns
    -------
    acquisition : dict
    """
    observation = load_template(
        TEMPLATE_FILE, "observation", operational_mode=operational_mode
    )
    resolution, dit, wl0, photometry = get_observation_settings(
        resolution, operational_mode, array_configuration
    )
    observation_type = "SCIENCE" if observation_type == "sci" else "CALIB"
    observation["DPR.CATG"] = observation_type
    observation["INS.DIL.NAME"] = resolution
    observation["DET1.DIT"] = dit
    observation["SEQ.PHOTO.ST"] = "T" if photometry else "F"
    observation["SEQ.DIL.WL0"] = wl0
    return observation


def compose_ob(
    target_name: str,
    ob_kind: str,
    array: str,
    mode: str | None = "st",
    sci_name: str | None = None,
    tag: str | None = None,
    resolution: str | None = "low",
) -> Dict:
    """Composes the dictionary

    Parameters
    ----------
    target_name : str
        The target's name.
    ob_kind : str
        The type of OB. If it is a science target ("sci") or a calibrator ("cal").
    array : str
        Determines the array configuration. Possible values are "UTs",
        "small", "medium", "large", "extended".
    mode : str, optional
        The mode of operation for MATISSE. Can be either "st"/"standalone"
        for the MATISSE-standalone mode or "gr"/"gra4mat" for GRA4MAT.
        Default is standalone.
    sci_name : str, optional
        The name of the science target. If the OB is a science OB, this
        is None.
    tag : str, optional
        The calibrator tag (L, N or LN).
    resolution : str, optional
        The resolution of the OB. Can be either "low", "med" or "high".

    Returns
    -------
    target : dict
        A dictionary containg all the target's information.
    """
    array = array.lower()
    if array not in ["uts", "small", "medium", "large", "extended"]:
        raise IOError(
            "Unknown array configuration provided!"
            " Choose from 'UTs', 'small', 'medium',"
            " 'large' or 'extended'."
        )

    ob_kind = ob_kind.lower()
    if ob_kind not in ["sci", "cal"]:
        raise IOError(
            "Unknown observation type provided!"
            " Choose from 'SCI' or 'CAL', for "
            "a science target or a calibrator."
        )

    mode = mode.lower()
    if mode in ["st", "standalone"]:
        mode = "matisse"
    elif mode in ["gr", "gra4mat"]:
        mode = "gra4mat"
    else:
        raise IOError(
            "Unknown operational mode provided!"
            " Choose from 'st'/'standalone' or"
            " 'gr'/'gra4mat'."
        )

    resolution = resolution.lower()
    if resolution not in ["low", "med", "high"]:
        raise IOError(
            "Unknown resolution provided!" " Choose from 'low', 'med' or 'high'."
        )

    target = query(target_name)
    header = fill_header(target, ob_kind, array, sci_name, tag)
    acquisition = fill_acquisition(target, mode, array)
    observation = fill_observation(target, resolution, ob_kind, mode, array)
    return {"header": header, "acquisition": acquisition, "observation": observation}
