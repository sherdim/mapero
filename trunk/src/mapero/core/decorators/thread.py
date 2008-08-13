# Author: Zacarias F. Ojeda <zojeda@gmail.com>
# License: new BSD Style.

from threadec import ThreadPool, threadpool
from decorator import new_wrapper, decorator
from enthought.pyface.gui import GUI


pool = ThreadPool(10)
#
#@decorator
#@threadpool(pool)
#def process():

@decorator
def threaded_process(func, *args, **kw):
    pool.put((func, args, kw))
    return pool


@decorator
def invoke_later(func, *args, **kw):
    GUI.invoke_later(func, *args, **kw)
    return

