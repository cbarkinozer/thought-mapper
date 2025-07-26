import json
import os
import re
from sentence_transformers import SentenceTransformer, util
import torch
from datetime import datetime
from tqdm import tqdm

# --- CONFIGURATION ---
TOPIC_THRESHOLD = 0.25
MAX_TOPICS_PER_ITEM = 3 # Renamed from TWEET for clarity

def load_topics(file_path='topics.txt'):
    """Loads a list of topics from a text file."""
    print(f"Loading topics from '{file_path}'...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            topics = [line.strip() for line in f if line.strip()]
        print(f"Found {len(topics)} topics.")
        return topics
    except FileNotFoundError:
        print(f"Error: '{file_path}' not found. Please create it.")
        return None

def clean_text(text):
    """A general-purpose text cleaner."""
    text = re.sub(r'https?:\/\/\S+', '', text)
    text = re.sub(r'\[https?:\/\/\S+\]', '', text)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'pic\.x\.com\/\S+', '', text)
    text = text.replace('\n', ' ')
    text = ' '.join(text.split())
    return text.strip()

def parse_tweets_js(file_path='tweets.js'):
    """Parses tweets and returns them in a standardized format."""
    print(f"\nParsing '{file_path}'...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Info: '{file_path}' not found, skipping.")
        return []

    start_index = content.find('[')
    end_index = content.rfind(']')
    if start_index == -1 or end_index == -1: return []

    json_data_str = content[start_index : end_index + 1]
    raw_tweets = json.loads(json_data_str)
    
    standardized_content = []
    for item in raw_tweets:
        tweet = item.get('tweet', {})
        full_text = tweet.get('full_text', '')
        if not full_text: continue
        
        cleaned_full_text = clean_text(full_text)
        date_obj = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
        
        standardized_content.append({
            'text_for_embedding': cleaned_full_text,
            'title': cleaned_full_text,
            'description': '',
            'date': date_obj,
            'platform': 'X',
            'source': f"https://twitter.com/user/status/{tweet.get('id_str', '')}"
        })
    print(f"Successfully parsed {len(standardized_content)} items from X.")
    return standardized_content

def parse_articles_txt(file_path='articles.txt'):
    """Parses articles from a text file and returns them in a standardized format."""
    print(f"\nParsing '{file_path}'...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Info: '{file_path}' not found, skipping.")
        return []

    month_map = {
        'Ocak': 1, 'Şubat': 2, 'Mart': 3, 'Nisan': 4, 'Mayıs': 5, 'Haziran': 6,
        'Temmuz': 7, 'Ağustos': 8, 'Eylül': 9, 'Ekim': 10, 'Kasım': 11, 'Aralık': 12
    }
    
    standardized_content = []
    current_year, current_month = 0, 0
    sections = re.split(r'(^\w+\s+\d{4}$|^\d+\.\s)', content, flags=re.MULTILINE)
    
    for i, part in enumerate(sections):
        part = part.strip()
        if not part: continue

        month_match = re.match(r'(\w+)\s+(\d{4})', part)
        if month_match:
            month_name, year = month_match.groups()
            current_month = month_map.get(month_name, 1)
            current_year = int(year)
            continue

        if re.match(r'^\d+\.', part):
            content_part = sections[i+1]
            link_match = re.search(r'\[(https?:\/\/\S+)\]', content_part)
            link = link_match.group(1) if link_match else ""
            
            text_content = content_part.replace(link_match.group(0), '') if link_match else content_part
            lines = text_content.strip().split('\n')
            title = lines[0].strip()
            description = " ".join(lines[1:]).strip()
            
            text_for_embedding = f"{title}. {description}"
            
            standardized_content.append({
                'text_for_embedding': clean_text(text_for_embedding),
                'title': title,
                'description': description,
                'date': datetime(current_year, current_month, 1),
                'platform': 'Medium',
                'source': link
            })
            
    print(f"Successfully parsed {len(standardized_content)} items from Medium.")
    return standardized_content

# --- NEW: Parser for YouTube JSON data ---
def parse_youtube_json(file_path='youtube_videos.json'):
    """Parses YouTube video data and returns it in a standardized format."""
    print(f"\nParsing '{file_path}'...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            videos = json.load(f)
    except FileNotFoundError:
        print(f"Info: '{file_path}' not found, skipping.")
        return []

    standardized_content = []
    for video in videos:
        title = video.get('title', '')
        description = video.get('description', '')
        if not title: continue # Skip videos without a title

        # Use title + description for the best embedding context
        text_for_embedding = f"{title}. {description}"
        
        # The YouTube API returns dates in ISO 8601 format
        date_obj = datetime.fromisoformat(video['publishedAt'].replace('Z', ''))

        standardized_content.append({
            'text_for_embedding': clean_text(text_for_embedding),
            'title': title,
            'description': description,
            'date': date_obj,
            'platform': 'YouTube',
            'source': video.get('url', '')
        })
    print(f"Successfully parsed {len(standardized_content)} items from YouTube.")
    return standardized_content


def assign_topics(embeddings, topic_embeddings, topic_names):
    """Assigns topics to each content item based on semantic similarity."""
    print("\nAssigning topics to all content...")
    cosine_scores = util.cos_sim(embeddings, topic_embeddings)
    
    content_topics_map = []
    for i in range(len(embeddings)):
        item_scores = cosine_scores[i]
        topic_score_pairs = list(zip(topic_names, item_scores))
        topic_score_pairs.sort(key=lambda x: x[1], reverse=True)
        
        assigned_topics = [
            topic for topic, score in topic_score_pairs if score > TOPIC_THRESHOLD
        ][:MAX_TOPICS_PER_ITEM]
        
        if not assigned_topics: assigned_topics = [topic_score_pairs[0][0]]
        content_topics_map.append(assigned_topics)
        
    print("Topic assignment complete.")
    return content_topics_map

def generate_zettelkasten_files(output_dir, all_content, assigned_topics_map, content_embeddings):
    """Generates the Obsidian-ready Zettelkasten files."""
    if os.path.exists(output_dir):
        print(f"\nClearing existing output directory '{output_dir}'...")
        for root, dirs, files in os.walk(output_dir, topdown=False):
            for name in files: os.remove(os.path.join(root, name))
            for name in dirs: os.rmdir(os.path.join(root, name))
    os.makedirs(output_dir, exist_ok=True)
    print(f"Created output directory: '{output_dir}'")

    print(f"Generating {len(all_content)} notes...")
    # similarity_matrix = util.cos_sim(content_embeddings, content_embeddings) # Can be used for related links

    for i, data in enumerate(tqdm(all_content, desc="Generating Notes")):
        assigned_topics = assigned_topics_map[i]
        
        safe_title_text = re.sub(r'[^\w\s-]', '', data['title'][:40]).strip()
        filename = f"{data['date'].strftime('%Y%m%d%H%M%S')}-{safe_title_text}.md"

        topics_yaml_list = "\n".join([f"  - {topic}" for topic in assigned_topics])
        frontmatter = f"""---
date: {data['date'].isoformat()}
platform: {data['platform']}
topics:
{topics_yaml_list}
source: {data['source']}
---
"""
        body = f"# {data['title']}\n\n"
        if data['description']:
            body += f"{data['description']}\n\n"

        topics_link_section = "## Topics\n" + "\n".join([f"- [[{topic}]]" for topic in assigned_topics]) + "\n"
        body += topics_link_section
        
        tags_section = "\n## Tags\n"
        sanitized_tags = [f"#{re.sub(r'[^A-Za-z0-9]+', '', topic)}" for topic in assigned_topics]
        tags_section += " ".join(sanitized_tags)
        body += tags_section

        with open(os.path.join(output_dir, filename), 'w', encoding='utf-8') as f:
            f.write(frontmatter + body)
    
    print(f"\nSuccessfully generated {len(all_content)} notes in '{output_dir}'.")

def main():
    """Main function to execute the full thought-mapper pipeline."""
    print("--- Thought-Mapper v6.0: The Unified Knowledge Graph ---")
    
    topics = load_topics()
    if not topics: return

    # --- INGEST & STANDARDIZE ALL SOURCES ---
    twitter_content = parse_tweets_js()
    medium_content = parse_articles_txt()
    youtube_content = parse_youtube_json() # New data source
    
    all_content = twitter_content + medium_content + youtube_content
    
    if not all_content:
        print("\nNo content found from any source. Exiting.")
        return

    print(f"\nTotal items to process: {len(all_content)}")

    # --- PROCESS THE COMBINED DATA ---
    texts_for_embedding = [item['text_for_embedding'] for item in all_content]
    
    model = SentenceTransformer('all-MiniLM-L6-v2')
    content_embeddings = model.encode(texts_for_embedding, convert_to_tensor=True, show_progress_bar=True, title="Embedding All Content")
    topic_embeddings = model.encode(topics, convert_to_tensor=True, show_progress_bar=True, title="Embedding Topics")

    assigned_topics_map = assign_topics(content_embeddings, topic_embeddings, topics)

    # --- GENERATE THE FINAL VAULT ---
    generate_zettelkasten_files('obsidian_vault', all_content, assigned_topics_map, content_embeddings)

    print("\n--- Process Finished ---")

if __name__ == "__main__":
    main()