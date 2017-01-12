import uuid

from django.conf import settings

REQUEST_ID_HEADER = getattr(settings, 'REQUEST_ID_HEADER', 'X-Request-ID')
INCLUDE_REQUEST_ID_IN_RESPONSE = getattr(settings, 'INCLUDE_REQUEST_ID_IN_RESPONSE', False)


class RequestIdMiddleware(object):
    def process_request(self, request):
        if not hasattr(request, 'id'):
            request.id = uuid.uuid4().hex

    def process_response(self, request, response):
        if all([
            INCLUDE_REQUEST_ID_IN_RESPONSE,
            REQUEST_ID_HEADER not in response,
            hasattr(request, 'id'),
        ]):
            response[REQUEST_ID_HEADER] = request.id

        return response
