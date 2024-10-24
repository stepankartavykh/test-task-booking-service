"""All config variables for project."""
import os
import subprocess
from pathlib import Path, PurePath

from dotenv import load_dotenv

load_dotenv()

_DATABASE_NAME = os.getenv('DATABASE_NAME')
_DATABASE_FOR_TESTING_NAME = os.getenv('TEST_DATABASE_NAME')

DEBUG = os.getenv('DEBUG') == 'True'
TESTING = os.getenv('TESTING') == 'True'

BASE_DIR = Path(os.path.abspath(__file__)).parent.parent.absolute()
DATABASE_PATH = PurePath(BASE_DIR, Path(_DATABASE_NAME))
TEST_DATABASE_PATH = PurePath(BASE_DIR, Path(_DATABASE_FOR_TESTING_NAME))

LOCAL_STORAGE_DIR = str(BASE_DIR) + '/storage'

command = ['openssl', 'rand', '-hex', '32']
command_result = subprocess.run(command,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)

SECRET_KEY = command_result.stdout.decode('utf-8').strip('\n')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
