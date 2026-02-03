from typing import List, Optional

def base_order_payload(colors: Optional[List[str]] = None) -> dict:
    payload = {
        "firstName": "Tony",
        "lastName": "QA",
        "address": "Moscow, Red Square 1",
        "metroStation": 4,
        "phone": "+79999999999",
        "rentTime": 5,
        "deliveryDate": "2026-02-03",
        "comment": "test order",
    }
    if colors is not None:
        payload["color"] = colors
    return payload
