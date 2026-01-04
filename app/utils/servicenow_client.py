import requests
from flask import current_app


def create_incident(payload):
    url = f"{current_app.config['SERVICENOW_INSTANCE']}/api/now/table/incident"

    response = requests.post(
        url,
        auth=(
            current_app.config["SERVICENOW_USER"],
            current_app.config["SERVICENOW_PASSWORD"],
        ),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        json=payload,
        timeout=30
    )

    response.raise_for_status()
    return response.json()
