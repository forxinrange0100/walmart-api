import pickle
import pandas as pd
from statsforecast import StatsForecast
from api.errors import InvalidDataError, NotFoundDataError

def make_predictions(models, horizon):
    total_preds = []
    for name, data in models.items():
        try:
            with open(data["path"], "rb") as model:
                models_statsforecast: StatsForecast = pickle.load(model)
            preds = models_statsforecast.predict(h=horizon)
            preds = preds.rename(columns={name: "sales"})
            preds["model"] = name
            preds = preds[preds["unique_id"].isin(data["unique_ids"])]
            total_preds.append(preds)
        except FileNotFoundError:
            raise NotFoundDataError(f"{data['path']} not found")
        except (pickle.UnpicklingError, EOFError):
            raise InvalidDataError(f"Invalid data: {data['path']}")
    total_preds = pd.concat(total_preds)
    total_preds = total_preds.sort_values(by=["unique_id", "ds"])
    total_preds["ds"] = total_preds["ds"].astype(str)
    result = total_preds.to_dict(orient="records")
    n_stores = total_preds["unique_id"].nunique()

    return {
        "n_stores": n_stores,
        "horizon": horizon, 
        "forecast": result
    }
