# -*- coding: utf-8 -*-

# FlickrBot 0.3
# 
# This code will pick a random photo from a Flickr user and post it on Twitter
# 
# Made by Rob Manuel from a request by Paul Clarke
#
# USE: 
# python flickrbot.py -tag paulfav -id paul_clarke -nocontext 
#
# install
# git clone https://github.com/robmanuel/flickrbot
#
# version 0.3 adds a default privacy setting of 1
#
# 1 public photos
# 2 private photos visible to friends
# 3 private photos visible to family
# 4 private photos visible to friends & family
# 5 completely private photos
#
# version 0.2 moves api keys to an ini file
# and allows tag searching


import flickr_api,random,tweepy,argparse

from botini import *

#what Flickr user are we looking for?
id="paul_clarke"

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
parser.add_argument('-tag',required=False,type=str,help='Tag to search for')
parser.add_argument('-privacy_filter',required=False,type=str,help='Return photos only matching a certain privacy level',default="1")


args = vars(parser.parse_args())

id=args["id"] 
tag=args["tag"]
privacy_filter=args["privacy_filter"]

flickr_api.set_keys(api_key = api_key, api_secret = api_secret)
user=flickr_api.Person.findByUserName(id)


if tag is None:
    user=flickr_api.Person.findByUserName(id)
    photos = user.getPhotos(privacy_filter=privacy_filter)
else:
    photos=flickr_api.Photo.search(tags=tag,user_id=id,privacy_filter=privacy_filter) 

pagetot=photos.info.pages

print "total pages: %s" % (pagetot)
print "total photos: %s" % (photos.info.total)

page=random.randrange(0,pagetot)

print "We're retrieving page: %s" % (page)
if tag is None:
    photos = user.getPhotos(page=page,privacy_filter=privacy_filter)
else:
    photos = flickr_api.Photo.search(tags=tag,page=page,user_id=id,privacy_filter=privacy_filter)

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
