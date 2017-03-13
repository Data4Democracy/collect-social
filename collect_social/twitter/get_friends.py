from __future__ import print_function
 
import dataset
import twitter
import sys
import time
 
from collect_social.twitter.utils import get_api, insert_if_missing
from datetime import datetime
 
 
def get_friend_ids(api,count=5000,screen_name=None,cursor=-1):
    next,prev,follower_ids = api.GetFriendIDsPaged(screen_name=screen_name,
                            cursor=cursor,
                            count=count)
 
    return next,prev,follower_ids
 
 
def create_connections(db,user_id,friend_ids=[]):
    connection_table = db['connection']
 
    for _id in friend_ids:
        connection = connection_table.find_one(friend_id=_id,
                                                follower_id=user_id)
        if not connection:
            data = dict(friend_id=_id,follower_id=user_id)
            connection_table.insert(data, ensure=True)
 
 
def run(consumer_key, consumer_secret, access_key, access_secret, 
        connection_string, threshold=5000, seed_only=True):
 
    db = dataset.connect(connection_string)
    api = get_api(consumer_key, consumer_secret, access_key, access_secret)
    
    if seed_only:
        is_seed = 1
    else:
        is_seed = 0

    user_table = db['user']
    users = user_table.find(user_table.table.columns.friends_count < threshold,
                            friends_collected=0, is_seed=is_seed)
    users = [u for u in users]
    all_users = len(users)
    remaining = all_users
 
    for u in users:
        try:
            print('Getting friend ids for ' + u['screen_name'])
            next,prev,friend_ids = get_friend_ids(api, screen_name=u['screen_name'])
 
            print('Adding ' + str(len(friend_ids)) + ' user ids to db')
            insert_if_missing(db,user_ids=friend_ids)
 
            print('Creating relationships for ' + str(u['user_id']))
            create_connections(db,u['user_id'],friend_ids=friend_ids)
 
            update_dict = dict(id=u['id'],friends_collected=1)
            user_table.update(update_dict,['id'])
 
            # Can only make 15 calls in a 15 minute window to this endpoint
            remaining -= 1
            time_left = remaining / 60.0
            print(str(time_left) + ' hours to go')
            print('Sleeping for 1 minute, timestamp: ' + str(datetime.now()))
            time.sleep(60)
        except:
            continue
