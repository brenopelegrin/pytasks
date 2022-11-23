import requests

import os
import time
import random
import string

interval = 0.001

api_url = os.getenv('API_URL')
request_count = 1
def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

while True:

    data = {
        "required_arg": get_random_string(16)
    }

    r = requests.post(url=api_url, json=data)
    print(r.json())
    time.sleep(interval)


