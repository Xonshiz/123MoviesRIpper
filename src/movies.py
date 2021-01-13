#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
import argparse
import logging
import platform
from cust_utils import *
from __version__ import __version__
from movies_api import *
from bs4 import BeautifulSoup


class Movies:
    def __init__(self, argv, cwd):
        print("Main")
        self.queue = []
        related_episodes = []
        url = None
        file_name = None
        video_file_name = None
        base_page_content = None
        youtube_dl_command = None
        url = 'https://new-movies123.co/tv-series/deutschland-89-season-1/UyTSbjuh/917zdf25/abfjn1jk-watch-online-for-free.html'
        resolution = '1080'
        while not url:
            url = input("Enter Movie URL : ").strip()
        if url:
            self.get_episode_list(url=url)

    def single_episode(self, url, file_name, add_to_queue=False):
        xml_request_data = get_xml_http_request(url)
        if xml_request_data and xml_request_data == "none":
            print("IP Limit Reached")
            sys.exit(1)
        if xml_request_data:
            xml_request_data = dict(xml_request_data[0])
            video_url = xml_request_data.get('src', None)
            max_resolution = xml_request_data.get('max', None)
            if not video_url:
                video_url = xml_request_data.get('file', None)
                if not video_url:
                    print("Couldn't get Video Stream URL.")
                    sys.exit(1)
            if video_url:
                print("Got Video Stream.")
                if max_resolution:
                    print("Will Be Downloading {0} Stream.".format(max_resolution))
                    video_url = str(video_url).replace('/360?', '/{0}?'.format(max_resolution))
                else:
                    print("Couldn't Find Max Resolution. Going with default {0}.".format(
                        xml_request_data.get('label', '')))

                base_page_content = get_http_request(url, text_only=True)
                if not base_page_content:
                    print("Can't Parse Basic Info")
                    # ASK USER FOR FILE NAME
                    while not file_name:
                        file_name = input("Enter file name : ").strip()
                else:
                    soup = BeautifulSoup(base_page_content, 'html.parser')

                    video_metadata = soup.find_all('script', type='application/ld+json')
                    if not video_metadata:
                        print("Can't find metadata")
                    if len(video_metadata) > 1:
                        metadata_json = str(video_metadata[0]).replace('<script type="application/ld+json">',
                                                                       '').replace('</script>', '')
                        season_metadata = dict(json.loads(str(metadata_json)))
                        current__episode_metadata_json = str(video_metadata[1]).replace(
                            '<script type="application/ld+json">', '').replace('</script>', '')
                        current_video_metadata = dict(json.loads(current__episode_metadata_json))
                        current_episode_list = current_video_metadata.get('itemListElement')
                        if current_episode_list and len(current_episode_list) > 0:
                            episode_dict = dict(current_episode_list[-1])
                            episode_item = episode_dict.get('item')
                            current_episode_name = utils.get_clean_path_name(dict(episode_item).get('name'))
                            file_name = '{0}.srt'.format(current_episode_name)
                            video_file_name = '{0}.mp4'.format(current_episode_name)
                            subs_json = re.search(r'window.subtitles = (.*?)</script>', str(base_page_content))
                            if subs_json:
                                subtitle_info_list = eval(subs_json.group(1))
                                subtitle_info = dict(subtitle_info_list[0]).get('src')
                                if subtitle_info:
                                    subtitle_src = str(subtitle_info).replace('\\', '')
                                    subtitle_content = browser_instance.get_request(subtitle_src, text_only=True)
                                    series_name = url.split('/')[4]
                                    if not path_util.file_exists('dist', os.sep + series_name):
                                        path_created = path_util.create_paths('dist' + os.sep + series_name + os.sep + video_file_name)
                                        if path_created:
                                            file_written = utils.create_file_binary_mode(path_created, os.sep + file_name, subtitle_content)
                                            if file_written:
                                                print("Downloaded : {0}".format(file_name))
                                            yt_command = utils.get_youtube_dl_command(file_location=path_created + os.sep + video_file_name, video_url=video_url)
                                            if add_to_queue:
                                                print("Added To Queue")
                                                self.queue.append(yt_command)
                                            else:
                                                print("Youtube-dl Command: {0}".format(yt_command))
                                                process_code = utils.call_youtube_dl(yt_command)
                                                print("Process Done: {0}".format(process_code))
        return 0

    def get_episode_list(self, url):
        related_episodes = []
        base_page_content = get_http_request(url, text_only=True)
        soup = BeautifulSoup(base_page_content, 'html.parser')

        video_metadata = soup.find_all('script', type='application/ld+json')
        if not video_metadata:
            print("Can't find metadata")
        if len(video_metadata) > 1:
            metadata_json = str(video_metadata[0]).replace('<script type="application/ld+json">',
                                                           '').replace('</script>', '')
            season_metadata = dict(json.loads(str(metadata_json)))
            # current__episode_metadata_json = str(video_metadata[1]).replace('<script type="application/ld+json">', '').replace('</script>', '')
            # current_video_metadata = dict(json.loads(current__episode_metadata_json))
            episodes = season_metadata.get('episode', [])
            for episode in episodes:
                url = dict(episode).get('url', None)
                if url:
                    related_episodes.append(str(url))
            print("Total Episodes To Download: {0}".format(len(related_episodes)))
            for episode_url in related_episodes:
                self.single_episode(url=episode_url, file_name=None, add_to_queue=True)
            for current_command in self.queue:
                print(current_command)
                process_code = utils.call_youtube_dl(current_command)
                print("Process Done: {0}".format(process_code))
        return 0

