from litestar import Litestar
from litestar.config.cors import CORSConfig

from .routers.images import ImagesController

app = Litestar(
    route_handlers=[ImagesController],
    cors_config=CORSConfig(
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    ),
)
