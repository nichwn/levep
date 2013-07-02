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


def convertJSON(url):
    """
    Read a URL string and deserialise it as JSON.
    """
    return json.load(urllib.urlopen(url))


def listRead(infotype, baseURL, level):
    """
    Return length of time until the soonest, current level's radical or kanji.
    """
    #TO-DO: Test this
    url = baseURL + "/{}/{}".format(infotype, level)
    jout = convertJSON(url)

    #Identify the lowest available date
    av_dates = [jout["requested_information"][i]["stats"]["available_date"]
                for i in range(len(jout["requested_information"]))]
    lowest = min(av_dates)

    #Identify the current time
    ctime = datetime.utcnow()
    cunix = calendar.timegm(ctime.utctimetuple())

    #Calculate the next review time
    revnext = cunix - int(lowest)
    if revnext < 0:
        revnext = 0

    #Convert to a more readable format
    days = hours = minutes = seconds = 0
    seconds = revnext % 60
    revnextmin = revnext / 60
    if revnextmin >= 60:
        minutes = revnextmin % 60
        revnexthr = revnextmin / 60
        if revnexthr >= 60:
            hours = revnexthr % 24
            days = revnexthr / 24
        else:
            hours = revnexthr
    else:
        minutes = revnextmin

    return (days, hours, minutes, seconds)
        
#Construct basic URL
api = "abd8edba52a2d02b7f4cc6ab328b47b8"  # TO-DO: save this value and load
baseURL = "http://www.wanikani.com/api/user/" + api

#Obtain user's level
url = baseURL + "/user-information"
userInfo = convertJSON(url)
level = userInfo["user_information"]["level"]

