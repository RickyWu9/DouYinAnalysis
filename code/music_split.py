# 将音乐取前n秒片段

from pydub import AudioSegment


def split_music(begin, end, filepath, filename):
    # 导入音乐
    song = AudioSegment.from_mp3(filepath)

    # 取begin秒到end秒间的片段
    song = song[begin * 1000: end * 1000]

    # 存储为临时文件做备份
    temp_path = '../音乐/backup/' + filename+'.wav'
    song.export(temp_path)
    return temp_path

