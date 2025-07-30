import boto3
import json
from pydantic import BaseSettings

from datetime import datetime
import time


class Settings(BaseSettings):
    updates_sqs_queue_url: str
    updates_sqs_queue_region: str


def post_update(title: str, user_id: str):
    SETTINGS = Settings()

    result = None
    sqs_client = boto3.client("sqs", region_name=SETTINGS.updates_sqs_queue_region)

    response = sqs_client.send_message(
        QueueUrl=SETTINGS.updates_sqs_queue_url,
        MessageBody=title,
        MessageAttributes={
            key: {"StringValue": value, "DataType": "String"}
            for key, value in [
                ("user_id", user_id),
                ("date", str(int(time.mktime(datetime.now().timetuple())))),
            ]
        },
    )

    if response and "MessageId" in response:
        result = response.get("MessageId")

    return result


def get_update_message(message_id: str, language: str):
    result = None

    with open("source/data/updates.json", "r") as file:
        data = json.loads(file.read())

        if data:
            result = data.get(language, {}).get(message_id)

        file.close()

    return result


__all__ = ["post_update", "get_update_message"]
