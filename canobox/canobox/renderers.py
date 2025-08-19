# myproject/renderers.py
from rest_framework.renderers import JSONRenderer

class DataWrapperJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        # 이미 에러일 경우 그대로 전달
        if renderer_context and renderer_context.get('response').status_code >= 400:
            return super().render(data, accepted_media_type, renderer_context)
        # 성공 응답일 경우 data로 감싸기
        return super().render({'data': data}, accepted_media_type, renderer_context)
