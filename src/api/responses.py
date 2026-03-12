from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(
        ...,
        description="Overall API health status",
        example="ok"
    )
    files: list[str] = Field(
        ...,
        description="List of model and metric artifact file paths that were validated",
        example=[
            "./artifacts/models/arima_train_pipeline.pkl",
            "./artifacts/metrics/arima_train_pipeline.csv",
            "./artifacts/models/sarima_train_pipeline.pkl",
            "./artifacts/metrics/sarima_train_pipeline.csv"
        ]
    )


class ForecastItem(BaseModel):
    unique_id: int = Field(
        ...,
        description="Unique store identifier",
        example=1
    )
    ds: str = Field(
        ...,
        description="Forecasted week date (YYYY-MM-DD)",
        example="2012-10-28"
    )
    sales: float = Field(
        ...,
        description="Predicted weekly sales value",
        example=1755919.05901099
    )
    model: str = Field(
        ...,
        description="Forecasting model used to generate the prediction",
        example="SARIMA"
    )


class PredictionResponse(BaseModel):
    n_stores: int = Field(
        ...,
        description="Total number of stores included in the forecast",
        example=45
    )
    horizon: int = Field(
        ...,
        description="Number of future weeks forecasted",
        example=12
    )
    forecast: list[ForecastItem] = Field(
        ...,
        description="List of generated forecasts grouped by store and week"
    )


class MetricItem(BaseModel):
    unique_id: int = Field(
        ...,
        description="Unique store identifier",
        example=1
    )
    metric: str = Field(
        ...,
        description="Error metric name (e.g., MAE, RMSE)",
        example="mae"
    )
    model: str = Field(
        ...,
        description="Forecasting model evaluated",
        example="SARIMA"
    )
    value: float = Field(
        ...,
        description="Metric value for the specified store and model",
        example=46569.4415023014
    )


class AvgMetricItem(BaseModel):
    metric: str = Field(
        ...,
        description="Error metric name (e.g., MAE, RMSE)",
        example="mae"
    )
    model: str = Field(
        ...,
        description="Forecasting model evaluated",
        example="ARIMA"
    )
    value: float = Field(
        ...,
        description="Average metric value across all stores",
        example=31019.8690414156
    )


class AvgMetrics(BaseModel):
    ARIMA: list[AvgMetricItem] = Field(
        ...,
        description="Average error metrics for the ARIMA model"
    )
    SARIMA: list[AvgMetricItem] = Field(
        ...,
        description="Average error metrics for the SARIMA model"
    )


class MetricsResponse(BaseModel):
    metrics: list[MetricItem] = Field(
        ...,
        description="Store-level error metrics for each forecasting model"
    )
    avg_metrics: AvgMetrics = Field(
        ...,
        description="Aggregated average error metrics grouped by model"
    )