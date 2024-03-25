# from app import historical_data_controller
from infastructure.fast_api_app import FastAPIApp

from app.historical_data_controller import router as historical_data_router
app = FastAPIApp.init_app()

app.include_router(historical_data_router)


