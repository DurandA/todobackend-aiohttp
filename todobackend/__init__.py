from logging import getLogger, basicConfig, INFO
from os import getenv
from aiohttp import web
import aiohttp_cors

from .views import (
    IndexView,
    TodoView,
)

IP = getenv('IP', '0.0.0.0')
PORT = getenv('PORT', '8000')

basicConfig(level=INFO)
logger = getLogger(__name__)


async def init(loop):
    app = web.Application(loop=loop)

    # Configure default CORS settings.
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
            )
    })

    # Routes
    #app.router.add_route('*', '/', IndexView)
    #app.router.add_route('*', '/{uuid}', TodoView)
    # Explicitly add individual methods, see https://github.com/aio-libs/aiohttp-cors/issues/41
    cors.add(app.router.add_route('get', '/', IndexView))
    cors.add(app.router.add_route('post', '/', IndexView))
    cors.add(app.router.add_route('delete', '/', IndexView))
    cors.add(app.router.add_route('get', '/{uuid}', TodoView))
    cors.add(app.router.add_route('patch', '/{uuid}', TodoView))
    cors.add(app.router.add_route('delete', '/{uuid}', TodoView))

    # Config
    logger.info("Starting server at %s:%s", IP, PORT)
    srv = await loop.create_server(app.make_handler(), IP, PORT)
    return srv
