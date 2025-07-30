#!/usr/bin/env python3
"""
yt-dlp MCP Server

Provides YouTube video operations through MCP protocol.
"""

import json
import re
import tempfile
import os
import sys
import io
import logging
from typing import Optional, List, Dict, Any
from pathlib import Path

import yt_dlp
from fastmcp import FastMCP
from youtubesearchpython import VideosSearch, ChannelsSearch, Channel


# Initialize FastMCP
mcp = FastMCP("yt-dlp-mcp")


class YouTubeDownloader:
    """Helper class for YouTube operations using yt-dlp"""
    
    def __init__(self):
        self.base_opts = {
            'quiet': True,
            'no_warnings': True,
            'extractaudio': False,
            'audioformat': 'mp3',
            'outtmpl': '%(title)s.%(ext)s',
            'noprogress': True,  # Disable progress output
            'no_color': True,    # Disable colored output
            'logger': self._get_null_logger(),  # Use null logger
        }
    
    def _get_null_logger(self):
        """Return a null logger to suppress all yt-dlp output"""
        logger = logging.getLogger('yt-dlp-null')
        logger.setLevel(logging.CRITICAL + 1)  # Disable all logging
        return logger
    
    def get_video_info(self, url: str) -> Dict[str, Any]:
        """Extract video information without downloading"""
        opts = self.base_opts.copy()
        opts.update({
            'skip_download': True,
            'writesubtitles': False,
            'writeautomaticsub': False,
        })
        
        with yt_dlp.YoutubeDL(opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                return info
            except Exception as e:
                raise Exception(f"Failed to extract video info: {str(e)}")
    
    def get_transcription(self, url: str, keep_timestamps: bool = False) -> str:
        """Extract transcription from YouTube video"""
        # Redirect stdout and stderr to suppress yt-dlp output
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = io.StringIO()
        sys.stderr = io.StringIO()
        
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                opts = self.base_opts.copy()
                opts.update({
                    'skip_download': True,
                    'writesubtitles': True,
                    'writeautomaticsub': True,
                    'subtitleslangs': ['en', 'en-US', 'en-GB'],
                    'subtitlesformat': 'vtt',
                    'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                })
                
                with yt_dlp.YoutubeDL(opts) as ydl:
                    try:
                        info = ydl.extract_info(url, download=False)
                        video_id = info.get('id', 'video')
                        video_title = info.get('title', 'Unknown Title')
                        
                        # Process the video to get subtitles
                        ydl.process_info(info)
                        
                        # Look for subtitle files
                        subtitle_files = []
                        for file in Path(temp_dir).glob('*.vtt'):
                            subtitle_files.append(file)
                        
                        if not subtitle_files:
                            return f"No transcription available for video: {video_title}"
                        
                        # Process the first available subtitle file
                        subtitle_file = subtitle_files[0]
                        transcription = self._process_vtt_file(subtitle_file, keep_timestamps)
                        
                        return f"Transcription for '{video_title}':\n\n{transcription}"
                        
                    except Exception as e:
                        raise Exception(f"Failed to extract transcription: {str(e)}")
        finally:
            # Restore stdout and stderr
            sys.stdout = old_stdout
            sys.stderr = old_stderr
    
    def _process_vtt_file(self, vtt_file: Path, keep_timestamps: bool) -> str:
        """Process VTT subtitle file to extract text"""
        try:
            with open(vtt_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            transcription_lines = []
            
            for i, line in enumerate(lines):
                line = line.strip()
                
                # Skip VTT header and empty lines
                if not line or line.startswith('WEBVTT') or line.startswith('NOTE'):
                    continue
                
                # Check if line contains timestamp
                if '-->' in line:
                    if keep_timestamps:
                        transcription_lines.append(f"[{line}]")
                    continue
                
                # Skip cue settings and add actual text
                if not re.match(r'^[\d:.,\s\-\>]+$', line) and line:
                    # Clean up HTML tags and formatting
                    clean_line = re.sub(r'<[^>]+>', '', line)
                    clean_line = clean_line.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
                    if clean_line.strip():
                        transcription_lines.append(clean_line.strip())
            
            return '\n'.join(transcription_lines)
            
        except Exception as e:
            return f"Error processing subtitle file: {str(e)}"


@mcp.tool()
def get_transcription(url: str, keep_timestamps: bool = False) -> str:
    """
    Extract transcription from a YouTube video.
    
    Args:
        url: YouTube video URL
        keep_timestamps: Whether to keep timestamp information in the transcription
    
    Returns:
        Video transcription text
    """
    try:
        downloader = YouTubeDownloader()
        return downloader.get_transcription(url, keep_timestamps)
    except Exception as e:
        return f"Error getting transcription: {str(e)}"


@mcp.tool()
def search_videos(search_terms: str, max_results: int = 10) -> List[Dict[str, str]]:
    """
    Search for YouTube videos by terms and return video information.
    
    Args:
        search_terms: Search query for YouTube videos
        max_results: Maximum number of results to return (default: 10)
    
    Returns:
        List of dictionaries containing video title, URL, and description
    """
    try:
        videos_search = VideosSearch(search_terms, limit=max_results)
        results = videos_search.result()
        
        video_list = []
        for video in results['result']:
            video_info = {
                'title': video.get('title', 'Unknown Title'),
                'url': video.get('link', ''),
                'description': video.get('descriptionSnippet', [{}])[0].get('text', '') if video.get('descriptionSnippet') else '',
                'duration': video.get('duration', 'Unknown'),
                'views': video.get('viewCount', {}).get('text', 'Unknown'),
                'channel': video.get('channel', {}).get('name', 'Unknown Channel')
            }
            video_list.append(video_info)
        
        return video_list
    except Exception as e:
        return [{"error": f"Search failed: {str(e)}"}]


@mcp.tool()
def list_channel_videos(channel_identifier: str, max_videos: int = 10) -> List[Dict[str, str]]:
    """
    List recent videos from a YouTube channel.
    
    Args:
        channel_identifier: Channel name, URL, or handle (e.g., "@channelname" or "UC...")
        max_videos: Number of recent videos to return (default: 10)
    
    Returns:
        List of dictionaries containing video information from the channel
    """
    try:
        # Handle different channel identifier formats
        if channel_identifier.startswith('@'):
            # Handle format
            search_query = channel_identifier
        elif channel_identifier.startswith('UC') or channel_identifier.startswith('http'):
            # Channel ID or URL
            search_query = channel_identifier
        else:
            # Channel name - search for it first
            channel_search = ChannelsSearch(channel_identifier, limit=1)
            channel_results = channel_search.result()
            
            if not channel_results['result']:
                return [{"error": f"Channel '{channel_identifier}' not found"}]
            
            search_query = channel_results['result'][0]['id']
        
        # Get channel videos
        channel = Channel.get(search_query)
        
        if not channel:
            return [{"error": f"Could not retrieve channel information for '{channel_identifier}'"}]
        
        videos = []
        video_count = 0
        
        # Get videos from the channel
        for video in channel['videos']:
            if video_count >= max_videos:
                break
            
            video_info = {
                'title': video.get('title', 'Unknown Title'),
                'url': video.get('link', ''),
                'description': video.get('descriptionSnippet', [{}])[0].get('text', '') if video.get('descriptionSnippet') else '',
                'duration': video.get('duration', 'Unknown'),
                'views': video.get('viewCount', {}).get('text', 'Unknown'),
                'published': video.get('publishedTime', 'Unknown')
            }
            videos.append(video_info)
            video_count += 1
        
        return videos
    except Exception as e:
        return [{"error": f"Failed to list channel videos: {str(e)}"}]


def main():
    """Main entry point for the MCP server"""
    mcp.run()


if __name__ == "__main__":
    main()
