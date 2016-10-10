from gevent import monkey
monkey.patch_socket()

import gevent
from gevent.coros import Semaphore
import urllib.request
import string
import random

def generate_urls(base_url, num_urls):
    for i in range(num_urls):
        yield base_url + "".join(random.sample(string.ascii_lowercase, 10))

def chunked_requests(urls, chunk_size = 100):
    #print ("chunked_request called")
    semaphore = Semaphore(chunk_size)
    requests = [gevent.spawn(download, u, semaphore) for u in urls]
    for response in gevent.iwait(requests):
        yield response

def download(url, semaphore):
    #print ("download called")
    with semaphore:
        data =urllib.request.urlopen(url)
        return data.read()

def run_experiment(base_url, num_iter = 500):
    urls = generate_urls(base_url, num_iter)
    response_futures = chunked_requests(urls, 100)
    response_szie = sum(len(r.value) for r in response_futures)
    return response_szie
"""
def l(r):
    print ("r in response_futures: r:", r)
    print ("r.value ", r.value)
    print ("len(r)", len(r))
    return len(r)
"""
def test(delay = 100, num_iter = 500):
    import time
    base_url = "http://localhost/add.php?name=zpoint&delay={}&".format(delay)
    start = time.time()
    result = run_experiment(base_url, num_iter)
    end = time.time()
    print ("Result: {}, Time: {}".format(result, end - start))

if __name__ == "__main__":
    test()
