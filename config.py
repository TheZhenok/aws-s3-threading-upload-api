from utils import get_environ_variable
import logging


# -------------------------
# SERVER
# 
SERVER_HOST = get_environ_variable('SERVER_HOST')
SERVER_PORT = get_environ_variable('SERVER_PORT')
SERVER_DEBUG = get_environ_variable('SERVER_DEBUG')

# -------------------------
# AWS S3 credentials.
# 
S3_ACCESS_KEY = get_environ_variable('S3_ACCESS_KEY')
S3_SECRET_KEY = get_environ_variable('S3_SECRET_KEY')
S3_BUCKET_NAME = get_environ_variable('S3_BUCKET_NAME')

# -------------------------
# LOGGER
# 
logger = logging.getLogger()
logging.getLogger('boto3').setLevel('WARNING')
logging.getLogger('botocore').setLevel('WARNING')
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s %(message)s')

# -------------------------
# FILE UPLOAD CONFIG
# 
MAX_ATTEMPTS_UPLOAD_TO_S3 = 5
COUNT_MB_PER_PART_OF_THE_FILE = 30
COUNT_THREADS = 10

