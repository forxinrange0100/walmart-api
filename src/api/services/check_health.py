from pathlib import Path
from api.errors import NotFoundDataError

def check_health(models):
    files = []
    for _, model in models.items():
        files.append(model["path"])
        files.append(model["metric_path"])
    for file in files:
        path = Path(file)
        if not path.is_file():
            raise NotFoundDataError(f"{path} not found")
    return {"status": "ok", "files": files}