from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


class FastAPIApp:
    app = None

    @staticmethod
    def init_app():
        if not FastAPIApp.app:
            FastAPIApp.app = FastAPI()
            origins = [
                "http://127.0.0.1:3000",
                "*",
            ]

            FastAPIApp.app.add_middleware(
                CORSMiddleware,
                allow_origins=origins,
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
        return FastAPIApp.app
