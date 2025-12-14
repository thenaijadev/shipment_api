from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from scalar_fastapi import get_scalar_api_reference
from app.errors import ErrorTemplates

app = FastAPI()

shipments = {
    "123423": {
        "id": "123423",
        "weight": "20kg",
        "content": "Wooden Table",
        "status": "In Transit",
    },
    "123424": {
        "id": "123424",
        "weight": "20kg",
        "content": "Wooden Table",
        "status": "In Transit",
    },
    "123425": {
        "id": "123425",
        "weight": "20kg",
        "content": "Wooden Table",
        "status": "In Transit",
    },
}


@app.get("/shipment/latest")
def get_latest_shipment() -> dict[str, str]:
    id = max(shipments.keys())
    return shipments[id]


@app.get("/shipment/")
def get_shipment(request: Request, id: str | None = None):
    if not id:
        id = max(shipments.keys())

    if id not in shipments:
        error = ErrorTemplates.not_found(
            resource="Shipment", resource_id=id, instance=str(request.url)
        )
        return JSONResponse(status_code=404, content=error)
    return shipments[id]


@app.post("/shipment/")
def create_shipment(data: dict, request: Request):
    new_id = str(int(max(shipments.keys())) + 1)

    if data["weight"] < 0 or data["weight"] > 100:
        error = ErrorTemplates.bad_request(
            detail="Weight must be between 0 and 100", instance=str(request.url)
        )
        return JSONResponse(status_code=400, content=error)

    shipments[new_id] = {
        "id": new_id,
        "content": data["content"],
        "weight": str(data["weight"]) + "kg",
        "status": "In Transit",
    }

    return shipments[new_id]


@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API Reference",
    )
