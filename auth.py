#!/usr/bin/env python

import tweepy

CONSUMER_KEY = 'Ck4MU5UrHqKvHpl9fLhCzw'
CONSUMER_SECRET = 'F0uhzfE58VdSuZhqgEkFknFQCdDDFKapYKL8C9LCJU'

# Authorize TwitVN with a Twitter account 
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth_url = auth.get_authorization_url()
print 'Please open the following URL: ' + auth_url
verifier = raw_input('PIN: ').strip()
auth.get_access_token(verifier)
print "ACCESS_KEY = '%s'" % auth.access_token.key
print "ACCESS_SECRET = '%s'" % auth.access_token.secret
