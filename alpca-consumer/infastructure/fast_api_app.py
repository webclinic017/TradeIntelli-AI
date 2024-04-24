from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request

class FastAPIApp:
    app = None


    @staticmethod
    def init_app():
        if not FastAPIApp.app:
            FastAPIApp.app = FastAPI()
            origins = [
                "*",
                "http://127.0.0.1:3000",
                "http://localhost:3000",
                "http://npm:3000",
            ]

            FastAPIApp.app.add_middleware(
                CORSMiddleware,
                allow_origins=origins,
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
        return FastAPIApp.app


app = FastAPIApp.init_app()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    print(f"Request path: {request.url.path}, Response status: {response.status_code}")
    return response
