from  pybloom_live import ScalableBloomFilter as SBF
import re

# http_http 0
# http_https 1
# https_http 2
# https_https 3
num_0 = 0
num_1 = 0
num_2 = 0
num_3 = 0

def count(num):
    global num_0, num_1, num_2, num_3
    if num == 0:
        num_0 += 1
    elif num == 1:
        num_1 += 1
    elif num == 2:
        num_2 += 1
    elif num == 3:
        num_3 += 1
    else:
        pass


if __name__ == '__main__':

    # 初始化布隆函数
    bf_domain = SBF(mode=SBF.LARGE_SET_GROWTH)
    fp = open('login_url4.txt', 'r')
    r_line = fp.readline()
    while r_line:
        r_line = r_line.strip()
        if not len(r_line):
            continue
        # 处理字符串
        domain = re.search(r'(http|https)://(.*?)/.*', r_line)
        if domain.group(2) not in bf_domain:
            if 'sjtu' in domain.group(2):
                bf_domain.add(domain.group(2))
                result = r_line.split(', ')
                # print(result)
                r_tmp = 0
                if re.match(r'https://.*', result[1]):
                    r_tmp = r_tmp + 1
                if re.match(r'https://.*', result[0]):
                    r_tmp = r_tmp + 2
                count(r_tmp)
        r_line = fp.readline()
    print(num_0, num_1, num_2, num_3)
