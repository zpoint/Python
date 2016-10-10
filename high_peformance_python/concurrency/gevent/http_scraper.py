import requests
import string
import random

def generate_urls(base_url, num_urls):
    for i in range(num_urls):
        yield base_url + "".join(random.sample(string.ascii_lowercase, 10))

def run_experiment(base_url, num_iter = 500):
    response_size = 0
    for url in generate_urls(base_url, num_iter):
        response = requests.get(url)
        response_size += len(response.text)
    return response_size

def test(num_iter = 500, delay = 100):
    import time
    base_url = "http://localhost/add.php?name=zpoint&delay={}&".format(delay)

    start = time.time()
    result = run_experiment(base_url, num_iter)
    end = time.time()
    print ("Result: {}, Time: {}".format(result, end - start))

if __name__ == "__main__":
    test()
