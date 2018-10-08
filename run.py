import logging

from app import app

handler = logging.FileHandler('flask.log')
logging_format = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
handler.setFormatter(logging_format)
app.logger.addHandler(handler)
app.run(host='0.0.0.0', port=50000, debug=True)
