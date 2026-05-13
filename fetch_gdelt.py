import requests
import pandas as pd
import json

def fetch_gdelt_news():
    """
    Fetches news articles from GDELT DOC API for Mudug/Somalia.
    """
    print("Querying GDELT DOC API for Mudug/Somalia...")
    url = 'https://api.gdeltproject.org/api/v2/doc/doc'
    params = {
        'query': 'Mudug Somalia Conflict',
        'mode': 'artlist',
        'format': 'json',
        'timespan': '3m' # Last 3 months for better volume
    }
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, params=params, headers=headers)
        r.raise_for_status()
        if 'json' in r.headers.get('Content-Type', ''):
            data = r.json()
            articles = data.get('articles', [])
            print(f"Found {len(articles)} articles.")
            return articles
        else:
            print("Response was not JSON. Rate limit might be hit.")
            return []
    except Exception as e:
        print(f"Error fetching from GDELT: {e}")
        return []

def save_news(articles):
    if not articles:
        # Create empty if nothing found
        with open('news_data.js', 'w') as f:
            f.write('const newsData = [];\n')
        return
    
    # Save CSV
    df = pd.DataFrame(articles)
    df.to_csv('gdelt_mudug_news.csv', index=False)
    
    # Save JS for landing page
    with open('news_data.js', 'w') as f:
        f.write('const newsData = ' + json.dumps(articles) + ';\n')
    
    print("Saved news to gdelt_mudug_news.csv and news_data.js")

if __name__ == "__main__":
    articles = fetch_gdelt_news()
    save_news(articles)
