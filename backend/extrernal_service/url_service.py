from rest_framework import status
import requests
import time


BASE_URL = "http://url:8001/"


def get_short_url(full_url):
    res_data = None
    response = requests.post(f"{BASE_URL}api/", data={"full_url": full_url})
    if response.status_code == status.HTTP_201_CREATED:
        res_data = response.json()
    return res_data


def delete_url_obj(full_url):
    response = requests.post(f"{BASE_URL}api/delete", data={"full_url": full_url})
    if not response.status_code == status.HTTP_204_NO_CONTENT:
        raise Exception('Can\'t delete a url object')


# MAX_RETRIES = 5
# SLEEP_TIME = 2
# BASE_URL = "http://url:8001/"

# def get_short_url(full_url):
#     attempt_num = MAX_RETRIES
#     while attempt_num:
#         response = requests.post(f"{BASE_URL}api/", data={"full_url": full_url})
#         if response.status_code == status.HTTP_201_CREATED:
#             data = response.json()
#             return data
#         attempt_num -= 1
#         time.sleep(SLEEP_TIME)
#     return None


# def delete_url_obj(full_url):
#     attempt_num = MAX_RETRIES
#     while attempt_num:
#         response = requests.post(f"{BASE_URL}api/delete", data={"full_url": full_url})
#         if response.status_code == status.HTTP_204_NO_CONTENT:
#             break
#         attempt_num -= 1
#         time.sleep(SLEEP_TIME)
#     else:
#         raise Exception('Can\'t delete a url object')
