import re
import asyncio
import aiohttp

CONCURRENT_REQUESTS = 3
headers = {
    "Host": "t.cn",
    "User-Agent": "Mozilla/5.0 (Linux; U; Android 4.4.4; Nexus 5 Build/KTU84P) AppleWebkit/534.30 "
                  "(KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "deflate",
    "Connection": "close",
    "Upgrade-Insecure-Requests": "1"
}

#fail_dir = '/home/zpoint/Desktop/fail.txt'
#succ_dir = '/home/zpoint/Desktop/succ.txt'
fail_dir = 'fail.txt'
succ_dir = 'succ.txt'
err_url = []
succ_url = []

def get_http_address():
    rgx = re.compile("(https*://.+?) ")
    result_list = []
    with open(fail_dir, 'r') as f:
        lines = f.readlines()
    for line in lines:
        r = re.match(rgx, line)
        if r:
            result_list.append(r.group(1))
    return result_list


async def fetch(client, semaphore, url, retry=1):
    if retry > 5:
        err_url.append(url)
        return
    try:
        with await semaphore:
            with aiohttp.Timeout(20):
                print("geting url: ", url, retry, "times")
                response = await client.get(url, headers=headers)
                async with response:
                    if response.status != 200:
                        print("Error", url, "in", retry, "times", response.status)
                        return await fetch(client, semaphore, url, retry+1)

                    print("Success", url)
                    text = await  response.text()
                    rgx = re.compile(r".+?video=\['(.+?)'\]", re.DOTALL)
                    result = re.match(rgx, text)
                    succ_url.append("http://zxfuli.h6080.com" + result.group(1))
                    """
                    print(type(response.headers))
                    print(response.status)
                    print(type(response.status))
                    print(response.headers['Content-Type'])
                    print(await response.text())
                    """
    except asyncio.TimeoutError:
        print(url, "Conntection time out", retry, "times")
        return await fetch(client, semaphore, url, retry+1)

async def fetch_all(loop, client, semaphore):
    url_list = get_http_address()
    test_list = url_list[:5]
    task_list = [loop.create_task(fetch(client, semaphore, url)) for url in test_list]
    await asyncio.wait(task_list)

    with open(succ_dir, "a+") as f:
        for url in succ_url:
            f.write(url + "\n")
    with open(fail_dir, "w") as f:
        for url in err_url:
            f.write(url + "\n")


if __name__ == "__main__":
    semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)
    loop = asyncio.get_event_loop()
    with aiohttp.ClientSession(loop=loop) as client:
        loop.run_until_complete(fetch_all(loop, client, semaphore))

