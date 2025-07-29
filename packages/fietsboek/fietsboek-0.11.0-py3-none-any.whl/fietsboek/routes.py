"""Route definitions for the main Fietsboek application."""


def includeme(config):
    # pylint: disable=missing-function-docstring
    config.add_static_view("static", "static", cache_max_age=3600)
    config.add_route("home", "/")
    config.add_route("login", "/login")
    config.add_route("logout", "/logout")
    config.add_route("browse", "/track/")

    config.add_route("static-page", "/page/{slug}")

    config.add_route("track-archive", "/track/archive")

    config.add_route("password-reset", "/password-reset")
    config.add_route("resend-verification", "/resend-verification")
    config.add_route("use-token", "/token/{uuid}")
    config.add_route("create-account", "/create-account")

    config.add_route("upload", "/upload")
    config.add_route(
        "preview", "/upload/{upload_id}/preview.gpx", factory="fietsboek.models.Upload.factory"
    )
    config.add_route(
        "finish-upload", "/upload/{upload_id}", factory="fietsboek.models.Upload.factory"
    )
    config.add_route(
        "cancel-upload", "/upload/{upload_id}/cancel", factory="fietsboek.models.Upload.factory"
    )

    config.add_route("details", "/track/{track_id}", factory="fietsboek.models.Track.factory")
    config.add_route("edit", "/track/{track_id}/edit", factory="fietsboek.models.Track.factory")
    config.add_route("gpx", "/track/{track_id}/gpx", factory="fietsboek.models.Track.factory")
    config.add_route(
        "invalidate-share",
        "/track/{track_id}/invalidate-link",
        factory="fietsboek.models.Track.factory",
    )
    config.add_route(
        "delete-track", "/track/{track_id}/delete", factory="fietsboek.models.Track.factory"
    )
    config.add_route(
        "add-comment", "/track/{track_id}/comment", factory="fietsboek.models.Track.factory"
    )
    config.add_route(
        "image", "/track/{track_id}/images/{image_name}", factory="fietsboek.models.Track.factory"
    )
    config.add_route(
        "track-map",
        "/track/{track_id}/preview",
        factory="fietsboek.models.Track.factory",
    )

    config.add_route("badge", "/badge/{badge_id}", factory="fietsboek.models.Badge.factory")

    config.add_route("admin", "/admin/")
    config.add_route("admin-badge", "/admin/badges/")
    config.add_route("admin-badge-add", "/admin/badges/add")
    config.add_route("admin-badge-edit", "/admin/badges/edit")
    config.add_route("admin-badge-delete", "/admin/badges/delete")

    config.add_route("user-data", "/me")
    config.add_route("add-friend", "/me/send-friend-request")
    config.add_route("delete-friend", "/me/delete-friend")
    config.add_route("accept-friend", "/me/accept-friend")
    config.add_route("json-friends", "/me/friends.json")
    config.add_route("json-summary", "/me/summary.json")
    config.add_route("toggle-favourite", "/me/toggle-favourite")
    config.add_route("force-logout", "/me/force-logout")

    config.add_route(
        "profile-overview", "/user/{user_id}/", factory="fietsboek.models.User.factory"
    )
    config.add_route(
        "profile-graphs", "/user/{user_id}/graphs", factory="fietsboek.models.User.factory"
    )
    config.add_route(
        "profile-calendar", "/user/{user_id}/calendar/", factory="fietsboek.models.User.factory"
    )
    config.add_route(
        "profile-calendar-ym",
        "/user/{user_id}/calendar/{year}/{month}",
        factory="fietsboek.models.User.factory",
    )
    config.add_route(
        "user-tile",
        "/user/{user_id}/tile/{map}/{z:\\d+}/{x:\\d+}/{y:\\d+}",
        factory="fietsboek.models.User.factory",
    )

    config.add_route("tile-proxy", "/tile/{provider}/{z:\\d+}/{x:\\d+}/{y:\\d+}")


__all__ = ["includeme"]
