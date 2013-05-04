import os

from apscheduler.scheduler import Scheduler
import requests

sched = Scheduler()


@sched.interval_schedule(hours=6)
def timed_job():
    requests.post("http://0.0.0.0:"
                  + str(os.environ.get("PORT", 3000))
                  + "/iss/update_ephem")

sched.start()

while True:
    pass
