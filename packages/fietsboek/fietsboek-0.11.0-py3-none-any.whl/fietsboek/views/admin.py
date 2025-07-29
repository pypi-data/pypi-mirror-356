"""Admin views."""

import datetime
import platform
import stat
from dataclasses import dataclass
from pathlib import Path

from pyramid.httpexceptions import HTTPFound
from pyramid.i18n import TranslationString as _
from pyramid.request import Request
from pyramid.view import view_config
from sqlalchemy import func, select

from .. import models, util

GOOD_CRON_THRESHOLD = datetime.timedelta(hours=1)


def _safe_size(path: Path) -> int:
    try:
        res = path.stat()
        if stat.S_ISDIR(res.st_mode):
            return util.recursive_size(path)
        if stat.S_ISREG(res.st_mode):
            return res.st_size
        return 0
    except FileNotFoundError:
        return 0


@dataclass
class SizeBreakdown:
    """A breakdown of what objects take how much storage."""

    gpx_files: int = 0
    image_files: int = 0
    preview_files: int = 0
    user_maps: int = 0


def _get_size_breakdown(data_manager):
    breakdown = SizeBreakdown()

    for track_id in data_manager.list_tracks():
        track = data_manager.open(track_id)
        breakdown.gpx_files += _safe_size(track.gpx_path())
        breakdown.preview_files += _safe_size(track.preview_path())
        for image_id in track.images():
            breakdown.image_files += _safe_size(track.image_path(image_id))

    for user_id in data_manager.list_users():
        user = data_manager.open_user(user_id)
        breakdown.user_maps += _safe_size(user.heatmap_path())
        breakdown.user_maps += _safe_size(user.tilehunt_path())

    return breakdown


def _get_fietsboek_version():
    # pylint: disable=import-outside-toplevel
    from fietsboek import __VERSION__

    return __VERSION__


@view_config(
    route_name="admin",
    renderer="fietsboek:templates/admin_overview.jinja2",
    request_method="GET",
    permission="admin",
)
def admin(request: Request):
    """Renders the admin overview.

    :param request: The Pyramid request.
    :return: The HTTP response.
    """
    # False-positive with func.count()
    # pylint: disable=not-callable
    user_count = request.dbsession.execute(select(func.count()).select_from(models.User)).scalar()
    track_count = request.dbsession.execute(select(func.count()).select_from(models.Track)).scalar()
    size_total = request.data_manager.size()
    size_breakdown = _get_size_breakdown(request.data_manager)

    try:
        distro = platform.freedesktop_os_release()["PRETTY_NAME"]
    except OSError:
        distro = None

    try:
        last_cronjob_timestamp = float(request.redis.get("last-cronjob"))
    except (TypeError, ValueError):
        last_cronjob = None
        cron_good = False
    else:
        last_cronjob = datetime.datetime.fromtimestamp(last_cronjob_timestamp, datetime.UTC)
        cron_good = (datetime.datetime.now(datetime.UTC) - last_cronjob) < GOOD_CRON_THRESHOLD

    versions = {
        "fietsboek": _get_fietsboek_version(),
        "python": platform.python_version(),
        "linux": platform.platform(),
        "distro": distro,
    }

    return {
        "user_count": user_count,
        "track_count": track_count,
        "total_size": size_total,
        "size_breakdown": size_breakdown,
        "versions": versions,
        "last_cronjob": last_cronjob,
        "cron_good": cron_good,
    }


@view_config(
    route_name="admin-badge",
    renderer="fietsboek:templates/admin_badges.jinja2",
    request_method="GET",
    permission="admin",
)
def admin_badges(request):
    """Renders the badges editor.

    :param request: The Pyramid request.
    :type request: pyramid.request.Request
    :return: The HTTP response.
    :rtype: pyramid.response.Response
    """
    badges = request.dbsession.execute(select(models.Badge)).scalars()
    return {
        "badges": badges,
    }


@view_config(route_name="admin-badge-add", permission="admin", request_method="POST")
def do_badge_add(request):
    """Adds a badge.

    This is the endpoint of a form on the admin overview.

    :param request: The Pyramid request.
    :type request: pyramid.request.Request
    :return: The HTTP response.
    :rtype: pyramid.response.Response
    """

    image = request.params["badge-image"].file.read()
    title = request.params["badge-title"]

    badge = models.Badge(title=title, image=image)
    request.dbsession.add(badge)

    request.session.flash(request.localizer.translate(_("flash.badge_added")))
    return HTTPFound(request.route_url("admin-badge"))


@view_config(route_name="admin-badge-edit", permission="admin", request_method="POST")
def do_badge_edit(request):
    """Modifies an already existing badge.

    This is the endpoint of a form on the admin overview.

    :param request: The Pyramid request.
    :type request: pyramid.request.Request
    :return: The HTTP response.
    :rtype: pyramid.response.Response
    """
    badge = request.dbsession.execute(
        select(models.Badge).filter_by(id=request.params["badge-edit-id"])
    ).scalar_one()
    try:
        badge.image = request.params["badge-image"].file.read()
    except AttributeError:
        pass
    badge.title = request.params["badge-title"]

    request.session.flash(request.localizer.translate(_("flash.badge_modified")))
    return HTTPFound(request.route_url("admin-badge"))


@view_config(route_name="admin-badge-delete", permission="admin", request_method="POST")
def do_badge_delete(request):
    """Removes a badge.

    This is the endpoint of a form on the admin overview.

    :param request: The Pyramid request.
    :type request: pyramid.request.Request
    :return: The HTTP response.
    :rtype: pyramid.response.Response
    """
    badge = request.dbsession.execute(
        select(models.Badge).filter_by(id=request.params["badge-delete-id"])
    ).scalar_one()
    request.dbsession.delete(badge)

    request.session.flash(request.localizer.translate(_("flash.badge_deleted")))
    return HTTPFound(request.route_url("admin-badge"))


__all__ = ["admin", "admin_badges", "do_badge_add", "do_badge_edit", "do_badge_delete"]
