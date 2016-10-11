import asyncio
import random
import string
import aiohttp
import random
import time
connector = aiohttp.TCPConnector(verify_ssl=False)
total_num = 20000
current_num = 16852

def generate_urls(base_url, num_urls):
    for i in range(num_urls):
        yield base_url + str(random.random())

def chunked_http_client(num_chunks):
    semaphore = asyncio.Semaphore(num_chunks) #semaphore is the max limit of workers
    @asyncio.coroutine
    def http_get(url):
        nonlocal semaphore
        with (yield from semaphore):
            response = yield from aiohttp.request('GET', url, connector=connector)
            body = yield from response.content.read()
            yield from response.wait_for_close()
        return body
    return http_get

def run_experiment(base_url, num_iter=total_num):
    urls = generate_urls(base_url, num_iter)
    http_client = chunked_http_client(800)
    tasks = [http_client(url) for url in urls]
    print("len(tasks): ", len(tasks))
    #responses_sum = 0
    i = current_num
    t1 = time.time()
    for future in asyncio.as_completed(tasks):
        data = yield from future
        f = open("12306/init_jpg/%d.jpg" % i, "wb")
        f.write(data)
        f.close()        
        i += 1
        if i % 100 == 0:
            print("%d solved, %d rest cost %f seconds" % (i + 1, total_num - (i + 1), time.time() - t1))
            t1 = time.time()
        #responses_sum += len(data)
    connector.close()
    print("connector closed")
    return i

def test(num_iter=total_num - current_num):
    import time
    base_url = "https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=login&rand=sjrand&"
    loop = asyncio.get_event_loop()
    start = time.time()
    result = loop.run_until_complete(run_experiment(base_url, num_iter))
    end = time.time()
    print("cost {} seconds".format( end - start))


if __name__ == "__main__":
    test()
