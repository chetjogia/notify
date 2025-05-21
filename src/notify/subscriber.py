from google.cloud import pubsub_v1
import base64
import json
from google.oauth2 import service_account

project_id = "notify-459020"
subscription_id = "notify-sub-push"
credentials = service_account.Credentials.from_service_account_file("service-account.json")

subscriber = pubsub_v1.SubscriberClient(credentials=credentials)
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message):
    print("📥 Got Pub/Sub message:")
    print(f"Raw data: {message.data}")
    try:
        decoded = json.loads(base64.b64decode(message.data).decode("utf-8"))
        print("🔍 Decoded:", decoded)
    except Exception as e:
        print("⚠️ Could not decode:", e)
    message.ack()

future = subscriber.subscribe(subscription_path, callback=callback)
print(f"✅ Subscription started: {subscription_path}")

try:
    future.result()
except KeyboardInterrupt:
    print("🛑 Stopping subscriber...")
    future.cancel()
except Exception as e:
    print(f"❌ Error while listening: {e}")