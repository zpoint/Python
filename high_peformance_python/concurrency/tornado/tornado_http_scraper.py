import string
import random
from functools import partial
from tornado import ioloop, gen
from tornado.httpclient import AsyncHTTPClient

AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient",
                          max_clients=100)

def generate_urls(base_url, num_urls):
    for i in range(num_urls):
        yield base_url + "".join(random.sample(string.ascii_lowercase, 10))

@gen.coroutine
def run_experiment(base_url, num_iter=500):
    http_client = AsyncHTTPClient()
    urls = generate_urls(base_url, num_iter)
    responses = yield [http_client.fetch(url) for url in urls]
    response_sum = sum(len(r.body) for r in responses)
    raise gen.Return(value=response_sum)

def test(delay=100, num_iter=500):
    import time
    base_url = "http://localhost/add.php?name=guozp&delay={}&".format(delay)
    _ioloop = ioloop.IOLoop.instance()
    run_func = partial(run_experiment, base_url, num_iter)
    start_time = time.time()
    result = _ioloop.run_sync(run_func)
    end_time = time.time()
    print("Result: {}, Time: {}".format(result, end_time - start_time))

if __name__ == "__main__":
    test()
