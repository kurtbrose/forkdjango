'''
Use start_job(func, args, kwargs) to spin off a separate process which will 
run func to completion.

start_job returns a globally unique key, which may be checked in django's
cache for the current status of the job.

func must return a pickle-able value, which will be stored in the cache
under the key after the function completes
'''
import sys
import os
import uuid
import thread

from django.core import cache

#forking doesn't work
def fork_job(func, args=(), kwargs=None):
    kwargs = kwargs or {}
    key = "fork-django-job#" + uuid.uuid4().hex
    status_key = "status-"+key
    result_key = "result-"+key
    cache.cache.set(status_key, "created")
    if os.fork():
        #parent
        return status_key, result_key
    #child
    cache.cache.set(status_key, "started")
    cache.cache.set(result_key, func(*args, **kwargs))
    cache.cache.set(status_key, "finished")
    sys.exit(0)

#threading does
def start_task(func, args=(), kwargs=None):
    kwargs = kwargs or {}
    key = "fork-django-job#" + uuid.uuid4().hex
    status_key = "status-"+key
    result_key = "result-"+key
    cache.cache.set(status_key, "created")
    def do_job():
        cache.cache.set(status_key, "started")
        cache.cache.set(result_key, func(*args, **kwargs))
        cache.cache.set(status_key, "finished")
    thread.start_new_thread(do_job, ())
    return status_key, result_key
