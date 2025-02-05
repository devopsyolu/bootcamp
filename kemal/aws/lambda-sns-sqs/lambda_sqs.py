
import json

def lambda_handler(event, context):
    """
    This function is triggered automatically by SQS (event source mapping).
    It processes any messages that arrive in the queue.
    """
    # 'Records' key contains the SQS messages
    records = event.get("Records", [])

    print(f"Received {len(records)} messages from SQS.")

    for record in records:
        # The body of the SQS message
        body = record["body"]
        print(f"Message body: {body}")

        # If using an SNS subscription, the body itself may be a JSON string with an SNS structure.
        # For example, the actual message might be inside:
        #   json.loads(body)["Message"]
        # This depends on how the subscription is configured.

    return {"statusCode": 200}
