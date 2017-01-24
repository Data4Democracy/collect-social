from __future__ import print_function
from datetime import datetime
from collect_social.facebook.utils import get_graph, setup_db, update_user

import time


def update_reaction(db,reaction_data,post_id):
    interactions = db['interaction']
    interaction = interactions.find_one(post_id=post_id,user_id=reaction_data['id'])

    if not interaction:
        data = {
            'post_id': post_id,
            'type': reaction_data['type'],
            'author_id': reaction_data['id']
        }

        user_data = {
            'id': reaction_data['id'],
            'name': reaction_data['name']
        }

        update_user(db,user_data)
        interactions.insert(data, ensure=True)


def get_reactions(graph,db,post_id,i=0,after=None):
    limit = 10

    kwargs = {
        'path': '/'+str(post_id)+'/reactions',
        'limit': limit
    }

    if after:
        kwargs['after'] = after

    post_data = graph.get(**kwargs)
    post_reactions = post_data['data']

    for reaction in post_reactions:
        update_reaction(db,reaction,post_id)

        i += 1
        if i % 100 == 0:
            print('Finished ' + str(i) + ' reactions')

    if len(post_reactions) == limit:
        _after = post_data['paging']['cursors']['after']

        time.sleep(1)
        get_reactions(graph,db,post_id,i=i,after=_after)


def run(app_id,app_secret,connection_string,post_ids, i=0):
    db = setup_db(connection_string)
    graph = get_graph(app_id,app_secret)

    interactions = db['interaction']

    for post_id in post_ids:
        existing_reactions = interactions.find_one(post_id=post_id)
        if existing_reactions:
            continue
        get_reactions(graph,db,post_id)
        i += 1
        if i % 10 == 0:
            print('Finished ' + str(i) + ' posts')
