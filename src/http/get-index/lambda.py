import numpy as np
import json


def handler(event, context):
    x = np.arange(10)
    y = np.square(x)
    return {
        "statusCode": 200,
        "headers": {
            "content-type": "application/javascript",
        },
        "body": json.dumps({"hello": "world"}),
    }
