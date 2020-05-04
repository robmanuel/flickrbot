# -*- coding: utf-8 -*-

# FlickrBot
# 
# This code will pick a random photo from a Flickr user and post it on Twitter
# 
# Made by Rob Manuel from a request by Paul Clarke

import flickr_api,random,tweepy,argparse

#what Flickr user are we looking for?
id="paul_clarke"

# Set your flickr API keys here:
# Get them at https://www.flickr.com/services/api/misc.api_keys.html

api_key=""
api_secret=""

# Set your Twitter API keys here
# get them at https://developer.twitter.com/en

def getApiKey():
	apikey={
	    "tck" : "",
	    "tcs" : "",
	    "tat" : "",
	    "tas" : ""}
	return (apikey)

def openTwitter():
        apikey=getApiKey()
        auth = tweepy.OAuthHandler(apikey['tck'], apikey['tcs'])
        auth.set_access_token(apikey['tat'],apikey['tas'])
        api = tweepy.API(auth)
        return api

outfile="/tmp/filename"
suffix=".jpg"

#sort out some command line parsing

parser = argparse.ArgumentParser(description='Posts random Flickr image on Twitter.')
parser.add_argument('-id',required=False,default=id,type=str,help='ID of Flickr user')
parser.add_argument('-nocontext', action='store_true',help="send tweet without any text if true")

args = vars(parser.parse_args())

id=args["id"] 

flickr_api.set_keys(api_key = api_key, api_secret = api_secret)
user=flickr_api.Person.findByUserName(id)
photos = user.getPhotos()
pagetot=photos.info.pages

print "total pages: %s" % (pagetot)
print "total photos: %s" % (photos.info.total)

page=random.randrange(0,pagetot)

print "We're retrieving page: %s" % (page)
photos = user.getPhotos(page=page)

phot=random.randrange(0,len(photos))
url="https://www.flickr.com/photos/%s/%s" % (id,photos[phot].id)

print "Chosen photo: %s on page %s" % (phot,page)
print "Title: %s" % photos[phot].title
print "Saving file %s%s from %s" % (outfile,suffix,url)

photos[phot].save(filename=outfile)

#log in to Twitter

api = openTwitter()

#post to Twitter

if args["nocontext"]:
    tweet=""
else:
    tweet="%s\n--> %s" % (photos[phot].title,url)

print "Tweet: %s" % tweet

print "Posting to Twitter..."

z=api.update_with_media (filename=outfile+suffix, status=tweet)

twitterurl="https://twitter.com/_/status/%s" % (z.id)

print "URL: %s" % twitterurl
