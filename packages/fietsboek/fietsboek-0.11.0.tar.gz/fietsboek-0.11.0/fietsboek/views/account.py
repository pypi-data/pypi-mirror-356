"""Account related endpoints."""

from pyramid.httpexceptions import HTTPForbidden, HTTPFound
from pyramid.i18n import TranslationString as _
from pyramid.view import view_config

from .. import actions, models, util


@view_config(
    route_name="create-account",
    renderer="fietsboek:templates/create_account.jinja2",
    request_method="GET",
)
def create_account(request):
    """Shows the "create account" page.

    :param request: The Pyramid request.
    :type request: pyramid.request.Request
    :return: The HTTP response.
    :rtype: pyramid.response.Response
    """
    # pylint: disable=unused-argument
    if not request.config.enable_account_registration:
        return HTTPForbidden()
    return {}


@view_config(
    route_name="create-account",
    renderer="fietsboek:templates/create_account.jinja2",
    request_method="POST",
)
def do_create_account(request):
    """Shows the "create account" page.

    :param request: The Pyramid request.
    :type request: pyramid.request.Request
    :return: The HTTP response.
    :rtype: pyramid.response.Response
    """
    # pylint: disable=duplicate-code
    if not request.config.enable_account_registration:
        return HTTPForbidden()
    password = request.params["password"]
    try:
        util.check_password_constraints(password, request.params["repeat-password"])
    except ValueError as exc:
        request.session.flash(request.localizer.translate(exc.args[0]))
        return HTTPFound(request.route_url("create-account"))

    name = request.params["name"]
    if not name:
        request.session.flash(request.localizer.translate(_("flash.invalid_name")))
        return HTTPFound(request.route_url("create-account"))

    email_addr = request.params["email"]
    if not email_addr:
        request.session.flash(request.localizer.translate(_("flash.invalid_email")))
        return HTTPFound(request.route_url("create-account"))

    user = models.User(name=name, email=email_addr)
    user.set_password(password)
    user.roll_session_secret()
    request.dbsession.add(user)

    actions.send_verification_token(request, user)

    request.session.flash(request.localizer.translate(_("flash.a_confirmation_link_has_been_sent")))
    return HTTPFound(request.route_url("login"))


__all__ = ["create_account", "do_create_account"]
