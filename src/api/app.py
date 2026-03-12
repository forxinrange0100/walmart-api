from fastapi import FastAPI, Query
from api.constants.models import models
from api.services.get_metrics import get_metrics
from api.services.check_health import check_health
from api.services.make_predictions import make_predictions
from api.responses import HealthResponse, MetricsResponse, PredictionResponse
from api.errors import InvalidDataError, NotFoundDataError, handle_internal_error, handle_invalid_data_error, handle_not_found_error

def create_app() -> FastAPI:
    app = FastAPI(
        title="Walmart API",
        description=(
            "REST API to serve trained forecasting models for Walmart stores. "
            "Provides health checks, weekly sales predictions, and model performance metrics."
        ),
        version="1.0.0"
        )
    app.add_exception_handler(NotFoundDataError, handle_not_found_error)
    app.add_exception_handler(InvalidDataError, handle_invalid_data_error)
    app.add_exception_handler(Exception, handle_internal_error)

    @app.get("/", 
             summary="Health check", 
             description="Verifies that all model and metrics artifacts exist and are accessible. ", 
             tags=["Health"], 
             response_model=HealthResponse,
             responses={
                404: {"description": "File not found"},
                500: {"description": "Internal server error"}
            })
    def root():
        return check_health(models=models)
    @app.get("/predict", 
             summary="Generate sales forecasts", 
             description=(
                 "Generates weekly sales forecast for all configured stores "
                "using the available trained models."
            ), 
             tags=["Forecast"], 
             response_model=PredictionResponse,
             responses={
                404: {"description": "File not found"},
                400: {"description": "Invalid File"},
                500: {"description": "Internal server error"}                 
             })    
    def predict(horizon: int = Query(12, description="Number of future weeks to forecast")):
        return make_predictions(models=models, horizon=horizon)


    @app.get("/metrics", 
            summary="Retrieve model performance metrics", 
            description=(
                "Returns store-level error metrics and aggregated average metrics "
                "for each forecasting model."
            ), 
            tags=["Metrics"], 
            response_model=MetricsResponse,
            responses={
                404: {"description": "File not found"},
                400: {"description": "Invalid File"},
                500: {"description": "Internal server error"}                 
             })
    def metrics():
        return get_metrics(models=models)
    return app
app = create_app()
