from flask import Flask, request, jsonify, render_template
from transformers import pipeline
import requests
import re
from dotenv import load_dotenv
from mira_sdk import MiraClient, Flow
import os
import time
from functools import wraps

load_dotenv(dotenv_path=".env")

app = Flask(__name__)
client = MiraClient(config={"API_KEY": "sb-85f5913affe3b2faafef48b20480d155"})

# Load Hugging Face models
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def fetch_trending_reddit(limit=15):
    """Fetch trending posts from multiple popular subreddits"""
    popular_subreddits = ['all', 'popular', 'news', 'worldnews', 'technology']
    all_posts = []
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    for subreddit in popular_subreddits:
        try:
            url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit}"
            response = requests.get(url, headers=headers)
            print(f"\n=== Reddit r/{subreddit} Response ===")
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                for post in data.get("data", {}).get("children", []):
                    post_data = post["data"]
                    # Skip stickied posts and posts with low scores
                    if post_data.get("stickied") or post_data.get("score", 0) < 1000:
                        continue
                        
                    all_posts.append({
                        'title': post_data["title"],
                        'text': post_data.get("selftext", ""),
                        'subreddit': post_data["subreddit"],
                        'score': post_data["score"],
                        'num_comments': post_data["num_comments"],
                        'url': post_data["url"],
                        'is_video': post_data["is_video"]
                    })
            
        except Exception as e:
            print(f"Error fetching from r/{subreddit}: {str(e)}")
            continue
    
    # Sort by score and remove duplicates
    all_posts.sort(key=lambda x: x['score'], reverse=True)
    unique_posts = []
    seen_titles = set()
    
    for post in all_posts:
        if post['title'] not in seen_titles:
            seen_titles.add(post['title'])
            unique_posts.append(post)
    
    print(f"\nTotal unique trending posts found: {len(unique_posts)}")
    return unique_posts

def preprocess_text(text):
    # Remove URLs
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    # Remove special characters but keep punctuation
    text = re.sub(r'[^\w\s.,!?]', '', text)
    # Normalize whitespace
    text = ' '.join(text.split())
    return text

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_trending', methods=['POST'])
def get_trending():
    try:
        # Fetch trending Reddit posts
        trending_posts = fetch_trending_reddit()
        
        # Process and analyze posts
        analyzed_posts = []
        
        for post in trending_posts[:10]:  # Analyze top 10 posts
            # Combine title and text
            full_text = f"{post['title']} {post['text']}"
            processed_text = preprocess_text(full_text)
            
            if len(processed_text.split()) < 10:
                processed_text = post['title']  # Use just title if text is too short
            
            # Truncate text for models
            sentiment_text = ' '.join(processed_text.split()[:500])
            summary_text = processed_text[:1024]
            
            try:
                summary = summarizer(summary_text, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
            except Exception as e:
                print(f"Error in summarization: {e}")
                summary = post['title']  # Use title as fallback
            
            try:
                sentiment = sentiment_analyzer(sentiment_text)[0]
            except Exception as e:
                print(f"Error in sentiment analysis: {e}")
                sentiment = {'label': 'NEUTRAL', 'score': 0.5}
            
            analyzed_posts.append({
                'title': post['title'],
                'subreddit': post['subreddit'],
                'score': post['score'],
                'comments': post['num_comments'],
                'summary': summary,
                'sentiment': sentiment,
                'url': post['url'],
                'is_video': post['is_video']
            })
        
        return jsonify({
            'status': 'success',
            'trending_posts': analyzed_posts
        })

    except Exception as e:
        print(f"\n!!! Error processing trending content: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/content')
def content_page():
    return render_template('content.html')

def retry_on_timeout(max_retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if "504" in str(e) and retries < max_retries - 1:
                        print(f"Attempt {retries + 1} failed, retrying in {delay} seconds...")
                        time.sleep(delay)
                        retries += 1
                    else:
                        raise e
            return func(*args, **kwargs)
        return wrapper
    return decorator

@app.route('/analyze_with_a0', methods=['POST'])
@retry_on_timeout(max_retries=3, delay=2)
def analyze_with_a0():
    try:
        data = request.json
        print("\n=== Starting Analysis ===")
        print("Received data:", data)
        
        # Load the flow from yaml
        try:
            flow = Flow(source="flow.yaml")
            print("Flow loaded successfully")
        except Exception as e:
            print("Error loading flow:", str(e))
            raise Exception(f"Failed to load flow configuration: {str(e)}")
        
        # Prepare input dictionary from the clicked post data
        input_dict = {
            "prime_input_1": data.get('summary', ''),
            "prime_input_2": str(data.get('sentiment_score', 0.5)),
            "prime_input_3": data.get('sentiment_label', 'NEUTRAL')
        }
        
        print("\nPrepared input:", input_dict)
        
        try:
            # Execute the flow without timeout
            print("\nExecuting flow...")
            response = client.flow.test(
                flow=flow,
                input_dict=input_dict
            )
            print("\nFlow execution completed")
            print("Response:", response)
            
        except Exception as e:
            print("\nError during flow execution:", str(e))
            if "504" in str(e):
                raise Exception("MIRA API timeout - please try again")
            raise Exception(f"Flow execution failed: {str(e)}")
        
        if not response:
            raise Exception("Empty response from MIRA API")
            
        # Extract outputs from the response
        try:
            outputs = response.get('output', [])
            print("\nExtracted outputs:", outputs)
            
            if not outputs:
                raise Exception("No content was generated")
            
            return jsonify({
                'status': 'success',
                'content_summary': outputs[0] if len(outputs) > 0 else 'No blog content generated',
                'reel_script': outputs[1] if len(outputs) > 1 else 'No reel script generated',
                'tweet_script': outputs[2] if len(outputs) > 2 else 'No tweet generated',
                'a0_analysis': response
            })
            
        except Exception as e:
            print("\nError processing response:", str(e))
            raise Exception(f"Failed to process API response: {str(e)}")

    except Exception as e:
        error_message = str(e)
        print(f"\n!!! Error in analyze_with_a0: {error_message}")
        
        if "504" in error_message:
            return jsonify({
                'status': 'error',
                'message': 'MIRA API is temporarily unavailable. Please try again later.',
                'error': 'Gateway Timeout'
            }), 504
        
        import traceback
        print("\nFull traceback:")
        print(traceback.format_exc())
        
        return jsonify({
            'status': 'error',
            'message': 'An error occurred while processing your request.',
            'error': error_message,
            'details': traceback.format_exc()
        }), 500


if __name__ == '__main__':
    app.run(debug=True)
