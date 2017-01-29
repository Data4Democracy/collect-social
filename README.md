# Collect Social: Simply collect public social media content 

[![Build Status](https://travis-ci.org/Data4Democracy/collect-social.svg?branch=master)](https://travis-ci.org/Data4Democracy/collect-social)

Getting content from social media data for analysis can be kind of a nuisance. This project aims to make that collection process as simple as possible, by making some common-sense assumptions about what most researchers need, and how they like to work with their data. For example, tasks like grabbing all the posts and comments from a handful of Facebook pages, and dumping the results into a sqlite database. 


## Setup

```bash
git clone https://github.com/Data4Democracy/collect-social.git
```

Then install the package using `pip`. This will allow you import `collect_social` from any python script.

```bash
cd collect-social
pip install -r requirements.txt
pip install .
```

### Testing

To run tests only:
```bash
pytest
```

To run tests with coverage report use shell script:
```bash
./run_tests
```

Contributors should add tests to the `tests` directory.

## Usage

### Facebook

If you haven't already, make sure to create a [Facebook app](https://developers.facebook.com/docs/apps/register) with your Facebook developer account. This will give you an app id and app secret that you'll use to query Facebook's graph API.

Note that you'll only be able to retrieve content from public pages that allow API access. 

#### Retrieving posts

You can retrieve posts using Facebook page ids. Note that the page id isn't the same as page name in the URL. For example [Justin Beiber's page name is JustinBieber](https://www.facebook.com/JustinBieber), but the page id is `67253243887`. You can find a page's id by looking at the source HTML at doing a ctrl+f (find in page) for `pageid`. [Here's a longer explanation](http://hellboundbloggers.com/2010/07/find-facebook-profile-and-page-id-8516/). 

```python
from collect_social.facebook import get_posts

app_id = '<YOUR APP ID>'
app_secret = '<YOUR APP SECRET>'
connection_string = 'sqlite:////full/path/to/a/database-file.sqlite'
page_ids = ['<page id 1>','<page id 2>']

get_posts.run(app_id,app_secret,connection_string,page_ids)
```

This will run until it has collected all of the posts from each of the pages in your `page_ids` list. It will create `post`, `page`, and `user` tables in the sqlite database from the file passed in `connection_string`. 
The database will be created if it does not already exist.
Note: The `app_id`, `app_secret` and elements in the `page_ids` list are all strings, and should be quoted (' ' or " ").

If you like, quickly check the success of your program by viewing the first 10 posts:

```shell
sqlite3 database-file.sqlite "SELECT  message FROM post LIMIT 10"
```

#### Retrieving comments

This will retrieve all the comments (including threaded replies) for a list of posts. You can optionally provide a `max_comments` value, which is helpful if you're grabbing comments from the Facebook page of a public figure, where posts often get tens of thousands of comments.

```python
from collect_social.facebook import get_comments

app_id = '<YOUR APP ID>'
app_secret = '<YOUR APP SECRET>'
connection_string = 'sqlite:////full/path/to/a/database-file.sqlite'
post_ids = ['<post id 1>','<post id 2>']

get_comments.run(app_id,app_secret,connection_string,post_ids,max_comments=5000)
```

This will create `post`, `comment`, and `user` tables in the sqlite database created in/opened from the file passed in `connection_string`, assuming those tables don't already exist.

#### Retrieving reactions

Reactions are "likes" and all the other happy/sad/angry/whatever responses that you can add to a Facebook post without actually typing a comment. The reaction `author_id` and `reaction_type` are saved to an `interaction` table in your sqlite database.

```python
from collect_social.facebook import get_reactions

app_id = '<YOUR APP ID>'
app_secret = '<YOUR APP SECRET>'
connection_string = 'sqlite:////full/path/to/a/database-file.sqlite'
post_ids = ['<post id 1>','<post id 2>']

get_reactions.run(app_id,app_secret,connection_string,post_ids,max_comments=5000)
```

### Twitter

If you haven't already, make sure to create a [Twitter app](https://apps.twitter.com/) with your Twitter account. This will give you an access token, access token secret, consumer key, and consumer secret that will be required to query the Twitter API.

#### Search Tweets

This will search tweets based on the query string specified in `topics` and store it in a `tweet` table in the sqlite database specified.

```python
from collect_social.twitter import search_tweets

ACCESS_TOKEN = '<YOUR ACCESS TOKEN>'
ACCESS_TOKEN_SECRET = '<YOUR ACCESS TOKEN SECRET>'
CONSUMER_KEY = '<YOUR CONSUMER KEY>'
CONSUMER_SECRET = 'YOUR CONSUMER SECRET>'
connection_string = 'sqlite:////full/path/to/a/database-file.sqlite'
topics = ['<hashtag or string to search for>']

search_tweets.run(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET,connection_string,topics,count=100)
```
You can reference [`tweet_model.py`](collect_social/twitter/tweet_model.py) to see what fields are stored. 
Twitter topic streaming coming soon.

More social media platforms coming soon. In the meantime, please [let me know](https://twitter.com/jonathonmorgan) if there's anything in particular you'd like to see. 

