from json import dumps
from logging import getLogger

from aiohttp.web import Response, View, json_response
from aiohttp_cors import CorsViewMixin

from .models import Task

logger = getLogger(__name__)


class IndexView(View, CorsViewMixin):
    async def get(self):
        return json_response(Task.all_objects())

    async def post(self):
        content = await self.request.json()
        return json_response(
            Task.create_object(content, self.request.app.router['todo'].url_for)
        )

    async def delete(self):
        Task.delete_all_objects()
        return Response()


class TodoView(View, CorsViewMixin):
    def __init__(self, request):
        super().__init__(request)
        self.uuid = request.match_info.get('uuid')

    async def get(self):
        return json_response(Task.get_object(self.uuid))

    async def patch(self):
        content = await self.request.json()
        return json_response(
            Task.update_object(self.uuid, content))

    async def delete(self):
        Task.delete_object(self.uuid)
        return Response()
