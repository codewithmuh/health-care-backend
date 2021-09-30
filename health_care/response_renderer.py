import copy
import json

from rest_framework.renderers import JSONRenderer


class ApiRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code
        response = {
            "status": "true",
            "code": status_code,
            "data": data,
            "message": None
        }

        if not str(status_code).startswith('2'):
            response["status"] = "false"
            response["data"] = None
            try:
                keys = data.keys()
                for key in keys:
                    response["message"] = data.get(key)[0]
                    break
            except Exception as e:
                print(e)
                response["data"] = None

        return super(ApiRenderer, self).render(response, accepted_media_type, renderer_context)
