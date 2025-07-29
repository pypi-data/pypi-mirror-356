from typing import Any
import xyzservices.providers as xyz


def resolve_basemap_name(basemap_name: str) -> Any:
    """
    Resolve a basemap name into an xyzservices object.

    Parameters
    ----------
    basemap_name : str
        Dot-separated name of the basemap (e.g., 'Esri.WorldImagery').

    Returns
    -------
    Any
        A xyzservices object, compatible with both folium and ipyleaflet.

    Raises
    ------
    AttributeError
        If the basemap name is not valid.
    """
    provider = xyz
    for part in basemap_name.split("."):
        if hasattr(provider, part):
            provider = getattr(provider, part)
        else:
            raise AttributeError(f"Unsupported basemap: {basemap_name}")
    return provider
