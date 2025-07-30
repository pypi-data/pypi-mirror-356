from setuptools import setup, find_packages

setup(
    name="cameo-youtube-transcript",
    version="1.1.1",
    author="Bowen Chiu",
    author_email="cbh@cameo.tw",
    description="一個用於下載 YouTube 影片字幕的工具",
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/bohachu/cameo_youtube_transcript",
    packages=find_packages(),
    py_modules=['cameo_youtube_transcript'],
    install_requires=[
        'youtube_transcript_api==1.1.0',
    ],
    entry_points={
        'console_scripts': [
            'cameo_youtube_transcript = cameo_youtube_transcript:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: Chinese (Traditional)",
        "Topic :: Multimedia :: Video",
        "Topic :: Text Processing",
    ],
    python_requires=">=3.6",
    keywords="youtube, transcript, subtitle, 字幕, 下載, cameo",
    license="MIT",
)