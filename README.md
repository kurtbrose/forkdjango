This doesn't work!  Do not use!

I'm only leaving this around as an example to others.

If you need this functionality your options seem to be:
1) spawn a thread / green-thread
2) use something heavy-weight like Celery

forkdjango
==========

light-weight django job forker

Interestingly, somethign to do with forking causes both the parent and child process to be waited on before the response is completed.  This results in the test.py generating output like this:

started job result-fork-django-job#62a2639a5ab6421e88529fc16c2a3725HTTP/1.0 500 INTERNAL SERVER ERROR Date: Mon, 13 Aug 2012 18:55:41 GMT Server: WSGIServer/0.1 Python/2.6.4 Content-Type: text/plain Content-Length: 908 Traceback (most recent call last): File "/x/opt/pp/lib/python2.6/site-packages/django/core/servers/basehttp.py", line 283, in run self.result = application(self.environ, self.start_response) File "/x/opt/pp/lib/python2.6/site-packages/django/contrib/staticfiles/handlers.py", line 68, in __call__ return self.application(environ, start_response) File "/x/opt/pp/lib/python2.6/site-packages/django/core/handlers/wsgi.py", line 272, in __call__ response = self.get_response(request) File "/x/opt/pp/lib/python2.6/site-packages/django/core/handlers/base.py", line 111, in get_response response = callback(request, *callback_args, **callback_kwargs) File "/x/home-new/kurose/forkdjango/test.py", line 30, in start_job status_key, result_key = forkdjango.start_job(job) File "/x/home-new/kurose/forkdjango/forkdjango.py", line 35, in start_job sys.exit(0) SystemExit: 0

That is, the parent process runs to completion, and its response is sent.  Then, when the child process exits, the stack trace of the SystemExit exception is appended on to the response.  The HTTP transaction is not completed while the child process still runs.

