#!/usr/bin/python
# -*- coding: utf-8 -*-

# A recommendation system. Based on (Segaran, 2007).

from math import sqrt

# A dictionary of movie reviews and their ratings of a small set of movies:
reviews_data_base = {
'Diana Sanchez': {'Lady in the Water': 2.5,
                  'Snakes on a Plane': 3.5,
                  'Just My Luck': 3.0,
                  'Superman Returns': 3.5,
                  'You, Me and Dupree': 2.5,
                  'The Night Listener': 3.0},
'Adam Zapata': {'Lady in the Water': 3.0,
                'Snakes on a Plane': 3.5,
                'Just My Luck': 1.5,
                'Superman Returns': 5.0,
                'The Night Listener': 3.0,
                'You, Me and Dupree': 3.5},
'Mariom Serfatty': {'Lady in the Water': 2.5,
                    'Snakes on a Plane': 3.0,
                    'Superman Returns': 3.5,
                    'The Night Listener': 4.0},
'Mariana Serfatty': {'Snakes on a Plane': 3.5,
                     'Just My Luck': 3.0,
                     'The Night Listener': 4.5,
                     'Superman Returns': 4.0,
                     'You, Me and Dupree': 2.5},
'Augusto Hernandez': {'Lady in the Water': 3.0,
                      'Snakes on a Plane': 4.0,
                      'Just My Luck': 2.0,
                      'Superman Returns': 3.0,
                      'The Night Listener': 3.0,
                      'You, Me and Dupree': 2.0},
'Alejandra Temprano': {'Lady in the Water': 3.0,
                       'Snakes on a Plane': 4.0,
                       'The Night Listener': 3.0,
                       'Superman Returns': 5.0,
                       'You, Me and Dupree': 3.5},
'Eduardo Sanchez': {'Snakes on a Plane':4.5,
                    'You, Me and Dupree':1.0,
                    'Superman Returns':4.0}}

#Returns a distance-based similarity score for person1 and person2.
def sim_distance(prefs, person1, person2):
    # Get the list of shared_items (si).
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1
    # If they have no rating in common, return 0.
    if len(si) == 0:
        return 0
    # Add up the squares of all the differences.
    sum_of_squares = \
      sum([pow(prefs[person1][item] - prefs[person2][item], 2)
          for item in prefs[person1] if item in prefs[person2]])

    return 1/(1 + sum_of_squares)

# Returns the Pearson correlation coefficient for p1 and p2.
def sim_pearson(prefs, p1, p2):
    # Get the list of mutually rated items, or shared items (si).
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1
    # Find the number of elements
    n = len(si)
    # If they are no ratings in common, return 0
    if n == 0:
        return 0
    # Add up all the preferences.
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])
    # Sum up the squares.
    sum1Sq = sum([pow(prefs[p1][it],2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it],2) for it in si])
    # Sum up the products
    pSum = sum([prefs[p1][it]*prefs[p2][it] for it in si])
    # Calculate Pearson score
    num = pSum - (sum1*sum2/n)
    den = sqrt((sum1Sq - pow(sum1, 2)/n)*(sum2Sq - pow(sum2, 2)/n))
    if den == 0:
        return 0
    r = num/den

    return r

# Returns the best matches for person from the preferences dictionary.
# Number of results and similarity functions are optional parameters.
def topMatches(prefs, person, n = 5, similarity = sim_pearson):
    scores = [(similarity(prefs, person, other), other)
              for other in prefs if other != person]
    # Sort the lists so the highest scores appear on at the top.
    scores.sort()
    scores.reverse()
    return scores[0:n]

# Gets recommendations for a person by using a weighted average of every other
# user's rankings.
def getRecommendations(prefs, person, similarity = sim_pearson):
    totals = {}
    simSums = {}
    for other in prefs:
        # Don't compare me to myself.
        if other == person: continue
        sim = similarity(prefs, person, other)
        # Ignore scores of zero or lower.
        if sim <= 0: continue
        for item in prefs[other]:
            # Only score movies I haven't seen yet.
            if item not in prefs[person] or prefs[person][item] == 0:
                # Similarity * Score
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item]*sim
                # Sum of similarities.
                simSums.setdefault(item,0)
                simSums[item] += sim
    # Create the normalized list.
    rankings = [(total/simSums[item], item) for item, total in totals.items()]
    # Return the sorted list.
    rankings.sort()
    rankings.reverse( )

    return rankings

# Transforms a data base by swapping the people and the items.
def transformPrefs(prefs):
    result={}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item,{})
            # Flip item and person.
            result[item][person] = prefs[person][item]

    return result

# Generates a data set of similar items.
def calculateSimilarItems(prefs, n = 10):
    # Create a dictionary of items showing which other items they are most
    # similar to.
    result = {}

    # Invert the preference matrix to be item-centric.
    itemPrefs = transformPrefs(prefs)
    c = 0
    for item in itemPrefs:
        # Status updates for large data sets.
        c += 1
        if c%100 == 0:
            print "%d / %d" % (c, len(itemPrefs))
        # Find the most similar items to this one.
        scores = topMatches(itemPrefs, item, n = n, similarity = sim_distance)
        result[item] = scores
    return result

def getRecommendedItems(prefs,itemMatch,user):
    userRatings=prefs[user]
    scores={}
    totalSim={}
    # Loop over items rated by this user
    for (item,rating) in userRatings.items( ):
        # Loop over items similar to this one
        for (similarity,item2) in itemMatch[item]:
            # Ignore if this user has already rated this item
            if item2 in userRatings: continue
            # Weighted sum of rating times similarity
            scores.setdefault(item2,0)
            scores[item2]+=similarity*rating
            # Sum of all the similarities
            totalSim.setdefault(item2,0)
            totalSim[item2]+=similarity
        # Divide each total score by total weighting to get an average
        rankings=[(score/totalSim[item],item) for item,score in scores.items( )]
    # Return the rankings from highest to lowest
    rankings.sort( )
    rankings.reverse( )
    return rankings

if __name__ == "__main__":

    #print(sim_distance(reviews_data_base, 'Diana Sanchez', 'Adam Zapata'))
    #print(sim_pearson(reviews_data_base, 'Diana Sanchez', 'Adam Zapata'))

    top = 3

    similar_people = topMatches(reviews_data_base, 'Eduardo Sanchez', top);

    print 'Top', top, 'people with closer taste in movies to yours:'
    ii = 1;
    for measure, people in similar_people:
        print "%d. %s" % (ii, people)
        ii += 1

    # We are interested in movie recommendations. How could we get them based on
    # the data base?

    # Our first approach could be to look at the person who has tastes more
    # similar to mine, and look for a movie he likes that I haven't seen yet.
    # However, this approach has the following problems:
    # 1. This person may not have yet seen movies that I might like.
    # 2. This person may be an outlier, since he may have strangely liked a
    # movie that no one else has liked according to topMatches.

    # We will therefore weight each rating based on that rating's person
    # similarity to the person we want to recommend the movies from. We take
    # a weighted sum and normalize over the sum of similarities, in order to
    # accidentally give more weight to a movie that has been reviewed by many
    # people.

    movie_recommendations = getRecommendations(reviews_data_base,
                                               'Eduardo Sanchez')

    print 'Top', top, 'movie recommendations for you based on people with' \
      ' similar taste in movies to yours:'
    ii = 1;
    for measure, movie in movie_recommendations:
        print "%d. %s" % (ii, movie)
        ii += 1

    # What if we want to see which movies are similar to each other?

    movies_data_base = transformPrefs(reviews_data_base)

    # We can now perform different queries...

    similar_movies = topMatches(movies_data_base, 'Superman Returns');

    print "People who have seen 'Superman Returns' also liked:"
    ii = 1;
    for measure, movie in similar_movies:
        if measure >= 0:
            print "%d. %s" % (ii, movie)
            ii += 1

    print "People who have seen 'Superman Returns' also hated:"
    ii = 1;
    for measure, movie in similar_movies:
        if measure < 0:
            print "%d. %s" % (ii, movie)
            ii += 1

    people_recommendation = getRecommendations(movies_data_base, 'Just My Luck')

    print "Best choices of guests to invite to go and see 'Just My Luck' are:"
    for measure, people in people_recommendation:
        print people

    itemsim = calculateSimilarItems(reviews_data_base)

    print('Similar items to each of the items:')
    print(itemsim)

    print('Recommendations for Eduardo Sanchez:')
    print(getRecommendedItems(reviews_data_base, itemsim, 'Eduardo Sanchez'))
