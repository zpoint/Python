import random
import string
from functools import partial
from tornado import ioloop
from tornado.httpclient import AsyncHTTPClient

AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient", max_clients=100)

def fetch_urls(urls, callback):
    http_client = AsyncHTTPClient()
    urls = list(urls)
    responses = []
    def _finish_fetch_urls(result):
        responses.append(result)
        if len(responses) == len(urls):
            callback(responses)
    for url in urls:
        http_client.fetch(url, callback=_finish_fetch_urls)

def generate_urls(base_url, num_urls):
    for i in range(num_urls):
        yield base_url + "".join(random.sample(string.ascii_lowercase, 10))

def run_experiment(base_url, num_iter=500, callback=None):
    urls = generate_urls(base_url, num_iter)
    callback_passthru = partial(_finish_run_experiment, callback=callback)
    fetch_urls(urls, callback_passthru)

def _finish_run_experiment(responses, callback):
    response_sum = sum(len(r.body) for r in responses)
    print(response_sum)
    callback()

def test(delay=100, num_iter=500):
    import time
    base_url = "http://localhost/add.php?name=zpoingggg&delay={}&".format(delay)
    _ioloop = ioloop.IOLoop.instance()
    _ioloop.add_callback(run_experiment, base_url, num_iter, _ioloop.stop)
    start = time.time()
    _ioloop.start()
    end_time = time.time()
    print("Time: {}(may be not accurate)".format(end_time - start))

if __name__ == "__main__":
    test()
