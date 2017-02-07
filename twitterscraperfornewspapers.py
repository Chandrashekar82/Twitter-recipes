import twitter, csv, sys

# == OAuth Authentication ==
consumer_key=""
consumer_secret=""
access_token=""
access_token_secret=""

AUTH = twitter.oauth.OAuth(access_token, access_token_secret, consumer_key, consumer_secret)
twitter_api = twitter.Twitter(auth=AUTH)

csvfile = open('filename.csv', 'w')
csvwriter = csv.writer(csvfile)
csvwriter.writerow(['created_at',
                    'text',
                    'retweet_count',
                    'place',
                    'user-location',
                    'user-geo_enabled',
                    'user-time_zone',
                    'user-statuses_count',
                    'user-followers_count',
                    'user-friends_count',
                    'user-created_at',
                    'user-source'])


# 'Independent', 'BBCNews', 'DailyMailUK', 'Telegraph','guardiannews', 'TheSun', 'DailyMirror', 'thetimes'
# see https://tweeterid.com/ you need ids not screen names for this to work
u = "abcde"

print >> sys.stderr, 'Following the public timeline for user(s)="%s"' % (u)
# Reference the self.auth parameter
twitter_stream = twitter.TwitterStream(auth=twitter_api.auth)
# See https://dev.twitter.com/docs/streaming-apis
stream = twitter_stream.statuses.filter(follow=u)



''' helper functions, clean data, unpack dictionaries '''
def getVal(val):
    clean = ""
    if isinstance(val, bool):
        return val
    if isinstance(val, int):
        return val
    if val:
        clean = val.encode('utf-8')
    return clean

def getLng(val):
    if isinstance(val, dict):
        return val['coordinates'][0]

def getLat(val):
    if isinstance(val, dict):
        return val['coordinates'][1]

def getPlace(val):
    if isinstance(val, dict):
        return val['full_name'].encode('utf-8')


# main loop
for tweet in stream:
    try:
        csvwriter.writerow([tweet['created_at'],                        # write lots of data!!
                            getVal(tweet['text']),
                            getVal(tweet['retweet_count']),
                            getPlace(tweet['place']),
                            getVal(tweet['user']['location']),
                            getVal(tweet['user']['geo_enabled']),
                            getVal(tweet['user']['lang']),
                            getVal(tweet['user']['time_zone']),
                            getVal(tweet['user']['statuses_count']),
                            getVal(tweet['user']['followers_count']),
                            getVal(tweet['user']['friends_count']),
                            getVal(tweet['source'])
                            ])
        csvfile.flush()
        print getVal(tweet['user']['screen_name']), getVal(tweet['text']), tweet['coordinates'], getPlace(tweet['place'])
    except Exception as e:
        print e.message
