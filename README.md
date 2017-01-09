# Collect Social: Simply collect public social media content 

Getting content from social media data for analysis can be kind of a nuisance. This project aims to make that collection process as simple as possible, by making some common-sense assumptions about what most researchers need, and how they like to work with their data. For example, tasks like grabbing all the posts and comments from a handful of Facebook pages, and dumping the results into a sqlite database. 

Currently only Facebook is supported, but Twitter will follow shortly.

## Setup

This isn't on pypi yet, so first clone this repo into the directory where you'll be working. 

```bash
git clone https://github.com/Data4Democracy/collect-social.git
```

Then install the requirements using `pip`. 

```bash
pip install -r requirements.txt
```

## Usage

If you haven't already, make sure to create a [Facebook app](https://developers.facebook.com/docs/apps/register) with your Facebook developer account. This will give you an app id and app secret that you'll use to query Facebook's graph API.

Note that you'll only be able to retrieve content from public pages that allow API access. 

### Retrieving posts

You can retrieve posts using Facebook page ids. Note that the page id isn't the same as page name in the URL. For example [Justin Beiber's page name is JustinBieber](https://www.facebook.com/JustinBieber), but the page id is `67253243887`. You can find a page's id by looking at the source HTML at doing a ctrl+f (find in page) for `pageid`. [Here's a longer explanation](http://hellboundbloggers.com/2010/07/find-facebook-profile-and-page-id-8516/). 

```python
from collect_social.facebook get_posts

app_id = <YOUR APP ID>
app_secret = <YOUR APP SECRET>
connection_string = 'sqlite:///full-path-to-an-existing-database-file.sqlite'
page_ids = [<page id 1>,<page id 2>]

get_posts.run(app_id,app_secret,connection_string,page_ids)
```

This will run until it has collected all of the posts from each of the pages in your `page_ids` list. It will create `post`, `page`, and `user` tables in the sqlite database created in/opened from the file passed in `connection_string`. 

### Retrieving comments

This will retrieve all the comments (including threaded replies) for a list of posts. You can optionally provide a `max_comments` value, which is helpful if you're grabbing comments from the Facebook page of a public figure, where posts often get tens of thousands of comments.

```python
from collect_social.facebook import get_comments

app_id = <YOUR APP ID>
app_secret = <YOUR APP SECRET>
connection_string = 'sqlite:///full-path-to-an-existing-database-file.sqlite'
post_ids = [<post id 1>,<post id 2>]

get_comments.run(app_id,app_secret,connection_string,post_ids,max_comments=5000)
```

This will create `post`, `comment`, and `user` tables in the sqlite database created in/opened from the file passed in `connection_string`, assuming those tables don't already exist.

### Retrieving reactions

Reactions are "likes" and all the other happy/sad/angry/whatever responses that you can add to a Facebook post without actually typing a comment. The reaction `author_id` and `reaction_type` are saved to an `interaction` table in your sqlite database.

```python
from collect_social.facebook import get_reactions

app_id = <YOUR APP ID>
app_secret = <YOUR APP SECRET>
connection_string = 'sqlite:///full-path-to-an-existing-database-file.sqlite'
post_ids = [<post id 1>,<post id 2>]

get_reactions.run(app_id,app_secret,connection_string,post_ids,max_comments=5000)
```

More social media platforms coming soon. In the meantime, please [let me know](https://twitter.com/jonathonmorgan) if there's anything in particular you'd like to see. 

