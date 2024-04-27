from infastructure.fast_api_app import FastAPIApp

from application.historical_data_controller import router as historical_data_router
from application.configurations_controller import router as config_data_router
app = FastAPIApp.init_app()

app.include_router(historical_data_router)
app.include_router(config_data_router)


