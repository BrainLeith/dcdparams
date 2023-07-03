import os
import requests
import re
import json
from lxml import etree
import ffmpeg

cookie_dict= {
    'b_lsid': 'c4e1b2b6%2C1624974869%2C5c4a9*41',
    'home_feed_column': 4,
    'header_theme_version': 'CLOSE',
    'DedeUserID': '350372771',
    'bili_jct': 'a7ac2520a375ff06310c4b9e7d0a93ea',
    'FEED_LIVE_VERSION': 'V_TOPSWITCH_FLEX',
    'sid': '5ltl3a9l',
    'SESSDATA': 'e358b854%2C1701791016%2C930a9%2A62',
    'CURRENT_FNVAL': 4048,
    'buvid3': 'F93BFFD4-FFD7-B258-7199-1E677D078A0C83544infoc',
    'buvid4': 'A9B3FB15-1735-A61B-F392-9C321B736B4520423-023060823-hdBRAxj2TsIlBFdJi%2FD%2FWw%3D%3D',
    'bp_video_offset_350372771': '810717215310479400',
    'rpdid': '''|(Yl)YR)|Y0J'uY)YkJ)~k|''',
    'browser_resolution': '1274-805',
    'b_nut': 1685598283,
    'DedeUserID__ckMd5': '88b72679fbcd6dcb'
}

headers = {
    'cookie': ';'.join([f'{key}={value}' for key, value in cookie_dict.items()]),
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'referer': 'https://www.bilibili.com/'
}

if __name__ == '__main__':
    url = 'https://www.bilibili.com/video/BV12a4y1K748/?spm_id_from=pageDriver&vd_source=41a53bd9b3706835bf4d02c24948565d'
    response = requests.get(url, headers=headers)
    # print(response.text)
    info = re.findall(r'<script>window.__playinfo__=(.*?)</script>', response.text)[0]
    video_url = json.loads(info)['data']['dash']['video'][0]['baseUrl']
    audio_url = json.loads(info)['data']['dash']['audio'][0]['baseUrl']
    print(video_url)
    print(audio_url)
    file_name = re.findall(r'<h1 title="(.*?)" class="video-title tit">', response.text)[0]
    print(file_name)
    video_data = requests.get(video_url, headers=headers).content
    audio_data = requests.get(audio_url, headers=headers).content
    video_path = 'static/video.mp4'
    audio_path = 'static/audio.mp3'
    out_path = f'static/{file_name}.mp4'
    if os.path.exists(out_path):
        os.remove(out_path)
    with open(f'{video_path}', 'wb') as f:
        f.write(video_data)
    with open(f'{audio_path}', 'wb') as f:
        f.write(audio_data)
    cmd = f'ffmpeg -i {video_path} -i {audio_path} -c:v copy -c:a aac -strict experimental {out_path} -loglevel quiet'
    os.system(cmd)
    os.remove(video_path)
    os.remove(audio_path)
