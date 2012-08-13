from os import path as osp
def rel_path(*p): return osp.normpath(osp.join(rel_path.path, *p))
rel_path.path = osp.abspath(osp.dirname(__file__))
this = osp.splitext(osp.basename(__file__))[0]
 
from django.conf import settings
SETTINGS = dict(
    DATABASES = {},
    DEBUG=True,
    TEMPLATE_DEBUG=True,
    ROOT_URLCONF = this, #current file
    CACHE_BACKEND = "locmem://",
    SESSION_ENGINE = "django.contrib.sessions.backends.cache",
)

if __name__=='__main__':
    settings.configure(**SETTINGS)

import forkdjango

from django.conf.urls.defaults import patterns
from django.http import HttpResponse

def start_job(request):
    def job():
        import time, random
        time.sleep(10 + 10*random.random())
        return "beep-boop-beep " + str(time.time())

    status_key, result_key = forkdjango.start_job(job)
    request.session.setdefault('keys', []).append( (status_key, result_key) )
    return HttpResponse("started job "+result_key)

def check_jobs(request):
    from django.core.cache import cache
    html = ["<html><head></head><body><table><tr><th>id</th><th>status</th><th>result</th></tr>"]
    for status_key, result_key in request.session.get('keys', []):
        html.append("<tr><td>"+status_key+"</td><td>"+cache.get(status_key)+\
                     "</td><td>"+str(cache.get(result_key))+"</td></tr>")
    html.append("</table></body></html")
    return HttpResponse("".join(html))

urlpatterns = patterns('', 
    (r'^start_job$', start_job), 
    (r'^check_jobs$', check_jobs))

if __name__ == '__main__':
    from django.core import management
    management.execute_from_command_line()
