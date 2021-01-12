#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import path_util
import subprocess


def create_file(file_path, file_name, data_to_write):
    if not isinstance(data_to_write, str):
        data_to_write = str(data_to_write)
    if not data_to_write or not str(data_to_write).strip():
        print("Empty data provided for {0}".format(file_name))
        return False
    file_location = path_util.get_abs_path_name(file_path, file_name)
    with open(file_location, 'w') as f:
        f.write(data_to_write)
        f.flush()
    return True


def create_file_binary_mode(file_path, file_name, data_to_write):
    if not data_to_write or not str(data_to_write).strip():
        print("Empty data provided for {0}".format(file_name))
        return False
    file_location = path_util.get_abs_path_name(file_path, file_name)
    with open(file_location, 'wb') as f:
        f.write(data_to_write)
        f.flush()
    return True


def read_file_data(file_path, file_name):
    file_location = path_util.get_abs_path_name(file_path, file_name)
    content = None
    with open(file_location, 'r') as f:
        content = f.read().strip()
    return None if content == "" else content


def get_clean_path_name(path_name):
    for cha in '\/*?:"<>|,;\'':
        path_name = path_name.replace(cha, ' -')
    return path_name


def get_youtube_dl_command(file_location, video_url):
    command = 'youtube-dl -i "{0}" -o "{1}"'.format(video_url, file_location)
    return command


def call_youtube_dl(youtube_dl_command):
    process = subprocess.Popen(youtube_dl_command, shell=True, stdout=subprocess.PIPE)
    process.wait()
    return process.returncode
