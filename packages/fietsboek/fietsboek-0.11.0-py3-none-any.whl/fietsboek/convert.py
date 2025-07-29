"""Conversion functions to convert between various recording formats."""

import fitparse
from gpxpy.gpx import GPX, GPXTrack, GPXTrackPoint, GPXTrackSegment

FIT_RECORD_FIELDS = ["position_lat", "position_long", "altitude", "timestamp"]


def semicircles_to_deg(circles: int) -> float:
    """Convert semicircles coordinate to degree coordinate.

    :param circles: The coordinate value in semicircles.
    :return: The coordinate in degrees.
    """
    return circles * (180 / 2**31)


def from_fit(data: bytes) -> GPX:
    """Reads a .fit as GPX data.

    This uses the fitparse_ library under the hood.

    .. _fitparse: https://pypi.org/project/fitparse/

    :param data: The input bytes.
    :return: The converted structure.
    """
    fitfile = fitparse.FitFile(data)
    points = []
    for record in fitfile.get_messages("record"):
        values = record.get_values()
        try:
            if any(values[field] is None for field in FIT_RECORD_FIELDS):
                continue
            point = GPXTrackPoint(
                latitude=semicircles_to_deg(values["position_lat"]),
                longitude=semicircles_to_deg(values["position_long"]),
                elevation=values["altitude"],
                time=values["timestamp"],
            )
        except KeyError:
            pass
        else:
            points.append(point)
    track = GPXTrack()
    track.segments = [GPXTrackSegment(points)]
    gpx = GPX()
    gpx.tracks = [track]
    return gpx


def smart_convert(data: bytes) -> bytes:
    """Tries to be smart in converting the input bytes.

    This function automatically applies the correct conversion if possible.

    Note that this function is not guaranteed to return valid GPX bytes. In the worst case,
    invalid bytes are simply passed through.

    :param data: The input bytes.
    :return: The converted content.
    """
    if len(data) > 11 and data[9:12] == b"FIT":
        return from_fit(data).to_xml().encode("utf-8")
    return data


__all__ = ["from_fit", "smart_convert"]
