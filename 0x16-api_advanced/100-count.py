#!/usr/bin/python3
"""Function to count words in all hot posts of a given Reddit subreddit."""
import requests

def count_words(subreddit, word_list, instances=None, after="", count=0):
    """Prints counts of given words found in hot posts of a given subreddit.

    Args:
        subreddit (str): The subreddit to search.
        word_list (list): The list of words to search for in post titles.
        instances (dict): Key/value pairs of words/counts.
        after (str): The parameter for the next page of the API results.
        count (int): The parameter of results matched thus far.
    """
    if instances is None:
        instances = {}  # Initialize instances dictionary

    url = f"https://www.reddit.com/r/{subreddit}/hot/.json"
    headers = {
        "User-Agent": "linux:0x16.api.advanced:v1.0.0 (by /u/bdov_)"
    }
    params = {
        "after": after,
        "count": count,
        "limit": 100
    }
    response = requests.get(url, headers=headers, params=params,
                            allow_redirects=False)

    try:
        response.raise_for_status()  # Check for HTTP errors
        results = response.json()["data"]
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return

    after = results.get("after")
    count += results.get("dist")
    for c in results.get("children"):
        title = c.get("data").get("title").lower().split()
        for word in word_list:
            if word.lower() in title:
                times = title.count(word.lower())
                instances[word] = instances.get(word, 0) + times

    if after is None:
        if not instances:
            print("No instances found.")
        else:
            instances_sorted = sorted(instances.items(),
                                      key=lambda kv: (-kv[1], kv[0]))
            for word, count in instances_sorted:
                print(f"{word}: {count}")
    else:
        count_words(subreddit, word_list, instances, after, count)

# Example usage:
subreddit_name = "learnprogramming"
word_list = ["python", "programming", "code"]
count_words(subreddit_name, word_list)
)
