#!/usr/bin/env python
import argparse
import json
import os
import uuid
from datetime import datetime

from youtube_transcript_api import YouTubeTranscriptApi


def parse_args():
    parser = argparse.ArgumentParser(description="Youtube Transcript Downloader")
    parser.add_argument("urls", metavar='URL', type=str, nargs='+', help="Youtube video URLs")
    parser.add_argument("--username", "-u", type=str, default="cbh@cameo.tw", help="Username (default: cbh@cameo.tw)")
    parser.add_argument("--folder", "-f", type=str,
                        help="Output folder path (default: data/users/[username]/youtube_transcript/[date])")
    return parser.parse_args()


def get_video_id(url):
    return url.split("=")[-1]


def cameo_youtube_transcript(url, username, output_folder):
    video_id = get_video_id(url)
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # 嘗試獲取繁體中文字幕
        try:
            transcript = transcript_list.find_transcript(['zh-Hant', 'zh-TW'])
            # print(f"找到繁體中文字幕: {transcript.language} ({transcript.language_code})")
        except:
            # 如果沒有繁體中文字幕，使用第一個可用的字幕
            transcript = next(iter(transcript_list))
            # print(f"使用字幕: {transcript.language} ({transcript.language_code})")

        # 獲取字幕內容
        transcript_data = transcript.fetch()

        result = ''
        for item in transcript_data:
            result += item.text + "\n"

        print("result:", result)

        if output_folder is None:
            output_folder = f"data/users/{username.replace('@', '_').replace('.', '_')}/youtube_transcript/{datetime.now().strftime('%Y-%m-%d')}"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        file_data = {
            "user": username,
            "type": "youtube_transcript",
            "time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "id": str(uuid.uuid4()),
            "url": url,
            "transcript": result
        }

        file_name = f"type_youtube_transcript_time_{file_data['time'].replace(':', '_')}_id_{file_data['id']}.json"
        file_path = os.path.join(output_folder, file_name)

        with open(file_path, 'w') as file:
            json.dump(file_data, file, ensure_ascii=False)

        print(f"Transcript downloaded for video {url}")

    except Exception as e:
        print(f"Error downloading transcript for video {url}: {e}")


def main():
    args = parse_args()

    for url in args.urls:
        cameo_youtube_transcript(url, args.username, args.folder)


if __name__ == '__main__':
    main()
