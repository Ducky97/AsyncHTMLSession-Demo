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
global bf_ready
global bf_file

def Extractor(url):
    str = url.strip().split("?", 1)
    return str[0]

async def wrt(url, act):
    global bf_file
    if url not in bf_file:
        bf_file.add(url)
        async with aiofiles.open("login_url.txt", 'a+') as afp:
            print("find! ", url, "action", act)
            await afp.write(url + "\t" + act + "\n")

async def finding(url, r):
    try:
        pq = r.html.pq
        pd_ele = pq.find("input[type='password']")
        ancestor_ele = pd_ele.closest('form')
        if ancestor_ele:
            act = ""
            try:
                act = ancestor_ele.attr['action']
            except:
                pass
            await wrt(r.html.url, act)
    except Exception as e:
        print(e)
        logging.error(e)


async def check(url, r):
    global bf_ready
    try:
        if not Extractor(r.html.url) in bf_ready:
            bf_ready.add(Extractor(r.html.url))
            await finding(url, r)
            await r.html.arender
            await finding(url, r)
    except:
        pass
    for i in r.html.absolute_links:
        if not Extractor(i) in bf_ready:
            bf_ready.add(Extractor(i))
            try:
                asession = AsyncHTMLSession()
                r_ = await  asession.get(i)
                # time.sleep(2)
                if Extractor(r_.html.url) not in bf_ready:
                    bf_ready.add(Extractor(r_.html.url))
                    await finding(url, r_)
                    await r_.html.arender
                    await finding(url, r_)
            except:
                pass

async def spider(url_s, len_):
    global a, bf_ready
    print(a, "/", len_, ":", url_s)
    a = a + 1
    if not Extractor(url_s) in bf_ready:
        bf_ready.add(Extractor(url_s))
        try:
            asession = AsyncHTMLSession()
            r = await asession.get(url_s)
            # time.sleep(2)
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
    file_name = input("input the test name: ")
    with open(file_name, 'r') as f:
        f_json = json.load(f)

    len_tmp = len(f_json["http_only"]) + len(f_json["https_only"]) + len(f_json["https_default"]) + len(f_json["https_reachable"])

    # 初始化布隆参数
    global bf_ready
    global bf_file
    bf_ready = SBF(initial_capacity=len_tmp*50, error_rate=0.001, mode=SBF.LARGE_SET_GROWTH)
    bf_file = SBF(initial_capacity=len_tmp*50, error_rate=0.001, mode=SBF.LARGE_SET_GROWTH)
    # bf_file = bloom.BloomFilter(error_rate = 0.001, element_num = len_tmp )
    # bf_ready = bloompy.BloomFilter(error_rate = 0.001, element_num = len_tmp*50)
    # 开始测试
    test(f_json)


if __name__ == '__main__':
    logging.basicConfig(filename="error.log", level=logging.DEBUG)
    start_time = time.time()
    main()
    print('Use time:{:.2f}s'.format(time.time() - start_time))