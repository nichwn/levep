import urllib
import json
from datetime import datetime
import calendar
import os.path


def main():
    #API key storage location
    FNAME = "api.dat"

    #Construct basic URL
    nokeyURL = "http://www.wanikani.com/api/user/"
    api = getAPI(FNAME, nokeyURL)
    baseURL = nokeyURL + api

    #Obtain user's level
    level = lev_cal(baseURL)

    #Output the length of time
    resout(baseURL, level)

    #Check if the user wants to change their API key.
    inp = raw_input("\nDid you want to change your API key? If so, type " +
                    "'reset' and press 'Enter'. Else, just press 'Enter' " +
                    "to close the program.\n")
    if inp.lower() == "reset":
        os.remove(FNAME)
        print
        main()


def convertJSON(url):
    """
    Read a URL string and deserialise it as JSON.
    """
    return json.load(urllib.urlopen(url))


def lev_cal(baseURL):
    """
    Obtain's the user's level.
    """
    url = baseURL + "/user-information"
    userInfo = convertJSON(url)
    return userInfo["user_information"]["level"]


def list_read(inftype, baseURL, level):
    """
    Return length of time until the soonest, current level's radical or kanji.
    """
    SEC_PER_MIN = 60
    MIN_PER_HOUR = 60
    HOUR_PER_DAY = 24
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
    if revnext <= 0:
        return "available"  # reviews are currently available

    #Convert to a more readable format
    seconds = revnext % SEC_PER_MIN
    minutes = revnext / SEC_PER_MIN % MIN_PER_HOUR
    hours = revnext / (SEC_PER_MIN * MIN_PER_HOUR) % HOUR_PER_DAY
    days = revnext / (SEC_PER_MIN * MIN_PER_HOUR * HOUR_PER_DAY)

    return (days, hours, minutes, seconds)


def getAPI(fname, nokeyURL):
    """
    Grabs the user's API key, or requests and stores a new one from user input
    if it is not found.
    """
    fl = open(fname, "a").close()  # create an empty file if none exists
    fl = open(fname, "r+")
    data = fl.read()

    #Store the API key, if none exists.
    if not data:
        api = reqAPI(nokeyURL)
        fl.write(api)
        print "\nSuccess! API key stored.\n\n"
        fl.close()
        return api

    #Read the stored API key
    return data


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


def resout(baseURL, level):
    """
    Outputs the length of time until the soonest, current level's radicals
    and kanji.
    """
    INFTYPES = ["radicals", "kanji"]
    for inftype in INFTYPES:
        time = list_read(inftype, baseURL, level)

        #Output the length of time
        if time is None:
            print "No unlocked {} for the current level.".format(inftype)
        elif time == "available":
            print "There are {} available for review!".format(inftype)
        else:
            if inftype == "radicals":
                inftype = "radical"
            print ("Next {}: {} days ".format(inftype, time[0]) +
                   "{} hours {} minutes {} seconds".format(time[1], time[2],
                                                           time[3]))

if __name__ == "__main__":
    main()
