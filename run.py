import logging
from logging import handlers
import os

from app import app

# init log files
if not os.path.exists('logs'):
    os.makedirs('logs')
handler = logging.handlers.TimedRotatingFileHandler(filename='logs/flask.log', when='midnight', backupCount=30, encoding='utf-8')
handler.setLevel(logging.DEBUG)
logging_format = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
handler.setFormatter(logging_format)
app.logger.addHandler(handler)

error_handler = logging.handlers.TimedRotatingFileHandler(filename='logs/flask_error.log', when='midnight', backupCount=30, encoding='utf-8')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging_format)
app.logger.addHandler(error_handler)

app.run(host='0.0.0.0', port=50000, threaded=True, debug=True)
