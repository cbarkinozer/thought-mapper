import os
import json
from dotenv import load_dotenv
from googleapiclient.discovery import build

def fetch_all_video_details(api_key, channel_handle):
    """
    Fetches the title, description, and publication date for all videos on a given channel.

    Args:
        api_key (str): Your YouTube Data API v3 key.
        channel_handle (str): The YouTube channel handle (e.g., 'cbarkinozer').

    Returns:
        list: A list of dictionaries, each containing details for one video.
    """
    youtube = build('youtube', 'v3', developerKey=api_key)

    print(f"Fetching channel ID for handle: @{channel_handle}...")
    channel_request = youtube.channels().list(
        part="contentDetails",
        forHandle=channel_handle
    )
    channel_response = channel_request.execute()

    if not channel_response.get("items"):
        print(f"Error: Could not find channel with handle '@{channel_handle}'.")
        return []

    uploads_playlist_id = channel_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    print(f"Found uploads playlist ID: {uploads_playlist_id}")

    all_video_ids = []
    next_page_token = None
    print("Fetching all video IDs from the channel...")
    while True:
        playlist_request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=uploads_playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        playlist_response = playlist_request.execute()
        video_ids = [item["contentDetails"]["videoId"] for item in playlist_response["items"]]
        all_video_ids.extend(video_ids)
        next_page_token = playlist_response.get("nextPageToken")
        if not next_page_token:
            break
            
    print(f"Found a total of {len(all_video_ids)} videos.")

    all_video_details = []
    print("Fetching details for all videos...")
    
    for i in range(0, len(all_video_ids), 50):
        chunk = all_video_ids[i:i+50]
        video_request = youtube.videos().list(
            part="snippet",
            id=",".join(chunk)
        )
        video_response = video_request.execute()
        
        for item in video_response["items"]:
            snippet = item["snippet"]
            video_id = item["id"]
            
            # --- MODIFIED PART ---
            # Instead of saving the ID, we now construct the full URL.
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            
            all_video_details.append({
                "title": snippet["title"],
                "description": snippet["description"],
                "publishedAt": snippet["publishedAt"],
                "url": video_url # Changed from "videoId" to "url"
            })
            
    print("Successfully fetched all video details.")
    return all_video_details

def main():
    """Main function to run the YouTube data fetching process."""
    print("--- YouTube Data Fetcher ---")
    
    load_dotenv()
    api_key = os.getenv("YOUTUBE_API_KEY")

    if not api_key:
        print("Error: YOUTUBE_API_KEY not found in .env file.")
        return

    channel_handle = "cbarkinozer"
    
    video_details = fetch_all_video_details(api_key, channel_handle)

    if video_details:
        output_filename = "youtube_videos.json"
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(video_details, f, indent=4, ensure_ascii=False)
        print(f"\nSuccess! Data for {len(video_details)} videos saved to '{output_filename}'.")

if __name__ == "__main__":
    main()