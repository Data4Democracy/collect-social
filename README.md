# Collect Social: Simply collect public social media content

[![Build Status](https://travis-ci.org/Data4Democracy/collect-social.svg?branch=master)](https://travis-ci.org/Data4Democracy/collect-social)


**Maintainers:** Maintainers have write access to the repository. They are responsible for reviewing pull requests, providing feedback and ensuring consistency.

* [@bstarling](https://datafordemocracy.slack.com/messages/@bstarling/)
* [@nick](https://datafordemocracy.slack.com/messages/@nick/)
* [@asragab](https://datafordemocracy.slack.com/messages/@asragab/)
* [@metame](https://datafordemocracy.slack.com/messages/@metame/)


## Purpose:
Collecting social media data for analysis can be kind of a nuisance. This project aims to make that collection process as simple as possible, by making some common-sense assumptions about what most researchers need, and how they like to work with their data. Collect social sits on top of other python libraries such as facepy (facebook) and tweepy (twitter). Our purpose is to take care of low level details and provide a clean API for working across multiple platforms.


## Philosophy:
Our goal is to make it as **easy as possible** for researchers to get up and running with new collections. Our focus is on ease of use over maximum features. At every decision point we should carefully consider how a new feature will impact simplicity. A user should be able to use collect-social without prior knowledge of underlying libraries and APIs. Based on our experience of underlying API we will attempt to make the best decision that should work in average case but if you are looking for maximum control over your collection process, consider using underlying libraries directly.


## Roadmap:
* Our current to-do can be found here [here](https://github.com/Data4Democracy/collect-social/projects/4)
* Command line interface
* [Eventador](https://github.com/Data4Democracy/assemble/tree/master/eventador) integration.
* Refactor facebook API to match twitter.
* Save data to sqlite.
* Flat file exports (JSON).
* Option to upload file output to designated s3 bucket.


#### First class platforms
* Facebook
* Twitter

#### Platforms we will potentially support in future
These are platforms we will consider supporting in the future. These will not be built out until we are happy with our implementation of facebook/twitter. If you are familiar with any of these platforms and would like to put together a proof of concept in a separate repository we welcome input.

* Reddit
* Disqus
* voat.co
* 4chan/8chan etc.

## Getting Started
If you are looking to get started contributing please see our contributor guide.
TODO - write guide

### Installation:
Collect-social is built to run on python 3.6.

`git clone https://github.com/Data4Democracy/collect-social.git`

Then install as a package using `pip`. This will allow you import `collect_social` from any python script.

```bash
cd collect-social
pip install -r requirements.txt
pip install .
```

## Usage

TODO: Explain settings file

### Facebook

If you haven't already, make sure to create a [Facebook app](https://developers.facebook.com/docs/apps/register) with your Facebook developer account. This will give you an app id and app secret that you'll use to query Facebook's graph API.

Note that you'll only be able to retrieve content from public pages that allow API access.

#### Retrieving posts
**Caution** work in progress. This will change as part of our ongoing refactor. We do not suggest anyone use this for now.

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
**Caution** work in progress. This will change as part of our ongoing refactor. We do not suggest anyone use this for now.

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
**Caution** work in progress. This will change as part of our ongoing refactor. We do not suggest anyone use this for now.

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

#### API

TODO: Document API
