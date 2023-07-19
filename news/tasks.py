from celery import shared_task
import time


@shared_task
def hello():
    time.sleep(10)
    print('Hi, my dear friend!')


@shared_task
def printing(N):
    for i in range(N):
        time.sleep(1)
        print(i+1)