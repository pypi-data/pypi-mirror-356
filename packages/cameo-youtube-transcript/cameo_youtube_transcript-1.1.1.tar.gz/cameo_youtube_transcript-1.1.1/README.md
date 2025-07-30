````markdown
# Cameo Youtube Transcript Downloader

Cameo Youtube Transcript Downloader 是一個 Python 套件，它可以簡單地從 YouTube 影片下載字幕。此工具可以透過 Python 庫的方式使用，也可以在命令列界面運行。

## 安裝

使用以下命令安裝 Cameo Youtube Transcript Downloader：

```sh
python3 -m pip install cameo-youtube-transcript
```
````

或者從 GitHub 安裝：

```sh
python3 -m pip install git+https://github.com/bohachu/cameo_youtube_transcript.git
```

## 套件用法

在 Python 程式可以透過以下方式匯入並使用 Cameo Youtube Transcript Downloader：

```python
from cameo_youtube_transcript import cameo_youtube_transcript

# 下載字幕
cameo_youtube_transcript(url, username, output_folder)
```

其中，`url` 是您要下載字幕的 Youtube 影片網址，`username` 是您的使用者名稱，`output_folder` 是存放輸出目錄的路徑。

## 命令列界面用法

在命令列界面，可以直接運行模組：

```sh
cameo_youtube_transcript
```

命令列界面提供以下參數：

- `urls`: Youtube 影片網址（必填）
- `--username`, `-u`: 使用者名稱（可選，預設為 "cbh@cameo.tw"）
- `--folder`, `-f`: 輸出目錄的路徑（可選）

範例：

```sh
cameo_youtube_transcript "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -u "cbh@cameo.tw" -f "/path/to/output/folder"
```

## 功能特色

- 支援繁體中文字幕優先下載
- 如果找不到繁體中文字幕，會自動使用第一個可用的字幕
- 將下載的字幕儲存為 JSON 格式，包含影片 URL、字幕內容等資訊
- 可同時處理多個 YouTube 影片 URL

## 輸出範例

```json
{
  "user": "cbh@cameo.tw",
  "type": "youtube_transcript",
  "time": "2023-05-21T04:21:18Z",
  "id": "23b9242f-2f62-42e8-bdbe-f65241d2ac5a",
  "url": "https://www.youtube.com/watch?v=HEquaCEckwg",
  "transcript": "0:00\nsummary of finish big by bill birlingham\n0:04\nwritten by lee schullery in quick read\n0:06\nnarrated\n0:07\nby alex smith introduction\n0:11\nthe truth is that every entrepreneur\n..."
}
```

## 版本歷史

- 1.1.1 (現行版本)
  - 更新 youtube-transcript-api 至 v1.1.1
  - 調整新版 api 取得 text 的方式
- 1.1.0
  - 更新功能以優先支援繁體中文字幕
- 1.0.4
  - 更名為 cameo-youtube-transcript
  - 加入 print 列印直接顯示
- 1.0.3
  - 改名字從 youtube_transcript_downloader 到 youtube_transcript 避免撞名 pypi
- 1.0.2
  - 新增加 README.md 完整說明
