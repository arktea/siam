import json

from siam.router import process
import siam.endpoints # noqa


def handle(event, context):

    try:
        response = process(event)
        print(response)
    except Exception as e:
        raise e
        #response = str(e)

    return dict(
        statusCode=200,
        body=json.dumps(
            dict(
                message=response,
                path=event["path"],
                httpMethod=event["httpMethod"],
                pathParameter=event["pathParameters"],
                body=event["body"],
                queryStringParameters=event["queryStringParameters"]
            )
        )
    )
