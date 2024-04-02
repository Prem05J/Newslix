import requests
from datetime import datetime, timedelta

class TwitterScraper:
    def __init__(self, bearer_token):
        self.bearer_token = bearer_token
        self.api_url = "https://api.twitter.com/2/tweets/search/recent"
        self.base_tweet_url = "https://twitter.com/user/status/"

    def create_headers(self):
        headers = {"Authorization": f"Bearer {self.bearer_token}"}
        return headers

    def create_params(self, keyword=None):
        # Calculate 'since' and 'until' dynamically to be 1 hour prior to the current time
        now = datetime.utcnow()
        since = (now - timedelta(hours=1)).isoformat("T") + "Z"
        until = (now - timedelta(seconds=10)).isoformat("T") + "Z"

        params = {
            "tweet.fields": "created_at,author_id",
            "expansions": "author_id",
            "user.fields": "name,username",
            "max_results": 10,  # Adjust accordingly, max is 100 for recent search
            "start_time": since,
            "end_time": until
        }

        if keyword:
            params['query'] = keyword

        return params

    def get_tweets(self, keyword=None):
        headers = self.create_headers()
        params = self.create_params(keyword)
        response = requests.get(self.api_url, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Request returned an error: {response.status_code}, {response.text}")

        tweets_data = response.json()
        data_list = self.parse_tweets(tweets_data, keyword)
        return data_list

    def parse_tweets(self, tweets_data, keyword):
        data_list = []
        users = {u["id"]: u for u in tweets_data["includes"]["users"]}  # Map of user IDs to user objects

        for tweet in tweets_data["data"]:
            print('tweet["created_at"] - ' + tweet["created_at"])
            tweet_dict = {
                "author": users[tweet["author_id"]]["name"],
                "publication": users[tweet["author_id"]]["username"],
                "date_publish": tweet["created_at"],
                "source_content": tweet["text"],
                "source_url": self.base_tweet_url + tweet["id"],
                "keywords": [keyword] if keyword else [],
                "states": []  # Not available directly from Twitter API without additional geolocation work
            }
            
            data_list.append(tweet_dict)

        return data_list
'''
# Example usage
bearer_token = "YOUR_BEARER_TOKEN_HERE"
scraper = TwitterScraper(bearer_token)

# Call without explicit 'since' and 'until', they are calculated dynamically to be 1 hour before now
data_list = scraper.get_tweets(keyword="modi")
for tweet in data_list:
    print(tweet)
'''
