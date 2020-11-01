import json


def handle(event, context):
    return dict(
        statusCode=200,
        body=json.dumps(
            dict(
                path=event["path"],
                httpMethod=event["httpMethod"],
                pathParameter=event["pathParameters"],
                body=event["body"],
                queryStringParameters=event["queryStringParameters"]
            )
        )
    )
