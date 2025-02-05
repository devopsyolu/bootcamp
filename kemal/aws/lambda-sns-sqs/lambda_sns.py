# Bu Lambda fonksiyonu, SNS topic'e mesaj yayınlamak için kullanılır.
# Bunun icin, SNS topic ARN ve SQS queue URL bilgileri gerekir.
# Bu bilgiler, Lambda fonksiyonunun environment variables kısmında tanımlanmalıdır.
# Test etmek için, aws'de lambda fonksiyonu açın ve python olarak bu kodu yapıştırın.
# Daha sonra, test kısmında bir event oluşturun ve test edin.
# Event örneği: { "message": "Hello from PublisherFunction!" }
# Çıktısını görmek için, CloudWatch log'lara bakın.

import json
import boto3
import os
sns_client = boto3.client('sns')

# Environment variables for SNS topic ARN
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']

def lambda_handler(event, context):
    """
    Publishes a message to SNS.
    This function is invoked manually from the Lambda console's "Test" section.
    """
    # 1. Get a message from the 'event', or default to something
    message = event.get("message", "Hello from PublisherFunction!")

    # 2. Publish the message to the SNS topic
    response = sns_client.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=json.dumps({"default": message})  # using 'default' message structure
    )

    # 3. Log some info
    print(f"Published message to SNS: {message}")
    print(f"SNS publish response: {response}")

    return {
        "statusCode": 200,
        "body": f"Message sent to SNS topic: {message}"
    }
