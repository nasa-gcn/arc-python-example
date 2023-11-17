import json

import .foo


def handler(event, context):
    return {
        "statusCode": 200,
        "headers": {
            "content-type": "application/javascript",
        },
        "body": json.dumps(foo.bar()),
    }
