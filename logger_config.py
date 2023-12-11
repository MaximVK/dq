import logging

# Configure the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a console handler and set the formatter
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
