from dotenv import load_dotenv
import os

load_dotenv()

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS')[2:-2].replace(',', '').split("' '")
print(type(ALLOWED_HOSTS))

print(ALLOWED_HOSTS)
