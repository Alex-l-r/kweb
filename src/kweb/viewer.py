from pathlib import Path

from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.routing import WebSocketRoute
from starlette.endpoints import WebSocketEndpoint
from typing import Type, Any

from . import config
from .api.viewer import router

# from .layout_server import EditableLayoutViewServerEndpoint
from .layout_server import LayoutViewServerEndpoint


def get_app(fileslocation: Path | str, editable: bool = False, layer_props: Path | None = None) -> FastAPI:
    _settings = config.Config(
        fileslocation=fileslocation, 
        editable=editable,
        layer_props=layer_props
    )

    def settings() -> config.Config:
        return _settings

    staticfiles = StaticFiles(directory=Path(__file__).parent / "static")

    print(f"Creating endpoint with layer_props: {_settings.layer_props}")

    # Create a closure to capture the settings
    def get_endpoint() -> Type[WebSocketEndpoint]:
        class BrowserLayoutViewServerEndpoint(LayoutViewServerEndpoint):
            def __init__(self, scope: dict, receive: Any, send: Any) -> None:
                super().__init__(
                    scope=scope,
                    receive=receive,
                    send=send,
                    root=_settings.fileslocation,
                    editable=editable,
                    add_missing_layers=_settings.add_missing_layers,
                    meta_splitter=_settings.meta_splitter,
                    layer_props=_settings.layer_props,
                    max_rdb_limit=100
                )
        return BrowserLayoutViewServerEndpoint

    app = FastAPI(
        routes=[WebSocketRoute("/ws", endpoint=get_endpoint())]
    )

    router.dependencies.insert(0, Depends(settings))
    app.include_router(router)
    app.mount("/static", staticfiles, name="kweb_static")

    return app
