# logging_config.py
import logging

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,  # You can change this to INFO or ERROR depending on your needs
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("audit_log.log"),  # Saves to a log file
            logging.StreamHandler()  # Also outputs to the console
        ]
    )