#!/usr/bin/python
# -*- coding: utf-8 -*-

# A del.icio.us Link recommender. Based on (Segaran, 2007).

import time
from pydelicious import get_popular, get_userposts, get_urlposts
import random

# Initializes a dictionary of users who have recently posted a popular link with
# a specified tag.
def initializeUserDict(tag, count = 5):
    user_dict = {}
    # Get the top count popular posts.
    for p1 in get_popular(tag = tag)[0:count]:
        # Find all the users who posted this.
        for p2 in get_urlposts(p1['url']):
            user = p2['user']
            user_dict[user] = {}
    return user_dict

# Function to fill in the ratings for all the users.
def fillItems(user_dict):
    all_items = {}
    # Find links posted by all users.
    for user in user_dict:
        for i in range(3):
            try:
                posts = get_userposts(user)
                break
            except:
                print "Failed user " + user + ", retrying..."
                time.sleep(4)
        for post in posts:
            url = post['url']
            user_dict[user][url] = 1
            all_items[url] = 1
    # Fill in missing items with 0.
    for ratings in user_dict.values():
        for item in all_items:
            if item not in ratings:
                ratings[item] = 0.0

if __name__ == "__main__":

    delusers = initializeUserDict('programming')
    print(delusers)
    fillItems(delusers)

    # Find a random users and find other users who have similar tastes to his.
    user = delusers.keys()[random.randint(0, len(delusers) - 1)]
    print(user)
    print(recommendations.topMatches(delusers, user))

    # Get recommendations for links for this user.
    print(recommendations.getRecommendations(delusers, user)[0:10])

    # Find a set of links similar to one that you found interesting.
    url = recommendations.getRecommendations(delusers, user)[0][1]
    recommendations.topMatches(recommendations.transformPrefs(delusers), url)
