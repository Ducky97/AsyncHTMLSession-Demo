# coding: utf-8

from requests_html import AsyncHTMLSession
from urllib.parse import unquote
import aiofiles
import asyncio
import json
import time
import re
import logging
from  pybloom_live import ScalableBloomFilter as SBF

a = 1
file_name = ""
global bf_file
global bf_ready

def Extractor(url):
    str = url.strip().split("?", 1)
    return str[0]

async def wrt(url):
    global bf_file
    if not url in bf_file:
        bf_file.add(url)
        async with aiofiles.open("login_url.txt", 'a+') as afp:
            await afp.write(url + "\n")

async def finding(url, r):
    try:
        pq = r.html.pq
        pd_ele = pq.find("input[type='password']")
        ancestor_ele = pd_ele.closest('form')
        if ancestor_ele:
            print(url, ":", r.html.url)
            print("Extractor:", Extractor(r.html.url))
            await wrt(r.html.url)
    except Exception as e:
        print(e)
        logging.error(e)


async def check(url, r):
    global bf_ready
    try:
        await finding(url, r)
    except:
        pass
    for i in r.html.absolute_links:
        if not Extractor(i) in  bf_ready:
            # print("checking:", i)
            bf_ready.add(Extractor(i))
            # print(Extractor(i))
            try:
                asession = AsyncHTMLSession()
                r_ = await  asession.get(i)
                time.sleep(2)
                await finding(url, r_)
            except:
                pass


async def spider(url_s, len_):
    global a
    print(a, "/", len_, ":", url_s)
    a = a + 1
    if not Extractor(url_s) in bf_ready:
        # print("checking: ", url_s)
        bf_ready.add(Extractor(url_s))
        # print(Extractor(url_s))
        try:
            asession = AsyncHTMLSession()
            r = await asession.get(url_s)
            time.sleep(2)
            await check(url_s, r)
        except Exception as e:
            print(e)
            logging.error(e)
    a = a - 1
    print(a)


def test(f_json):
    for key in f_json:

        if re.match(r'http_only', key):
            len_ = len(f_json['http_only'])
            loop = asyncio.get_event_loop()
            cor = [spider("http://"+i, len_) for i in f_json["http_only"]]
            loop.run_until_complete(asyncio.gather(*cor))
        elif re.match(r'https_only', key):
            len_ = len(f_json['https_only'])
            loop = asyncio.get_event_loop()
            cor = [spider("https://" + i, len_) for i in f_json["https_only"]]
            loop.run_until_complete(asyncio.gather(*cor))
        elif re.match(r'https_default', key):
            len_ = len(f_json['https_default'])
            loop = asyncio.get_event_loop()
            cor = [spider("https://" + i, len_) for i in f_json["https_default"]]
            loop.run_until_complete(asyncio.gather(*cor))
        elif re.match(r'https_reachable', key):
            len_ = len(f_json['https_reachable'])
            loop = asyncio.get_event_loop()
            cor = [spider("https://"+i, len_) for i in f_json["https_reachable"]]
            loop.run_until_complete(asyncio.gather(*cor))
        else:
            continue

def main():
    global file_name
    file_name = input("input the test name: ")
    with open(file_name, 'r') as f:
        f_json = json.load(f)

    len_tmp = len(f_json["http_only"]) + len(f_json["https_only"]) + len(f_json["https_default"]) + len(f_json["https_reachable"])

    # 初始化布隆参数
    global bf_file, bf_ready
    bf_file = SBF(initial_capacity=len_tmp, error_rate=0.001, mode=SBF.LARGE_SET_GROWTH)
    bf_ready = SBF(initial_capacity=len_tmp*50, error_rate=0.001, mode=SBF.LARGE_SET_GROWTH)
    # bf_file = bloom.BloomFilter(error_rate = 0.001, element_num = len_tmp )
    # bf_ready = bloompy.BloomFilter(error_rate = 0.001, element_num = len_tmp*50)
    # 开始测试
    test(f_json)


if __name__ == '__main__':
    logging.basicConfig(filename="error.log", level=logging.DEBUG)
    start_time = time.time()
    main()
    print('Use time:{:.2f}s'.format(time.time() - start_time))