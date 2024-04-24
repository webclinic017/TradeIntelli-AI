from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


class FastAPIApp:
    app = None

    @staticmethod
    def init_app():
        if not FastAPIApp.app:
            FastAPIApp.app = FastAPI()
            origins = [
                "http://localhost:3000",  # The correct client origin
                "http://localhost:8000",  # The correct client origin
                "http://127.0.0.1:3000",
                "http://127.0.0.1:8000",
                "*",
                "*:3000",
            ]

            FastAPIApp.app.add_middleware(
                CORSMiddleware,
                allow_origins=origins,
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
        return FastAPIApp.app
