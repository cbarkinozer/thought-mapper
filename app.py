import json
import re
from sentence_transformers import SentenceTransformer, util
import torch

def parse_tweets_js(file_path):
    """
    Parses the tweets.js file from a Twitter archive to extract tweet data.

    Args:
        file_path (str): The path to the tweets.js file.

    Returns:
        list: A list of tweet objects (dictionaries), or an empty list if an error occurs.
    """
    print(f"Attempting to read and parse '{file_path}'...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        print("Please ensure your 'tweets.js' file is in the same directory as this script.")
        return []

    start_index = content.find('[')
    end_index = content.rfind(']')

    if start_index == -1 or end_index == -1:
        print("Error: Could not find the JSON data array (enclosed in '[]') in the .js file.")
        return []

    json_data_str = content[start_index : end_index + 1]

    try:
        data = json.loads(json_data_str)
        tweets = [item['tweet'] for item in data if 'tweet' in item]
        print(f"Successfully parsed {len(tweets)} tweets.")
        return tweets
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from the file: {e}")
        return []

def clean_tweet_text(text):
    """
    Cleans the text of a tweet by removing URLs, mentions, and extra whitespace.
    Hashtags are preserved for later analysis.

    Args:
        text (str): The raw tweet text.

    Returns:
        str: The cleaned tweet text.
    """
    text = re.sub(r'https?:\/\/\S+', '', text)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'pic\.x\.com\/\S+', '', text)
    text = text.replace('\n', ' ')
    text = ' '.join(text.split())
    return text.strip()

def generate_embeddings(texts, model):
    """
    Generates sentence embeddings for a list of texts using a SentenceTransformer model.

    Args:
        texts (list): A list of strings to be embedded.
        model (SentenceTransformer): The loaded sentence transformer model.

    Returns:
        torch.Tensor: A tensor containing the embeddings.
    """
    print(f"\nGenerating embeddings for {len(texts)} tweets... (This may take a moment)")
    # Using encode() which is optimized for performance. It will show a progress bar.
    embeddings = model.encode(texts, convert_to_tensor=True, show_progress_bar=True)
    print("Embeddings generated successfully.")
    return embeddings

def main():
    """
    Main function to execute the tweet processing and analysis pipeline.
    """
    print("--- Thought-Mapper v0.2: Initializing ---")
    print("Step 1: Tweet Extraction and Cleaning")
    tweets_js_path = 'tweets.js'
    raw_tweets = parse_tweets_js(tweets_js_path)

    if not raw_tweets:
        print("\nProcessing halted. Please check errors above.")
        return

    # Create a list of cleaned tweet texts for analysis
    cleaned_tweets = [clean_tweet_text(tweet.get('full_text', '')) for tweet in raw_tweets]
    
    # Filter out any empty strings that might result from cleaning
    original_and_cleaned = [
        (raw_tweets[i], cleaned) 
        for i, cleaned in enumerate(cleaned_tweets) if cleaned
    ]
    if not original_and_cleaned:
        print("\nError: No valid tweet text found after cleaning. Cannot proceed.")
        return

    # Unpack the lists
    raw_tweets, cleaned_tweets = zip(*original_and_cleaned)
    raw_tweets, cleaned_tweets = list(raw_tweets), list(cleaned_tweets)


    print(f"\nStep 2: AI Model Loading & Semantic Analysis")
    # Load a pre-trained model. 'all-MiniLM-L6-v2' is a great starting point: fast and high quality.
    print("Loading Sentence Transformer model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("Model loaded.")

    # Generate embeddings for all cleaned tweets
    tweet_embeddings = generate_embeddings(cleaned_tweets, model)

    # --- DEMONSTRATION: Find tweets similar to the very first tweet ---
    print("\n--- Semantic Similarity Demonstration ---")
    if len(cleaned_tweets) > 1:
        # The tweet we want to find similarities for
        target_tweet_index = 0
        target_tweet_text = cleaned_tweets[target_tweet_index]
        target_embedding = tweet_embeddings[target_tweet_index]

        print(f"\nFinding tweets similar to your first tweet:")
        print(f"  > \"{target_tweet_text}\"")

        # Compute cosine similarity between the target tweet and all other tweets
        # We exclude the target tweet itself from the comparison pool
        other_embeddings = torch.cat((tweet_embeddings[:target_tweet_index], tweet_embeddings[target_tweet_index+1:]))
        other_texts = cleaned_tweets[:target_tweet_index] + cleaned_tweets[target_tweet_index+1:]

        cosine_scores = util.cos_sim(target_embedding, other_embeddings)[0]
        
        # Get the top 5 most similar tweets
        top_results = torch.topk(cosine_scores, k=min(5, len(other_texts)))

        print("\nTop 5 most similar tweets found:")
        for i, (score, idx) in enumerate(zip(top_results[0], top_results[1])):
            print(f"  {i+1}. (Score: {score:.4f}) - \"{other_texts[idx]}\"")

    print("\n--- End of Demonstration ---")
    print("\nNext we will use these embeddings for clustering and full graph generation.")
    print("--- Process Finished ---")

if __name__ == "__main__":
    main()