# yt-dlp MCP Server

A Model Context Protocol (MCP) server that provides YouTube video operations using yt-dlp.

## Features

- **Get Transcriptions**: Extract transcriptions from YouTube videos with optional timestamp preservation
- **Search Videos**: Search for YouTube videos by terms and return URLs
- **List Channel Videos**: Get recent videos from a YouTube channel

## Installation

```bash
pip install -e .
```

## Usage

Run the MCP server:

```bash
yt-dlp-mcp
```

## Tools

### get_transcription
- **Input**: YouTube URL, optional timestamp preservation flag
- **Output**: Video transcription text

### search_videos
- **Input**: Search terms
- **Output**: List of YouTube video URLs

### list_channel_videos
- **Input**: Channel name/URL, number of videos to return
- **Output**: List of recent video URLs from the channel

## Requirements

- Python 3.8+
- yt-dlp
- fastmcp
- youtube-search-python
