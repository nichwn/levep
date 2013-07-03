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
from datetime import datetime
import calendar


INFTYPES = ["radicals", "kanji"]

def convertJSON(url):
    """
    Read a URL string and deserialise it as JSON.
    """
    return json.load(urllib.urlopen(url))


def list_read(inftype, baseURL, level):
    """
    Return length of time until the soonest, current level's radical or kanji.
    """
    url = baseURL + "/{}/{}".format(inftype, level)
    jout = convertJSON(url)

    #Identify the lowest available date
    av_dates = [jout["requested_information"][i]["stats"]["available_date"]
                for i in range(len(jout["requested_information"]))
                if jout["requested_information"][i]["stats"] is not None]
    try:
        lowest = min(av_dates)
    except:
        return None  # no unlocked inftype for the current level

    #Identify the current time
    ctime = datetime.utcnow()
    cunix = calendar.timegm(ctime.utctimetuple())

    #Calculate the next review time
    revnext = int(lowest) - cunix
    if revnext < 0:
        revnext = 0

    #Convert to a more readable format
    seconds = revnext % 60
    minutes = revnext / 60 % 60
    hours = revnext / 3600 % 24
    days = revnext / 86400

    return (days, hours, minutes, seconds)
        
#Construct basic URL
api = "abd8edba52a2d02b7f4cc6ab328b47b8"  # TO-DO: save this value and load
baseURL = "http://www.wanikani.com/api/user/" + api

#Obtain user's level
url = baseURL + "/user-information"
userInfo = convertJSON(url)
level = userInfo["user_information"]["level"]
