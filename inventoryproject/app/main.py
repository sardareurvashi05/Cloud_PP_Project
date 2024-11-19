import logging
from business_logic.inventory_manager import check_inventory_and_notify
from config.settings import AWS_REGION

logging.basicConfig(level=logging.INFO)

def main():
    logging.info("Starting inventory management process...")

    # Example usage: Check and notify for itemA
    item = 'itemA'
    threshold = 10
    check_inventory_and_notify(item, threshold)

if __name__ == "__main__":
    main()
