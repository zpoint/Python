import os
import copy
import logging
import traceback
import threading
import requests
import tldextract
from scrapy_img_dev.urls import urls

origin_headers = {
    "Host": "www.poliform.it",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:76.0) Gecko/20100101 Firefox/76.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Cookie": "_ga=GA1.2.958985166.1589539318",
    "Upgrade-Insecure-Requests": "Upgrade-Insecure-Requests",

}

file_map = dict()
file_map_lock = threading.Lock()
for url in urls:
    result = tldextract.extract(url)
    domain = result.domain
    suffix = result.suffix
    real_domain = domain+"."+suffix
    file_map[real_domain] = open(domain + ".txt", "r")


def get_url_getter(domain_full):
    for line in file_map[domain_full]:
        yield line.strip()


def real_domain_getter_func():
    for key in file_map.keys():
        yield key


real_domain_getter = real_domain_getter_func()


def per_file_thread():
    while True:
        try:
            file_map_lock.acquire()
            real_domain = next(real_domain_getter)
            file_map_lock.release()
        except StopIteration:
            file_map_lock.release()
            logging.error(traceback.format_exc())
            return

        url_getter = get_url_getter(real_domain)
        lock = threading.Lock()
        thread_num = 3
        base_dir = "./%s/" % (real_domain, )
        if not os.path.exists(base_dir):
            os.mkdir(base_dir)
        exists_set = os.listdir(base_dir)
        headers = copy.deepcopy(origin_headers)
        headers["Host"] = real_domain
        logging.warning("starting %d thread for real_domain: %s, base_dir: %s" % (thread_num, real_domain, base_dir))
        threads = list()
        for i in range(thread_num):
            x = threading.Thread(target=downloader, args=(url_getter, base_dir, exists_set, headers, lock))
            x.start()
            threads.append(x)
        for t in threads:
            t.join()
        logging.warning("Done for real_domain: %s, base_dir: %s" % (real_domain, base_dir))


def downloader(url_getter, base_dir, exists_set, headers, lock):
    while True:
        try:
            lock.acquire()
            url = next(url_getter)
            lock.release()
        except StopIteration:
            lock.release()
            logging.error(traceback.format_exc())
            return
        file_name = url.split("/")[-1]
        if file_name in exists_set:
            continue
        r = requests.get(url, headers=headers)
        logging.info(url)
        with open(base_dir + file_name, "wb") as f:
            f.write(r.content)


if __name__ == "__main__":
    threads = list()
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    logging.info("Main    : before creating thread")
    for i in range(5):
        x = threading.Thread(target=per_file_thread)
        x.start()
        threads.append(x)
    logging.info("Main    : wait for the thread to finish")
    for t in threads:
        t.join()
    logging.info("Main    : all done")
