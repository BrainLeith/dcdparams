import re
from pprint import pprint
import threading
import requests

main_url = "https://music.163.com/playlist?id=14435255"

cookie = {
    'JSESSIONID-WYYY': 'padBx5xFs2f%2FPPpS29zovKQ927gJ553SFSdzgASW4zkZ5piSiX8%2Fy%2F5p8yVqhCbNzhufmo%2FFNfzUAWPpm6M3BrmA8yDk3ynBp1qftTfDw%2BvYA5H4WjkgRHy6DK%2FJEBu%2FAhnR8JV%5CCpaMXMHWP8x6PV41swh%5Csf6F1SCYkDsPn%2BmZ%2BVEP%3A1687883715649',
    'MUSIC_U': '000825AC29DAC572C40F6C28EF32287F337165EDEB07DDD68B3375DB06844794A4428A31BD645EA5A28E9DAEDC1AC943976EBE969CE3EF7F8B6A47C71A23732B81B95125937419E3521E381AF170127E77C6EEE0B39E3058B2DA1D722360BD1370D3A329329F2251D2FF65AB22B0A15F9EEBE8505280730C0674F497078267E19347DFC227E307A245B5EAF8733460965CB392BAC2207C064A166CA106A40DD90B65389F00D224437E5D6C58DBF171A6B8BC8B51D0A46F75EA11C5A5184D8C18C95D7510771E5CA3A5FFDED4385161BA04867A13D6E91CF92EEAC89CB014F467E338499DD5209E52CBFB9933CF57BD3F77D322E1BB5560FD32B6DC7315A58A3284A86A6E30D7D6AC1F130E2100EB7BC762035B059B5849645830B370D06390B4A0BC4636DEAA98EEE42768ADBDF63F6CEB603D8BEAD3872524727AE72AA4C60F5C9BFDBA579A793C6A96DD53A734ECBCAB56D46B96BCBC8EC1303012AE585A01FF59007B68027BA76D019E0C15AF9529BB',
    'NMTID': '00OGjMJ_l31xD7300WirAs0x6sHz2YAAAGI_ZofEQ',
    'NTES_P_UTID': 'oIjZxizYJz8Xkybbx2B1GSUhu5SDPNPg|1687881943',
    'NTES_SESS': 'IDfnBzKVnSebnXBP9tfJnZKs_xheMzo33Pvz049SaXZ7LJgka6ijVu.L70PkVG4qOWdXNcHKwRsXcYHhWd_UHgzlwNX3hQ6D.e.MWdLOO.W8vvioTFq7TJBe6MfbDvJvUpBzILy7th31v2D4s3OoiLhGvcwCz9J4nEeTT4MEZ5Ax74rNf3ixMrr8mwtzyt4eQgWxX6UFpMb4zJ4SXdzFeUuxJ0USTu_sTkRgF6xIxVeKD',
    'P_INFO': 'qiuciji@126.com|1687881943|0|music|11&16|hub&1682228511&music#hub&421100#10#0#0|139083&0|music&cloudmusic|qiuciji@126.com',
    'S_INFO': '1687881943|0|#3&80#|qiuciji@126.com#qiuciji',
    'WEVNSM': '1.0.0',
    'WM_TID': 'qnzhqb.1687881916977.01.0',
    '__csrf': '32dc8bed6ae7fba8796443e23c4b054e',
    '__remember_me': 'true',
    '__snaker__id': 'BNpoSUASw9B8eRTh',
    '_iuqxldmzr_': 32,
    '_ntes_nnid': '70a26aac4ca7abf4917ab7519d9c0e11,1687881915667',
    '_ntes_nuid': '70a26aac4ca7abf4917ab7519d9c0e11',
    'gdxidpyhxdE': 'dMuN4D6Pu0P9mS4BuKGE3k9EzNkWJuWr3DuUbD32RI%5CVudeSOcWJBqHiVO6I2xpOrY5bnm67VBsrjhyniLJSIhIvf9Rvo0XEJh19dkf6HApAm8vbrApI2CG%2FX5xprigTm%2BfY1RAN88iUglRdSTPNipqiHTLLeLKCiAnK8%2FpMOnn9kXW%2F%3A1687882834299',
    'ntes_utid': 'tid._.%252B2w4%252BHz2jKdEVlRVRRfQwOq3Hurc61e4._.0',
    'sDeviceId': 'YD-%2FbOCQ1ir%2FQBAB1RRVFPEwbv3D%2Brd6hfs'
}

headers = {
    'cookie': ';'.join([f'{key}={value}' for key, value in cookie.items()]),
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'referer': 'https://music.163.com/'
}


class DownloadThread(threading.Thread):
    def __init__(self, song_id, song_name, headers):
        threading.Thread.__init__(self)
        self.song_id = song_id
        self.song_name = song_name
        self.headers = headers

    def run(self):
        song_url = f'https://music.163.com/song/media/outer/url?id={self.song_id}.mp3'
        print(song_url)
        song_data = requests.get(song_url, headers=self.headers).content
        with open(f'static/{self.song_name}.mp3', 'wb') as f:
            f.write(song_data)


if __name__ == '__main__':
    print('开始下载')
    response = requests.get(main_url, headers=headers).text
    songs = re.findall('<a href="/song\?id=(\d*?)">(.*?)</a>', response)
    pprint(songs)
    threads = []
    for song in songs:
        song_id = song[0]
        song_name = song[1]
        thread = DownloadThread(song_id, song_name, headers)
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    print('下载完成')
