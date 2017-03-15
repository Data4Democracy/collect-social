from __future__ import print_function

import dataset
from datetime import datetime

from collect_social.twitter.utils import get_api


def get_profiles(api, user_ids=None):
    profiles = api.UsersLookup(include_entities=False,
                               user_id=user_ids)

    return profiles


def upsert_profiles(db, profiles):
    user_table = db['user']
    for profile in profiles:
        data = {
            'user_id': profile.id,
            'profile_collected': 1
        }

        profile_props = [
            'contributors_enabled',
            'created_at',
            'default_profile',
            'default_profile_image',
            'description',
            'favourites_count',
            'followers_count',
            'friends_count',
            'geo_enabled',
            'lang',
            'listed_count',
            'location',
            'name',
            'profile_background_color',
            'profile_background_image_url',
            'profile_background_tile',
            'profile_banner_url',
            'profile_image_url',
            'profile_link_color',
            'profile_sidebar_fill_color',
            'profile_text_color',
            'protected',
            'screen_name',
            'statuses_count',
            'time_zone',
            'url',
            'utc_offset',
            'verified'
        ]

        for key in profile_props:
            data[key] = getattr(profile, key)

        user_table.upsert(data, ['user_id'])


def collect_new_profiles(db):
    user_table = db['user']

    users = user_table.find(user_table.table.columns.user_id != 0,
                            profile_collected=0)
    users = [u for u in users]
    return users


def run(api, connection_string):
    """
    Collect profiles
    """

    db = dataset.connect(connection_string)

    new_users = collect_new_profiles(db)

    if not new_users:
        print("No new profiles found")
        return None

    ids_to_lookup = []
    ids_remain = len(new_users)
    for user in new_users:
        ids_to_lookup.append(user['user_id'])
        if len(ids_to_lookup) >= 100:
            print('Getting profiles')
            profiles = get_profiles(api, user_ids=ids_to_lookup)

            print('Updating 100 profiles')
            upsert_profiles(db, profiles)
            ids_to_lookup = []
            ids_remain -= 100

            print('Users remaining {}'.format(ids_remain))
            print('Sleeping, timestamp: {}'.format(datetime.now()))
            # time.sleep(5)

    print('Getting profiles')
    profiles = get_profiles(api, user_ids=ids_to_lookup)
    print('Updating ' + str(len(ids_to_lookup)) + ' profiles')
    upsert_profiles(db, profiles)

    print('Finished getting profiles')
