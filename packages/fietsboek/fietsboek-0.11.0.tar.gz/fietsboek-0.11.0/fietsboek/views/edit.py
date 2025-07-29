"""Views for editing a track."""

import datetime
import logging
from collections import namedtuple

import gpxpy
from pyramid.httpexceptions import HTTPBadRequest, HTTPFound
from pyramid.i18n import TranslationString as _
from pyramid.view import view_config
from sqlalchemy import select

from .. import actions, convert, models, util
from ..data import TrackDataDir
from ..models.track import TrackType, Visibility

ImageEmbed = namedtuple("ImageEmbed", "name url description")

LOGGER = logging.getLogger(__name__)


@view_config(
    route_name="edit",
    renderer="fietsboek:templates/edit.jinja2",
    permission="track.edit",
    request_method="GET",
)
def edit(request):
    """Renders the edit form.

    :param request: The Pyramid request.
    :type request: pyramid.request.Request
    :return: The HTTP response.
    :rtype: pyramid.response.Response
    """
    track = request.context
    badges = request.dbsession.execute(select(models.Badge)).scalars()
    badges = [(badge in track.badges, badge) for badge in badges]

    on_disk_images = []
    try:
        on_disk_images = request.data_manager.open(track.id).images()
    except FileNotFoundError:
        pass
    images = []
    for image in on_disk_images:
        metadata = request.dbsession.execute(
            select(models.ImageMetadata).filter_by(track=track, image_name=image)
        ).scalar_one_or_none()
        if metadata:
            description = metadata.description
        else:
            description = ""
        img_src = request.route_url("image", track_id=track.id, image_name=image)
        images.append(ImageEmbed(image, img_src, description))

    return {
        "track": track,
        "badges": badges,
        "images": images,
    }


@view_config(route_name="edit", permission="track.edit", request_method="POST")
def do_edit(request):
    """Endpoint for saving the edited data.

    :param request: The Pyramid request.
    :type request: pyramid.request.Request
    :return: The HTTP response.
    :rtype: pyramid.response.Response
    """
    # pylint: disable=duplicate-code,broad-exception-caught
    track = request.context

    user_friends = request.identity.get_friends()
    badges = util.retrieve_multiple(request.dbsession, models.Badge, request.params, "badge[]")
    tagged_people = util.retrieve_multiple(
        request.dbsession, models.User, request.params, "tagged-friend[]"
    )

    if any(user not in track.tagged_people and user not in user_friends for user in tagged_people):
        return HTTPBadRequest()

    data: TrackDataDir = request.data_manager.open(track.id)
    tz_offset = datetime.timedelta(minutes=int(request.params["date-tz"]))
    date = datetime.datetime.fromisoformat(request.params["date"])
    with data, data.lock():
        redo_cache = False
        try:
            gpx_bytes = request.POST["gpx"].file.read()
        except AttributeError:
            pass
        else:
            LOGGER.info("Setting new track for %s", track.id)
            gpx_bytes = convert.smart_convert(gpx_bytes)
            try:
                gpxpy.parse(gpx_bytes)
            except Exception as exc:
                request.session.flash(request.localizer.translate(_("flash.invalid_file")))
                LOGGER.info("Could not parse updated gpx: %s", exc)
                return HTTPFound(request.route_url("edit", track_id=track.id))
            data.compress_gpx(gpx_bytes)
            data.backup()
            track.transformers = []
            redo_cache = True

        track.date = date.replace(tzinfo=datetime.timezone(tz_offset))

        track.tagged_people = tagged_people
        track.title = request.params["title"]
        track.visibility = Visibility[request.params["visibility"]]
        track.type = TrackType[request.params["type"]]
        track.description = request.params["description"]
        track.badges = badges
        tags = request.params.getall("tag[]")
        track.sync_tags(tags)

        actions.edit_images(request, request.context, manager=data)
        gpx = actions.execute_transformers(request, request.context)
        data.engrave_metadata(
            title=track.title,
            description=track.description,
            author_name=track.owner.name,
            time=track.date,
            gpx=gpx,
        )

        # actions.execute_transformers automatically rebuilds the cache, so we only need to do
        # this if execute_transformers didn't do it
        if redo_cache and gpx is None:
            LOGGER.info("New file detected, rebuilding cache for %s", track.id)
            track.cache = None
            track.ensure_cache(gpx_bytes)
            request.dbsession.add(track.cache)

    return HTTPFound(request.route_url("details", track_id=track.id))


__all__ = ["ImageEmbed", "edit", "do_edit"]
