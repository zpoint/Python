# coding=utf8
import os
import json
from moviepy.editor import VideoFileClip

FINAL_DICT = dict()
SUFFIX = {"mp4", }
PROCESSING_SET = set()


def time_convert(size):
    M, H = 60, 60 ** 2
    if size < M:
        return str(size) + u'秒'
    if size < H:
        return u'%s分钟%s秒 ' % (int(size / M), int(size % M))
    else:
        hour = int(size /H)
        mine = int(size % H /M)
        second = int(size % H %M)
        tim_srt = u'%s小时%s分钟%s秒 ' % (hour, mine, second)
        return tim_srt


def get_file_times(filename):
    u"""
    获取视频时长（s:秒）
    """
    clip = VideoFileClip(filename)
    file_time = clip.duration
    return file_time


def get_all(dire, parent_lst=None):
    if parent_lst is None:
        FINAL_DICT[dire] = [dict(), 0]
        parent_lst = FINAL_DICT[dire]
    parent_dict = parent_lst[0]

    for each in os.listdir(dire):
        target_dir = dire + os.path.sep + each
        if os.path.isdir(target_dir):
            # 文件夹
            if target_dir not in PROCESSING_SET:
                PROCESSING_SET.add(target_dir)
                print("正在扫描: %s" % (target_dir,))

            new_parent_dict = dict()
            parent_dict[target_dir] = [new_parent_dict, 0]
            get_all(target_dir, parent_dict[target_dir])
        else:
            # 文件
            suffix = each.split(".")[-1]
            if suffix in SUFFIX:
                parent_dict[target_dir] = get_file_times(target_dir)


def sum_all(current_lst=None, level=0):
    if current_lst is None:
        current_lst = FINAL_DICT[list(FINAL_DICT.keys())[0]]
        current_dict = FINAL_DICT
    else:
        current_dict = current_lst[0]

    level_val = 0
    for key, value in current_dict.items():
        if isinstance(value, (int, float)):
            # 最后一级
            level_val += value
            continue

        result_val = sum_all(value, level+1)
        level_val += result_val

    current_lst[1] = level_val
    return level_val


def pr_all(current_dict=None, level=0):
    if current_dict is None:
        current_dict = FINAL_DICT

    for key, value in current_dict.items():
        if isinstance(value, (int, float)):
            # 最后一级
            if value > 0:
                print("\t" * level, key, time_convert(value))
            continue

        next_dict, val = value
        if val > 0:
            print("\t" * level, key, time_convert(val))
            pr_all(next_dict, level+1)


def load(dire):
    global FINAL_DICT
    has_cache = False
    cache_key = "".join(dire.split(os.path.sep)).replace(":", "")
    cache_key = "./" + cache_key + ".json"
    if os.path.exists(cache_key):
        try:
            with open(cache_key, "r") as f:
                FINAL_DICT = json.loads(f.read())
            has_cache = True
        except Exception as e:
            os.remove(cache_key)
            FINAL_DICT = dict()
    if not has_cache:
        get_all(dire)
        print("\n" * 5)
        sum_all()
        print("dumping to file: %s" % (cache_key, ))
        with open(cache_key, "w") as f:
            f.write(json.dumps(FINAL_DICT))
    pr_all()
    input("输入Enter退出....")


if __name__ == "__main__":
    load("E:\\摄影")
