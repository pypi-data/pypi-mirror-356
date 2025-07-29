"""Error views."""

from pyramid.view import forbidden_view_config, notfound_view_config


@notfound_view_config(renderer="fietsboek:templates/404.jinja2")
def notfound_view(request):
    """Renders the 404 response.

    :param request: The Pyramid request.
    :type request: pyramid.request.Request
    :return: The HTTP response.
    :rtype: pyramid.response.Response
    """
    request.response.status = 404
    return {}


@forbidden_view_config(renderer="fietsboek:templates/403.jinja2")
def forbidden_view(request):
    """Renders the 403 response.

    :param request: The Pyramid request.
    :type request: pyramid.request.Request
    :return: The HTTP response.
    :rtype: pyramid.response.Response
    """
    request.response.status = 403
    return {}


__all__ = ["notfound_view", "forbidden_view"]
