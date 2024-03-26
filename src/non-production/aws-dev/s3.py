
import boto3
from logging.handlers import RotatingFileHandler

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

# Create a file handler to log errors
file_handler = RotatingFileHandler('accounting.log', maxBytes=10*1024*1024, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# upload logs to S3
class S3Handler(logging.StreamHandler):
    def __init__(self, bucket_name, folder, key):  # Update S3Handler to accept folder parameter
        super().__init__()
        self.bucket_name = bucket_name
        self.folder = folder  # Store folder name
        self.key = key
        self.s3_client = boto3.client('s3')

    def emit(self, record):
        log_entry = self.format(record) + '\n'
        self.upload_log(log_entry)

    def upload_log(self, log_entry):
        # Construct the full key including the folder
        full_key = f"{self.folder}/{self.key}"
        self.s3_client.put_object(Body=log_entry, Bucket=self.bucket_name, Key=full_key)

# Create an instance of the S3Handler with folder parameter
s3_handler = S3Handler(bucket_name=ACCOUNTING_LOG_BUCKET, folder=LOG_FOLDER, key='accounting.log')
s3_handler.setLevel(logging.ERROR)
logger.addHandler(s3_handler)

try:
except Exception as e:
            logger.error(f"Error processing message: {e}")
            pass
