BOOKING_SCHEMA = {
    "type": "object",
    "properties": {
        "bookingid": {
            "type": "integer"
        },
        "booking": {
            "type": "object",
            "properties": {
                "firstname": {
                    "type": "string"
                },
                "lastname": {
                    "type": "string"
                },
                "totalprice": {
                    "type": "integer"
                },
                "depositpaid": {
                    "type": "boolean"
                },
                "bookingdates": {
                    "type": "object",
                    "required": ["checkin", "checkout"],
                    "properties": {
                        "checkin": {
                            "type": "string"
                        },
                        "checkout": {
                            "type": "string"
                        }
                    },
                    "additionalProperties": False
                },
                "additionalneeds": {
                    "type": "string"
                }
            },
            "required": ["firstname", "lastname", "totalprice", "depositpaid", "bookingdates"],
            "additionalProperties": False
        }
    },
    "required": ["bookingid", "booking"],
    "additionalProperties": False
}
