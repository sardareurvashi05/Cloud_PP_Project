from services.sns_service import create_sns_topic, publish_to_sns
from services.sqs_service import create_sqs_queue, send_message_to_sqs

def check_inventory_and_notify(item, threshold):
    inventory_level = get_inventory_level(item)  # Replace with actual DB/API call
    if inventory_level < threshold:
        message = f"Inventory alert: Low stock on {item}!"
        notify_inventory_event(message)

def notify_inventory_event(message):
    topic_arn = create_sns_topic('InventoryAlertTopic')
    if topic_arn:
        publish_to_sns(topic_arn, message, 'Low Inventory Alert')

    queue_url = create_sqs_queue('InventoryQueue')
    if queue_url:
        send_message_to_sqs(queue_url, message)

def get_inventory_level(item):
    inventory = {'itemA': 5, 'itemB': 2, 'itemC': 50}
    return inventory.get(item, 0)
