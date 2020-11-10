import re

import requests
from lxml import etree
import os


class a():
    def __init__(self, url):
        url = url
        headers_top = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/84.0.4147.125 Safari/537.36',
            'cookie': "_uuid=A10E1109-5230-332F-7889-E7B566296C0477565infoc; "
                      "buvid3=DEF33546-B6AC-4C64-92F3-6A2E0F335F58138394infoc; CURRENT_FNVAL=80; blackside_state=1; "
                      "rpdid=|( "
                      "umk)kmkYkl0J'uY||YmR~uY; LIVE_BUVID=AUTO8816007671860767; CURRENT_QUALITY=16; PVID=1; "
                      "bsource=search_baidu "
        }

        self.headers_buttom = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/84.0.4147.125 Safari/537.36',
            'Referer': url
        }
        # 3.发送请求，得到响应对象
        self.response = requests.get(url=url, headers=headers_top)
        str_data = self.response.text
        html_obj = etree.HTML(str_data)
        # 获取视频的名称
        title = html_obj.xpath("//span[@class='tit']/text()")[0]
        title = title.replace('/', '')
        title = title.replace(' ', '')
        title = title.replace('&', '')
        self.title = title.replace('×', '')
        self.vid_aud = html_obj.xpath('//script[contains(text(),"window.__playinfo__")]/text()')[0]

    def video(self):
        inc = 0
        # 获取到视频的播放地址
        mp4_video = re.findall(r'"video":\[{"id":\d+,"baseUrl":"(.*?)"', self.vid_aud)[0]

        # 获取到视频音频
        # mp3_audio = re.findall(r'"audio":\[{"id":\d+,"baseUrl":"(.*?)"', vid_aud)[0]
        headers_video = requests.get(url=mp4_video, headers=self.headers_buttom, stream=True)
        with open('./%s.mp4' % self.title, 'wb') as headers_videos:
            # 流下载，比起直接content，iter_content 一次只让requests.get获取chunk_size大小的内容，
            # 等到下载的内容存入文件后，再让requests.get获取后面的
            for chunk in headers_video.iter_content(chunk_size=1000):  # iter_content是一个可迭代对象
                inc += 1000 / int(headers_video.headers.get("content-length"))
                print("视频下载了%0.2f" % (inc * 100))
                headers_videos.write(chunk)

    def audio(self):
        inc = 0
        # 获取到视频的播放地址
        mp3_audio = re.findall(r'"audio":\[{"id":\d+,"baseUrl":"(.*?)"', self.vid_aud)[0]

        # 获取到视频音频
        # mp3_audio = re.findall(r'"audio":\[{"id":\d+,"baseUrl":"(.*?)"', vid_aud)[0]
        headers_audio = requests.get(url=mp3_audio, headers=self.headers_buttom, stream=True)
        with open('./%s.mp3' % self.title, 'wb') as headers_videos:
            # 流下载，比起直接content，iter_content 一次只让requests.get获取chunk_size大小的内容，
            # 等到下载的内容存入文件后，再让requests.get获取后面的
            for chunk in headers_audio.iter_content(chunk_size=1000):  # iter_content是一个可迭代对象
                inc += 1000 / int(headers_audio.headers.get("content-length"))
                print("音频下载了%0.2f" % (inc * 100))
                headers_videos.write(chunk)

    # def composite(self):
    #
    #     # os.system(f'ffmpeg -i {self.title}.mp3 -i {self.title}.mp4 -c copy {self.title}.mp4 -loglevel quiet')
    #     os.system('ffmpeg -i %s.mp4 -i %s.mp3 -c:v copy -c:a aac -strict experimental %s01.mp4'%(self.title,self.title,self.title,))
    #     # 新增，显示合成文件的大小
    #     res_ = int(os.stat(f'{self.title}.mp4').st_size / 1024)
    #     print(f'{self.title}视频合成成功......大小为：{res_}KB,{int(res_ / 1024)}MB')




Dowlat = a('https://www.bilibili.com/video/BV1A7411J7jE')

Dowlat.composite()
