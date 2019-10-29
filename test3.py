from requests_html import AsyncHTMLSession
import pymysql
import asyncio
import aiomysql
import json
import chardet
import re

async def check_login(r):
    try:
        pq = r.html.pq
        pd_ele = pq.find("input[type='password']")
        ancestor_ele = pd_ele.closest('form')
        if ancestor_ele
            print("find!!!!", r.html.url)
    except:
        pass

async def test_(r):
    # print(r.html.absolute_links)
    for i in r.html.absolute_links:
        asession = AsyncHTMLSession()
        r = await asession.get(i)
        await check_login(r)


async def spider(url):
    asession = AsyncHTMLSession()
    try:
        r = await asession.get(url)
        await test_(r)
        return r
    except Exception as e:
        print(e)

def test(f_json):
    for key in f_json:
        if re.match(r'http_only', key):
            print(f_json['http_only'])
            loop = asyncio.get_event_loop()
            cor = [spider("http://"+url) for url in f_json["http_only"]]
            result = loop.run_until_complete(asyncio.gather(*cor))
    print(result)
    '''
        if re.match(r'http_only', key):
            r['http_only'] = dict()
            initialize(r['http_only'])
            test(f_json[key], 'http', r['http_only'])
            for_json_record(r['http_only'])
            
        elif re.match(r'https_only', key):
            r['https_only'] = dict()
            initialize(r['https_only'])
            test(f_json[key], 'https', r['https_only'])
            for_json_record(r['https_only'])

        elif re.match(r'https_reachable', key):
            r['https_reachable'] = dict()
            initialize(r['https_reachable'])
            test(f_json[key], 'https', r['https_reachable'])
            for_json_record(r['https_reachable'])

        elif re.match(r'https_default', key):
            r['https_default'] = dict()
            initialize(r['https_default'])
            test(f_json[key], 'https', r['https_default'])
            for_json_record(r['https_default'])
        else:
            continue
        '''


def create_table_string(key):
    str = ""
    if re.match(r'http_only', key) or re.match(r'https_only', key) or re.match(r'https_reachable', key) or re.match(r'https_default', key):
        str = "CREATE TABLE IF NOT EXISTS " + key + " ( \
                Domain_hash BIGINT,\
                Domain TEXT,\
                IF_Login TINYINT UNIQUE, \
                PRIMARY KEY(Domain_hash))"
    return str

def init(f_json):
    # 创建所需的数据库和数据表
    # 创建连接
    conn = pymysql.connect(host='localhost', user='root', password='password', charset="utf8")
    # 创建游标
    cursor = conn.cursor()
    # 创建数据库sql（如果数据库存在就不创建，防止异常）
    sql = "CREATE DATABASE IF NOT EXISTS LOGIN_TEST;"
    cursor.execute(sql)

    # 创建表
    # 连接表
    cursor.execute("use LOGIN_TEST")

    # 创建login表
    sql = """CREATE TABLE IF NOT EXISTS login(
            URL_hash BIGINT,
            URL TEXT,
            Action TEXT,
            Domain TEXT,
            PRIMARY KEY(URL_hash));"""
    cursor.execute(sql)

    for  key in f_json:
        # 为http_only https_only https_default https_reachable建表
        sql = create_table_string(key)
        if len(sql):
            cursor.execute(sql)


def main():
    file_name = "sjtu.edu.cn.json"
    with open(file_name, 'r') as f:
        f_json = json.load(f)
        init(f_json)
    # 开始测试
    test(f_json)

if __name__=='__main__':
    print("hello")
    main()

