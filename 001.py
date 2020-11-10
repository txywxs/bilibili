import requests
import os
from lxml import etree
import re

# 1.确认url
url = 'https://www.bilibili.com/video/BV1k54y1r79P?spm_id_from=333.851.b_7265706f7274466972737431.8'
# 2.设置用户代理,Cookie
headers_ = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/84.0.4147.125 Safari/537.36',
    'cookie': "_uuid=A10E1109-5230-332F-7889-E7B566296C0477565infoc; "
              "buvid3=DEF33546-B6AC-4C64-92F3-6A2E0F335F58138394infoc; CURRENT_FNVAL=80; blackside_state=1; rpdid=|("
              "umk)kmkYkl0J'uY||YmR~uY; LIVE_BUVID=AUTO8816007671860767; CURRENT_QUALITY=16; PVID=1; "
              "bsource=search_baidu "
}

# 3.发送请求，得到响应对象
response_ = requests.get(url=url, headers=headers_)
print("------1-------")
str_data = response_.text  # 视频主页的html代码，类型是字符串
print("------2-------")
# 4.使用xpath解析html代码，得到想要的url

html_obj = etree.HTML(str_data)
print("------3-------")
# 获取视频的名称
title = html_obj.xpath("//span[@class='tit']/text()")
print(title)

# 如果视频的名称有特殊字符会影响
# 将视频名字里面的特殊字符全部替换为空
title_ = title.replace('/', '')
title = title.replace(' ', '')
title = title.replace('&', '')
title = title.replace('×', '')



