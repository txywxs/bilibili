import requests
import os
from lxml import etree
import re

# 1.确认url
url = '' \
      'https://www.bilibili.com/video/BV1LA411J77w/'
# 2.设置用户代理,Cookie
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/84.0.4147.125 Safari/537.36',
    'cookie': "_uuid=A10E1109-5230-332F-7889-E7B566296C0477565infoc; "
              "buvid3=DEF33546-B6AC-4C64-92F3-6A2E0F335F58138394infoc; CURRENT_FNVAL=80; blackside_state=1; rpdid=|("
              "umk)kmkYkl0J'uY||YmR~uY; LIVE_BUVID=AUTO8816007671860767; CURRENT_QUALITY=16; PVID=1; "
              "bsource=search_baidu "
}


# 3.发送请求，得到响应对象
response_ = requests.get(url=url, headers=headers)
print("------1-------")
str_data = response_.text  # 视频主页的html代码，类型是字符串
print("------2-------")
# 4.使用xpath解析html代码，得到想要的url

html_obj = etree.HTML(str_data)
print("------3-------")
# 获取视频的名称
title = html_obj.xpath("//span[@class='tit']/text()")[0]
vid_aud = html_obj.xpath('//script[contains(text(),"window.__playinfo__")]/text()')[0]
print(title)

# 如果视频的名称有特殊字符会影响
# 将视频名字里面的特殊字符全部替换为空
title = title.replace('/', '')
title = title.replace(' ', '')
title = title.replace('&', '')
title = title.replace('×', '')


# 获取到视频的播放地址
mp4_video = re.findall(r'"video":\[{"id":\d+,"baseUrl":"(.*?)"',vid_aud)[0]

# 获取到视频音频
mp3_audio = re.findall(r'"audio":\[{"id":\d+,"baseUrl":"(.*?)"',vid_aud)[0]
print(mp3_audio)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/84.0.4147.125 Safari/537.36',
    'Referer': url
}
# 请求视频地址
headers_video = requests.get(url=mp4_video,headers=headers,stream=True)
# 请求音频地址
headers_audio = requests.get(url=mp3_audio,headers=headers,stream=True)
inc = 0
with open('./%s.mp4'%title, 'wb') as headers_videos:
    # 流下载，比起直接content，iter_content 一次只让requests.get获取chunk_size大小的内容，
    # 等到下载的内容存入文件后，再让requests.get获取后面的
    for chunk in headers_video.iter_content(chunk_size=10000):# iter_content是一个可迭代对象
        inc += 1000/int(headers_video.headers.get("content-length"))
        print("视频下载了%0.2f"%(inc*1000))
        headers_videos.write(chunk)

inc = 0
with open('./%s.mp3'%title, 'wb') as headers_audios:
    # 流下载，比起直接content，iter_content 一次只让requests.get获取chunk_size大小的内容，
    # 等到下载的内容存入文件后，再让requests.get获取后面的

    for chunk in headers_audio.iter_content(chunk_size=1000):  # iter_content是一个可迭代对象
        inc += 1000 / int(headers_audio.headers.get("content-length"))
        print("音频下载了%0.2f" % (inc * 100))
        headers_audios.write(chunk)
