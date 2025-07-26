import json
import os
import re
from sentence_transformers import SentenceTransformer, util
import torch
from datetime import datetime
from tqdm import tqdm

# --- CONFIGURATION ---
TOPIC_THRESHOLD = 0.25 # How similar a tweet must be to a topic to be tagged (lower = more topics)
MAX_TOPICS_PER_TWEET = 3 # The maximum number of topics a single tweet can have

def load_topics(file_path='topics.txt'):
    """Loads a list of topics from a text file."""
    print(f"Loading topics from '{file_path}'...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            topics = [line.strip() for line in f if line.strip()]
        print(f"Found {len(topics)} topics.")
        return topics
    except FileNotFoundError:
        print(f"Error: '{file_path}' not found. Please create it and add your topics, one per line.")
        return None

def parse_tweets_js(file_path):
    """Parses the tweets.js file from a Twitter archive."""
    print(f"Parsing '{file_path}'...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return []

    start_index = content.find('[')
    end_index = content.rfind(']')
    if start_index == -1 or end_index == -1: return []

    json_data_str = content[start_index : end_index + 1]
    try:
        data = json.loads(json_data_str)
        tweets = [item['tweet'] for item in data if 'tweet' in item]
        print(f"Successfully parsed {len(tweets)} tweets.")
        return tweets
    except json.JSONDecodeError: return []

def clean_tweet_text(text):
    """Cleans the text of a tweet."""
    text = re.sub(r'https?:\/\/\S+', '', text)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'pic\.x\.com\/\S+', '', text)
    text = text.replace('\n', ' ')
    text = ' '.join(text.split())
    return text.strip()

def assign_topics_to_tweets(tweet_embeddings, topic_embeddings, topic_names):
    """Assigns topics to each tweet based on semantic similarity."""
    print("\nAssigning topics to all tweets...")
    
    cosine_scores = util.cos_sim(tweet_embeddings, topic_embeddings)
    
    tweet_to_topics_map = []
    for i in range(len(tweet_embeddings)):
        tweet_scores = cosine_scores[i]
        topic_score_pairs = list(zip(topic_names, tweet_scores))
        topic_score_pairs.sort(key=lambda x: x[1], reverse=True)
        
        assigned_topics = [
            topic for topic, score in topic_score_pairs if score > TOPIC_THRESHOLD
        ][:MAX_TOPICS_PER_TWEET]
        
        if not assigned_topics:
            assigned_topics = [topic_score_pairs[0][0]]
            
        tweet_to_topics_map.append(assigned_topics)
        
    print("Topic assignment complete.")
    return tweet_to_topics_map

def generate_zettelkasten_files(output_dir, all_tweets_data, tweet_topics, tweet_embeddings):
    """Generates the Obsidian-ready Zettelkasten files with structural topic links."""
    if os.path.exists(output_dir):
        print(f"\nClearing existing output directory '{output_dir}'...")
        for root, dirs, files in os.walk(output_dir, topdown=False):
            for name in files: os.remove(os.path.join(root, name))
            for name in dirs: os.rmdir(os.path.join(root, name))
    os.makedirs(output_dir, exist_ok=True)
    print(f"Created output directory: '{output_dir}'")

    print(f"Generating {len(all_tweets_data)} notes in Obsidian vault...")

    similarity_matrix = util.cos_sim(tweet_embeddings, tweet_embeddings)

    for i, data in enumerate(tqdm(all_tweets_data, desc="Generating Notes")):
        tweet_obj = data['raw']
        cleaned_text = data['cleaned']
        tweet_id = tweet_obj.get('id_str', str(i))
        topics = tweet_topics[i]
        
        date_obj = datetime.strptime(tweet_obj['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
        safe_title_text = re.sub(r'[^\w\s-]', '', cleaned_text[:40]).strip()
        filename = f"{date_obj.strftime('%Y%m%d%H%M%S')}-{safe_title_text}.md"

        # --- Frontmatter (For data queries) ---
        topics_yaml_list = "\n".join([f"  - {topic}" for topic in topics])
        frontmatter = f"""---
date: {date_obj.isoformat()}
topics:
{topics_yaml_list}
source: https://twitter.com/user/status/{tweet_id}
---
"""
        body = f"# {cleaned_text}\n\n"

        # --- Structural Links (For Graph View and Zettelkasten linking) ---
        # This is the new section that adds the [[Topic]] links
        topics_link_section = "## Topics\n"
        for topic in topics:
            topics_link_section += f"- [[{topic}]]\n"
        body += topics_link_section

        related_links_section = "\n## Related Thoughts\n"
        similar_indices = torch.topk(similarity_matrix[i], k=6).indices[1:]
        
        found_links = False
        for sim_index in similar_indices:
            if similarity_matrix[i][sim_index] > 0.65:
                sim_data = all_tweets_data[sim_index.item()]
                sim_cleaned_text = sim_data['cleaned']
                sim_date_obj = datetime.strptime(sim_data['raw']['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
                sim_safe_title = re.sub(r'[^\w\s-]', '', sim_cleaned_text[:40]).strip()
                sim_filename = f"{sim_date_obj.strftime('%Y%m%d%H%M%S')}-{sim_safe_title}.md"
                related_links_section += f"- [[{sim_filename}]]\n"
                found_links = True

        if found_links: body += related_links_section

        with open(os.path.join(output_dir, filename), 'w', encoding='utf-8') as f:
            f.write(frontmatter + body)
    
    print(f"\nSuccessfully generated {len(all_tweets_data)} notes in '{output_dir}'.")
    print("This version includes structural links for a rich graph view.")
    print("You can now open this folder as a vault in Obsidian!")

def main():
    """Main function to execute the full thought-mapper pipeline."""
    print("--- Thought-Mapper v2.1: Zettelkasten Gold Standard ---")
    
    topics = load_topics()
    if not topics: return

    raw_tweets = parse_tweets_js('tweets.js')
    if not raw_tweets: return

    all_tweets_data = []
    for tweet in raw_tweets:
        cleaned_text = clean_tweet_text(tweet.get('full_text', ''))
        if cleaned_text:
            all_tweets_data.append({'raw': tweet, 'cleaned': cleaned_text})

    cleaned_tweets = [data['cleaned'] for data in all_tweets_data]

    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    tweet_embeddings = model.encode(cleaned_tweets, convert_to_tensor=True, show_progress_bar=True, title="Embedding Tweets")
    topic_embeddings = model.encode(topics, convert_to_tensor=True, show_progress_bar=True, title="Embedding Topics")

    tweet_topics = assign_topics_to_tweets(tweet_embeddings, topic_embeddings, topics)

    generate_zettelkasten_files('obsidian_vault', all_tweets_data, tweet_topics, tweet_embeddings)

    print("\n--- Process Finished ---")

if __name__ == "__main__":
    main()