import logging
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

print("hello")
logging.info("hello logs")
logger.info("hello logger")

if __name__ == "__main__":
	print("hello inside main")
	logging.info("hello logs from main")
	logger.info("hello logger from main")
	while True:
		logger.info("loop")

