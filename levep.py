"""

Title:        levep

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
import os.path


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


def getAPI(nokeyURL):
    """
    Grabs the user's API key, or requests and stores a new one from user input
    if it is not found.
    """
    fname = "api.dat"

    #Create the file to store the API key, if none exists.
    if not os.path.exists(fname):
        fl = open(fname, "w")
        api = reqAPI(nokeyURL)
        fl.write(api)
        print "\nSuccess! API key stored.\n\n"
        fl.close()
        return api

    #Read the stored API key
    fl = open(fname, "r+")
    return fl.read()


def reqAPI(nokeyURL):
    """
    Requests the user's API key.
    """
    while True:
        api = raw_input("Type your API key and press 'Enter'.\n")

        #API keys have 32 characters.
        if not len(api) == 32:
            print "\nInvalid API key. Please try again.\n\n"
        else:

            #Check that the correct API key was typed.
            try:
                jout = convertJSON(nokeyURL + api + "/user-information")
                user = jout["user_information"]["username"]
                crct = raw_input("\nAre you {}? If so, type 'Y'".format(user) +
                                 " and then press 'Enter', else just press " +
                                 "'Enter'.\n")
                if crct.upper() == "Y":
                    return api
                else:
                    print "Not you? Please try again.\n\n"

            #No user found for the given API key
            except:
                print ("\nNo user found for the API key provided. " +
                       "Please try again.\n\n")
                
        
#Construct basic URL
nokeyURL = "http://www.wanikani.com/api/user/"
api = getAPI(nokeyURL)
baseURL = nokeyURL + api

#Obtain user's level
url = baseURL + "/user-information"
userInfo = convertJSON(url)
level = userInfo["user_information"]["level"]

#Output the results
for inftype in INFTYPES:
    time = list_read(inftype, baseURL, level)
    if time is None:
        print "No unlocked {} for the current level.".format(inftype)
    else:
        if inftype == "radicals":
            inftype = "radical"
        print "Next {}: {} days {} hours {} minutes {} seconds".format(inftype,
                                                                       time[0],
                                                                       time[1],
                                                                       time[2],
                                                                       time[3])
