import os
import logging
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


logger = logging.getLogger('request')
mailing_logger = logging.getLogger('mailing')
client_logger = logging.getLogger('client')


class RequestLoggingMiddleware(MiddlewareMixin):

    @staticmethod
    def _save_log(request, obj_name):
        parts = request.path.split('/')
        obj_id = parts[-2] if parts[-2].isdigit() else None
        message = {
            'method': request.method,
            'path': request.path,
            'body': request.body
        }

        if obj_id:
            message = {'id': obj_id,
                       'method': request.method,
                       'path': request.path,
                       'body': request.body
                       }

        if obj_name == 'mailing':
            mailing_logger.info(message)
        if obj_name == 'client':
            client_logger.info(message)

    def __call__(self, request):

        logger.info({
            'method': request.method,
            'path': request.path,
            'body': request.body,
            'headers': dict(request.headers)
        })

        views = ['mailing', 'message', 'client']

        for view in views:
            if view in request.path:
                self._save_log(request, str(view))

        response = self.get_response(request)

        return response
