from minio import Minio
from dotenv import load_dotenv
import os


load_dotenv()  # load .env file

# where the desired file is located, as in folder
LOCAL_FILE_PATH = os.environ.get('LOCAL_FILE_PATH')
# file name
LOCAL_FILE_NAME = os.environ.get('LOCAL_FILE_NAME')
# username
MINIO_ROOT_USER = os.environ.get('MINIO_ROOT_USER')
# password
MINIO_ROOT_PASSWORD = os.environ.get('MINIO_ROOT_PASSWORD')
# bucket name in min.io
MINIO_BUCKET_NAME = os.environ.get('MINIO_BUCKET_NAME')

# min.io initialize
MINIO_CLIENT = Minio("minio:9000", access_key=MINIO_ROOT_USER, secret_key=MINIO_ROOT_PASSWORD, secure=False)

# -----------------------------
# found checking actually isn't required since this bucked is created by another compose service
# but still just to be safe
found = MINIO_CLIENT.bucket_exists(MINIO_BUCKET_NAME)
if not found:
    MINIO_CLIENT.make_bucket(MINIO_BUCKET_NAME)
else:
    print("Bucket already exists")
# -----------------------------

try:
    # upload file to min.io
    MINIO_CLIENT.fput_object(
        MINIO_BUCKET_NAME,  # bucket name
        LOCAL_FILE_NAME,  # destination file name
        LOCAL_FILE_PATH + LOCAL_FILE_NAME,  # source file path
    )

    # closure
    print(f"File {LOCAL_FILE_NAME} successfully uploaded.")

except FileNotFoundError:
    # if file not found
    print("File not found. Check .env file and try again")
