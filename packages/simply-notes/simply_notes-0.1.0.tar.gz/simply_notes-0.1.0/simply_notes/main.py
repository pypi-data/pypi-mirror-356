from flask import Flask
from waitress import serve
from os import getenv
import logging

import logging

def get_port() -> str:
    portStr =  getenv("PORT", '5000')
    return int(portStr)

def setup_logging(module_name: str = __name__, log_level = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(module_name)
    logger.setLevel(log_level)

    if not logger.hasHandlers():
        # Create a console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)

        # Create a formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Add the formatter to the console handler
        console_handler.setFormatter(formatter)

        # Add the console handler to the logger
        logger.addHandler(console_handler)
        return logger

app = Flask(__name__)

@app.route('/')
def hello():
    return """<h1>Hello, world!</h1>
    <p> Click here to create a custom report </p>
    <p> And click here to access the ChatBot </p>
    """

def main():
    logger = setup_logging()
    port = get_port()
    logger.info(f"Started serving on port {port}")
    serve(app, host='0.0.0.0', port=port)

if __name__ == '__main__':
    main()