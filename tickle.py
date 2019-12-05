from  pybloom_live import ScalableBloomFilter as SBF
import re
import json

# http_http 0
# http_https 1
# https_http 2
# https_https 3
# not_tickle = 4
num_0 = 0
num_1 = 0
num_2 = 0
num_3 = 0
num_4 = 0


def count(num, record):
    global num_0, num_1, num_2, num_3, num_4, d

    if num == 0:
        num_0 += 1
        d["http_http"].append(record)
        print("0")

    elif num == 1:
        num_1 += 1
        d["http_https"].append(record)
        print("1")

    elif num == 2:
        num_2 += 1
        d["https_http"].append(record)
        print("2")

    elif num == 3:
        num_3 += 1
        d["https_https"].append(record)
        print("3")

    elif num == 4:
        num_4 += 1
        d["not_classified"].append(record)
        print("4")
    else:
        pass


if __name__ == '__main__':
    global d
    d = dict()
    d["http_http"] = list()
    d["http_https"] = list()
    d["https_http"] = list()
    d["https_https"] = list()
    d["not_classified"] = list()

    file_name = input("input your file name: ")
    domain_ = file_name.strip().split('_')[0]

    # 初始化布隆函数
    bf_domain = SBF(mode=SBF.LARGE_SET_GROWTH)

    fp = open(file_name, 'r')
    r_line = fp.readline()

    while r_line:

        r_line = r_line.strip()
        if not len(r_line):
            continue
        # 处理字符串
        domain = re.search(r'(http|https)://(.*?)/.*', r_line)
        r_tmp = 4
        try:
            if domain.group(2) not in bf_domain or '\d+\.\d+\.\d+\.\d+' in domain.group(2)::
                bf_domain.add(domain.group(2))
                if domain_ in domain.group(2):
                    result = r_line.split(', ')
                    r_tmp = 0
                    if re.match(r'https://.*', result[1]):
                        r_tmp = r_tmp + 1
                    if re.match(r'https://.*', result[0]):
                        r_tmp = r_tmp + 2
                    count(r_tmp, r_line)
                else:
                    count(r_tmp, r_line)
            else:
                count(r_tmp, r_line)
        except:
            count(r_tmp, r_line)

        r_line = fp.readline()

    # 记录结果
    record_file_name = domain_ + '_' + 'login_' + 'classified' + '.txt'
    fr = open(record_file_name, 'w')
    json_str = json.dumps(d, indent=4)
    fr.write(json_str)
    print(d)
    print(num_0, num_1, num_2, num_3, num_4)
