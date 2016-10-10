import grequests
import string
import random

def generate_urls(base_url, num_urls):
    for i in range(num_urls):
        yield base_url + "".join(random.sample(string.ascii_lowercase, 10))

def run_experiment(base_url, num_iter = 500):
    urls = generate_urls(base_url, num_iter)
    response_futures = (grequests.get(u) for u in urls)
    responses = grequests.imap(response_futures, size = 100)
    response_size = sum(len(r.text) for r in responses)
    return response_size

def test(delay = 100, num_iter = 500):
    import time
    base_url = "http://localhost/add.php?name=zpoint&delay={}&".format(delay)
    start = time.time()
    result = run_experiment(base_url, num_iter)
    end = time.time()
    print ("Result: {}, Time: {}".format(result, end -start))

if __name__ == "__mian__":
    test()
