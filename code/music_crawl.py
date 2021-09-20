# 实现背景音乐以及数据的爬取
import requests
import csv


def getMusicInfo():
    # url = 'https://api-service.chanmama.com/v1/music/search?keyword=&page=1&size=50&orderby=user_count&incr_type=7d&order=desc'
    url = 'https://api-service.chanmama.com/v1/music/search?keyword=&page=' + page + '&size=50&orderby=user_count&incr_type=7d&order=desc'
    headers = {'accept': 'application/json,text/plain,*/*', 'accept-Encoding': 'gzip, deflate, br',
               'accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
               # authorization请通过f12->network->xhr文件的header查看
               'authorization': authorization,
               'connection': 'keep-alive',
               'host': 'api-service.chanmama.com',
               'origin': 'https://www.chanmama.com',
               'referer': 'https://www.chanmama.com/musicRank?keyword=&incr_type=7d',
               'sec-fetch-dest': 'empty',
               'sec-fetch-site': 'same-site',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
               }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            list = response.json().get('data').get('list')
            for item in list:
                del item['cover_image']
                del item['use_trend']
                del item['hot_awemes']
                del item['is_fav']
            return list
    except requests.ConnectionError as e:
        print('Error', e.args)


def downloadMusic(id, name):
    url = 'https://api-service.chanmama.com/v1/music/getPlayUrl?music_id=' + id
    headers = {'accept': 'application/json,text/plain,*/*',
               'accept-Encoding': 'gzip, deflate, br',
               'accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
               # authorization请通过f12->network->xhr文件的header查看
               'authorization': authorization,
               'connection': 'keep-alive',
               'host': 'api-service.chanmama.com',
               'origin': 'https://www.chanmama.com',
               'referer': 'https://www.chanmama.com/musicDetail/' + id,
               'sec-fetch-dest': 'empty',
               'sec-fetch-mode': 'cors',
               'sec-fetch-site': 'same-site',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
               }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            src = response.json().get('data')
            print(name, end=": ")
            if src != '' and src != 'None':
                music = requests.get(src)
                # 下面填写本地存储的路径，记得后缀添加mp3
                open(downLoadPath + name + '.mp3', 'wb').write(music.content)
                print("成功")
            else:
                print("歌曲不存在")
    except requests.ConnectionError as e:
        print('Error', e.args)  # 输出异常信息


def writeToCsv(music_info):
    with open(csvPath, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["音乐ID", "音乐名", "创作者", "歌曲时间", "使用人数", "使用人数增量"])
        for item in music_info:
            writer.writerow([item.get('music_id'), item.get('title'), item.get('author'), item.get('audition_duration'),
                             item.get('user_count'), item.get('user_incr')])
        print("csv写入成功！")


page = '8'
downLoadPath = '../mp3/351-400/'
csvPath = '../mp3/351-400/data.csv'
authorization = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBJZCI6MTAwMDAsImV4cGlyZV90aW1lIjoxNTk2Mzk0ODAwLCJpYXQiOjE1OTU4NDAwMjQsImlkIjo1NzI5OTl9.mAsVCdfhfQ8sNH4jKjFxERs5udQL1hB0U7IjsJsgRls'

if __name__ == '__main__':

    music_info = getMusicInfo()
    writeToCsv(music_info)
    for item in music_info:
        downloadMusic(item.get('music_id'), item.get('title'))
