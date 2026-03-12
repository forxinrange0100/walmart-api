import pandas as pd
from api.errors import InvalidDataError, NotFoundDataError


def get_metrics(models):
    total_metrics = []
    avg_metrics = {}

    for name, data in models.items():
        try:
            metrics_df = pd.read_csv(data["metric_path"])
            metrics_df = metrics_df.rename(columns={name: "value"})
            metrics_df["model"] = name
            metrics_df = metrics_df[metrics_df["unique_id"].isin(data["unique_ids"])]
            total_metrics.append(metrics_df)
            avg_metrics[name] = metrics_df.groupby(["metric", "model"], as_index=False)["value"].mean().to_dict(orient="records")
        except FileNotFoundError:
            raise NotFoundDataError(f"{data['metric_path']} not found")
        except pd.errors.EmptyDataError:
            raise InvalidDataError(f"{data['metric_path']} is empty")
        except pd.errors.ParserError:
            raise InvalidDataError(f"Invalid Data {data['metric_path']}")
    total_metrics = (
        pd.concat(total_metrics)
        .groupby(["unique_id", "metric", "model"], as_index=False)["value"]
        .mean()
    )
    result = total_metrics.to_dict(orient="records")
    return {
        "metrics": result,
        "avg_metrics": avg_metrics
}
