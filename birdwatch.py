#!/usr/bin env python3

import tweepy
import re
import time
import datetime

from pprint import pprint

# Consumer keys and access tokens, used for OAuth
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Creation of the actual interface, using authentication
api = tweepy.API(auth)

public_tweets = tweepy.Cursor(api.home_timeline,
								 exclude_replies="True",
								 screen_name="",
								 tweet_mode="extended").items(200)

now = datetime.datetime.utcnow().isoformat() + "Z"
url_transf = re.compile(r'(https://[^\s]*)')

print("""<?xml version="1.0" encoding="utf-8"?>
<?xml-stylesheet type="text/xsl" href="atom.xsl"?>
<feed xmlns="http://www.w3.org/2005/Atom">

    <title>Twitter</title>
    <link rel="self" href="https://copype.ga/birdwatch.xml/"/>
    <updated>{}</updated>
    <id>https://copype.ga/birdwatch.xml/</id>""".format(now))

for tweet in public_tweets:
	twtime = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.strptime(tweet._json["created_at"],'%a %b %d %H:%M:%S %z %Y'))
	
	if "retweeted_status" in tweet._json.keys():
		twauthor = tweet._json["user"]["name"]
		twtitle = tweet._json["retweeted_status"]["user"]["screen_name"]
		before_transf = tweet._json["retweeted_status"]["full_text"]
		twtext = url_transf.sub(r'<a href="\1">\1</a>', before_transf)
		if "media" in tweet._json["retweeted_status"]["entities"].keys():
			twpic = tweet._json["retweeted_status"]["entities"]["media"][0]["media_url_https"]
			twmedia = '<img src="{}">'.format(twpic)
			twtext += twmedia
	
	elif "quoted_status" in tweet._json.keys():
		twtitle = tweet._json["user"]["screen_name"]
		twauthor = tweet._json["user"]["name"]
		# el espacio antes del <br> es para que .sub no lo interprete como parte del <a>
		before_transf = tweet._json["full_text"] + " <br /><blockquote><p>" + tweet._json["quoted_status"]["full_text"] + "</p></blockquote>"
		twtext = url_transf.sub(r'<a href="\1">\1</a>', before_transf)
		if "media" in tweet._json["entities"].keys():
			twpic = tweet._json["entities"]["media"][0]["media_url_https"]
			twmedia = '<img src="{}">'.format(twpic)
			twtext += twmedia
	
	else:
		twtitle = tweet._json["user"]["screen_name"]
		twauthor = tweet._json["user"]["name"]
		before_transf = tweet._json["full_text"]
		twtext = url_transf.sub(r'<a href="\1">\1</a>', before_transf)
		if "media" in tweet._json["entities"].keys():
			twpic = tweet._json["entities"]["media"][0]["media_url_https"]
			twmedia = '<img src="{}">'.format(twpic)
			twtext += twmedia
		
	twid = tweet._json["id"]
	output = """
	<entry>
		<id>https://twitter.com/{}/status/{}</id>
		<author>
			<name>{}</name>
			<uri>https://twitter.com/{}</uri>
		</author>
		<updated>{}</updated>
		<title>@<![CDATA[{}]]></title>
		<link rel="alternate" href="https://twitter.com/{}/status/{}"/>
		<content type="html"><![CDATA[{}]]></content>
	</entry>
	""".format(twauthor,twid,twauthor,twauthor,twtime,twtitle,twauthor,twid,twtext)
	
	print(output)

print("</feed>")
