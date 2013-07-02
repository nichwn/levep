"""

Title:        nextSigReview

Description:  Identify the next review time for the earliest apprentice radical
              and kanji of the user's level 

Author:       Nicholas Brown

Email:        nichwn@gmail.com

Date Created: 2013-07-02

"""
import urllib
import json


def convertJSON(url):
    """
    Read a URL string and deserialise it as JSON.
    """
    return json.load(urllib.urlopen(url))

#Construct basic URL
api = "abd8edba52a2d02b7f4cc6ab328b47b8"  # TO-DO: save this value and load
baseURL = "http://www.wanikani.com/api/user/" + api

#Obtain user's level
url = baseURL + "/user-information"
userInfo = convertJSON(url)
level = userInfo["user_information"]["level"]

