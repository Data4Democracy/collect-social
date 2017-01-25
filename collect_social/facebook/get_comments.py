from __future__ import print_function
from datetime import datetime
from collect_social.facebook.utils import get_graph, setup_db, update_user

import time


def update_comment(db,comment_data,post_id,parent=None):
    comments = db['comment']
    comment = comments.find_one(comment_id=comment_data['id'])

    if not comment:
        fields = [
                    'comment_count',
                    'created_time',
                    'like_count',
                    'message'
                ]

        data = {
            'post_id': post_id,
            'comment_id': comment_data['id']
        }

        if parent:
            data['parent_id'] = parent

        author_id = None
        if 'from' in comment_data and 'id' in comment_data['from']:
            data['author_id'] = comment_data['from']['id']
            author_id = data['author_id']
            update_user(db,comment_data['from'])

        for f in fields:
            if f in comment_data:
                data[f] = comment_data[f]


        comments.insert(data, ensure=True)


def get_comments(graph,db,post_id,i=0,after=None,parent=None,max_comments=5000):
    limit = 100
    max_comments = 5000

    kwargs = {
        'path': '/'+str(post_id)+'/comments',
        'limit': limit
    }

    if after:
        kwargs['after'] = after

    try:
        post_data = graph.get(**kwargs)
        post_comments = post_data['data']

        for comment in post_comments:
            update_comment(db,comment,post_id,parent=parent)

            if not parent:
                i += 1
                if i % 100 == 0:
                    print('Finished ' + str(i) + ' comments')

                if i > max_comments:
                    return

            if not parent and 'comment_count' in comment and \
                comment['comment_count'] > 0:
                get_comments(graph,db,comment['id'],parent=comment['id'])

        if len(post_comments) == limit:
            _after = post_data['paging']['cursors']['after']

            time.sleep(1)
            get_comments(graph,db,post_id,i=i,after=_after,parent=parent)
    except Exception as e:
        print(e)
        pass


def run(app_id,app_secret,connection_string,post_ids,max_comments=5000, i=0):
    db = setup_db(connection_string)
    graph = get_graph(app_id,app_secret)

    comments = db['comment']

    for post_id in post_ids:
        i += 1
        existing_comments = comments.find_one(post_id=post_id)
        if existing_comments:
            continue
        get_comments(graph,db,post_id)
        if i % 10 == 0:
            print('Finished ' + str(i) + ' posts')
