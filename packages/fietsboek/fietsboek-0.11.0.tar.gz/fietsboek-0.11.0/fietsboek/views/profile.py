"""Endpoints for the user profile pages."""

import datetime
import logging
import sqlite3
import urllib.parse

import sqlalchemy
from pyramid.httpexceptions import HTTPNotFound
from pyramid.request import Request
from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy import select
from sqlalchemy.orm import aliased

from .. import models, util
from ..data import DataManager, UserDataDir
from ..models.track import TrackType, TrackWithMetadata
from ..summaries import CumulativeStats, Summary

# A well-made transparent tile is actually pretty small (only 116 bytes), which
# is even smaller than our HTTP 404 page. So not only is it more efficient
# (bandwidth-wise) to transfer the transparent PNG, it also means that we can
# set cache headers, which the client will honor.
#
# Since the tile is so small, we've embedded it right here in the source.
#
# The tile is taken and adapted from hittekaart, which in turn took inspiration
# from https://www.mjt.me.uk/posts/smallest-png/ and
# http://www.libpng.org/pub/png/spec/1.2/PNG-Contents.html
# fmt: off
EMPTY_TILE = bytes([
    0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a, 0x00, 0x00, 0x00, 0x0d,
    0x49, 0x48, 0x44, 0x52, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01, 0x00,
    0x01, 0x03, 0x00, 0x00, 0x00, 0x66, 0xbc, 0x3a, 0x25, 0x00, 0x00, 0x00,
    0x03, 0x50, 0x4c, 0x54, 0x45, 0x00, 0xff, 0x00, 0x34, 0x5e, 0xc0, 0xa8,
    0x00, 0x00, 0x00, 0x01, 0x74, 0x52, 0x4e, 0x53, 0x00, 0x40, 0xe6, 0xd8,
    0x66, 0x00, 0x00, 0x00, 0x1f, 0x49, 0x44, 0x41, 0x54, 0x68, 0x81, 0xed,
    0xc1, 0x01, 0x0d, 0x00, 0x00, 0x00, 0xc2, 0xa0, 0xf7, 0x4f, 0x6d, 0x0e,
    0x37, 0xa0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xbe, 0x0d,
    0x21, 0x00, 0x00, 0x01, 0x9a, 0x60, 0xe1, 0xd5, 0x00, 0x00, 0x00, 0x00,
    0x49, 0x45, 0x4e, 0x44, 0xae, 0x42, 0x60, 0x82,
])
# fmt: on

LOGGER = logging.getLogger(__name__)


def profile_data(request: Request) -> dict:
    """Retrieves the profile data for the given request."""
    total = CumulativeStats()

    query = request.context.all_tracks_query()
    query = select(aliased(models.Track, query)).where(query.c.type == TrackType.ORGANIC)
    track: models.Track
    for track in request.dbsession.execute(query).scalars():
        meta = TrackWithMetadata(track, request.data_manager)
        total.add(meta)

    total.moving_time = util.round_to_seconds(total.moving_time)
    total.stopped_time = util.round_to_seconds(total.stopped_time)

    user_id = request.context.id
    heatmap_url = None
    tilehunt_url = None
    try:
        user_dir: UserDataDir = request.data_manager.open_user(request.context.id)
    except FileNotFoundError:
        pass
    else:
        if user_dir.heatmap_path().is_file():
            heatmap_url = util.tile_url(request, "user-tile", user_id=user_id, map="heatmap")
        if user_dir.tilehunt_path().is_file():
            tilehunt_url = util.tile_url(request, "user-tile", user_id=user_id, map="tilehunt")

    return {
        "user": request.context,
        "total": total,
        "mps_to_kph": util.mps_to_kph,
        "heatmap_url": heatmap_url,
        "tilehunt_url": tilehunt_url,
    }


@view_config(
    route_name="profile-overview",
    renderer="fietsboek:templates/profile_overview.jinja2",
    request_method="GET",
    permission="profile.view",
)
def profile_overview(request: Request) -> dict:
    """Shows the profile page.

    :param request: The pyramid request.
    :return: The template parameters.
    """
    data = profile_data(request)
    return data


@view_config(
    route_name="profile-graphs",
    renderer="fietsboek:templates/profile_graphs.jinja2",
    request_method="GET",
    permission="profile.view",
)
def profile_graphs(request: Request) -> dict:
    """Shows the user's graphs.

    :param request: The pyramid request.
    :return: The template parameters.
    """
    return {
        "user": request.context,
    }


@view_config(
    route_name="profile-calendar",
    renderer="fietsboek:templates/profile_calendar.jinja2",
    request_method="GET",
    permission="profile.view",
)
def profile_calendar(request: Request) -> dict:
    """Shows the user's calendar for the current month.

    :param request: The pyramid request.
    :return: The template parameters.
    """
    date = datetime.date.today()
    data = {}
    data["user"] = request.context
    data["calendar_rows"] = calendar_rows(
        request.dbsession,
        request.data_manager,
        request.context,
        date.year,
        date.month,
    )
    data["calendar_month"] = date
    data["calendar_prev"], data["calendar_next"] = prev_next_month(date)
    data["tab_focus"] = "calendar"
    data["day_name"] = util.day_name
    return data


@view_config(
    route_name="profile-calendar-ym",
    renderer="fietsboek:templates/profile_calendar.jinja2",
    request_method="GET",
    permission="profile.view",
)
def profile_calendar_ym(request: Request) -> dict:
    """Shows the user's calendar.

    :param request: The pyramid request.
    :return: The template parameters.
    """
    date = datetime.date(int(request.matchdict["year"]), int(request.matchdict["month"]), 1)
    data = {}
    data["user"] = request.context
    data["calendar_rows"] = calendar_rows(
        request.dbsession,
        request.data_manager,
        request.context,
        date.year,
        date.month,
    )
    data["calendar_month"] = date
    data["calendar_prev"], data["calendar_next"] = prev_next_month(date)
    data["tab_focus"] = "calendar"
    data["day_name"] = util.day_name
    return data


def cell_style(tracks: list[TrackWithMetadata]) -> str:
    """Returns the correct CSS style for a day with the given tracks.

    The style is determined by the amount of kilometers cycled on that day.

    :param tracks: The list of tracks.
    :return: The CSS style for the calendar cell.
    """
    length = sum(track.length for track in tracks)
    # kilometers
    length = length / 1000
    # Arbitrary cutoffs for the moment
    if length == 0:
        return "cell-length-0"
    if length <= 25:
        return "cell-length-1"
    if length <= 50:
        return "cell-length-2"
    if length <= 75:
        return "cell-length-3"
    if length <= 100:
        return "cell-length-4"
    return "cell-length-5"


def calendar_rows(
    dbsession: "sqlalchemy.orm.session.Session",
    data_manager: DataManager,
    user: models.User,
    year: int,
    month: int,
) -> list:
    """Lays out the calendar for the given user and the given year/month.

    :param dbsession: The database session.
    :param user: The user for which to retrieve the calendar.
    :param year: The year.
    :apram month: The month.
    :return: The calendar rows, ready to pass to the profile template.
    """
    # Four steps:
    # 1. Get all tracks of the user
    # 2. Build the calendar by getting the dates in the given month
    # 3. Associcate the tracks with their respective date
    # 4. Layout the calendar week-wise

    # Step 1: Retrieve all tracks
    query = user.all_tracks_query()
    query = select(aliased(models.Track, query)).where(query.c.type == TrackType.ORGANIC)
    tracks = [
        TrackWithMetadata(track, data_manager) for track in dbsession.execute(query).scalars()
    ]

    # Step 2: Build the calendar
    days = []
    current_day = datetime.date(year, month, 1)
    while True:
        days.append(current_day)
        current_day += datetime.timedelta(days=1)
        if current_day.month != int(month):
            break

    # Step 3: Associate days and tracks
    days = [
        (day, [track for track in tracks if track.date and track.date.date() == day])
        for day in days
    ]

    # Step 3.5: Style the cells
    days = [(day, cell_style(tracks), tracks) for (day, tracks) in days]

    # Step 4: Layout
    rows = []
    row: list[None | tuple[datetime.date, str, list[TrackWithMetadata]]] = []
    while days:
        next_day = days.pop(0)
        # This should only matter in the first row, when the month does not
        # start on a Monday. Otherwise, the range is always 0.
        for _ in range(next_day[0].weekday() - len(row)):
            row.append(None)
        row.append(next_day)
        if next_day[0].weekday() == 6:
            rows.append(row)
            row = []
    # Append last if month doesn't end on a Sunday
    if row:
        row += [None] * (7 - len(row))
        rows.append(row)

    return rows


def prev_next_month(date: datetime.date) -> tuple[datetime.date, datetime.date]:
    """Return the previous and next months.

    Months are normalized to the first day of the month.
    """
    date = date.replace(day=1)
    prev = (date - datetime.timedelta(days=1)).replace(day=1)
    nxt = (date + datetime.timedelta(days=32)).replace(day=1)
    return (prev, nxt)


@view_config(
    route_name="user-tile",
    request_method="GET",
    permission="profile.view",
    http_cache=datetime.timedelta(hours=1),
)
def user_tile(request: Request) -> Response:
    """Returns a single tile from the user's own overlay maps.

    :param request: The pyramid request.
    :return: The response, with the tile content (or an error).
    """
    try:
        user_dir: UserDataDir = request.data_manager.open_user(request.context.id)
    except FileNotFoundError:
        return HTTPNotFound()

    paths = {
        "heatmap": user_dir.heatmap_path(),
        "tilehunt": user_dir.tilehunt_path(),
    }
    path = paths.get(request.matchdict["map"])
    if path is None:
        return HTTPNotFound()

    # See
    # https://docs.python.org/3/library/sqlite3.html#how-to-work-with-sqlite-uris
    # https://stackoverflow.com/questions/10205744/opening-sqlite3-database-from-python-in-read-only-mode
    # https://stackoverflow.com/questions/17170202/dont-want-to-create-a-new-database-if-it-doesnt-already-exists
    sqlite_uri = urllib.parse.urlunparse(("file", "", str(path), "", "mode=ro", ""))
    try:
        connection = sqlite3.connect(sqlite_uri, uri=True)
    except sqlite3.OperationalError:
        return HTTPNotFound()

    cursor = connection.cursor()
    result = cursor.execute(
        "SELECT data FROM tiles WHERE zoom = ? AND x = ? AND y = ?;",
        (int(request.matchdict["z"]), int(request.matchdict["x"]), int(request.matchdict["y"])),
    )
    result = result.fetchone()
    if result is None:
        return Response(EMPTY_TILE, content_type="image/png")

    return Response(result[0], content_type="image/png")


@view_config(
    route_name="json-summary", request_method="GET", permission="profile.view", renderer="json"
)
def json_summary(request: Request) -> Response:
    """Returns the per-month summary as JSON.

    :param request: The pyramid request.
    :return: The response, rendered as JSON.
    """
    query = request.identity.all_tracks_query()
    query = select(aliased(models.Track, query)).where(query.c.type == TrackType.ORGANIC)
    summary = Summary()

    for track in request.dbsession.execute(query).scalars():
        if track.cache is None:
            LOGGER.debug("Skipping track %d as it has no cached metadata", track.id)
            continue
        summary.add(TrackWithMetadata(track, request.data_manager))

    return {y.year: {m.month: m.total_length for m in y} for y in summary}


__all__ = [
    "EMPTY_TILE",
    "profile_overview",
    "profile_graphs",
    "profile_calendar",
    "profile_calendar_ym",
    "user_tile",
    "json_summary",
]
