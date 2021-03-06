import uuid

from django.conf import settings

REQUEST_ID_HEADER = getattr(settings, "REQUEST_ID_HEADER", "X-Request-ID")
INCLUDE_REQUEST_ID_IN_RESPONSES = getattr(settings, "INCLUDE_REQUEST_ID_IN_RESPONSES", False)


def request_id_middleware(get_response):
    def middleware(request):
        if not hasattr(request, "id"):
            request.id = uuid.uuid4().hex

        response = get_response(request)

        if all([INCLUDE_REQUEST_ID_IN_RESPONSES, REQUEST_ID_HEADER not in response, hasattr(request, "id"),]):
            response[REQUEST_ID_HEADER] = request.id

        return response

    return middleware
