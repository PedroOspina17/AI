# This is Main function.
# Extracting streaming data from Twitter, pre-processing, and loading into Postgres
import credentials # Import api/access_token keys from credentials.py
import settings # Import related setting constants from settings.py 

import re
import tweepy
import time
from sqlalchemy import create_engine
from textblob import TextBlob
# Streaming With Tweepy 
# http://docs.tweepy.org/en/v3.4.0/streaming_how_to.html#streaming-with-tweepy



# Override tweepy.StreamListener to add logic to on_status
class TwStreamListener(tweepy.StreamListener):
    '''
    Tweets are known as “status updates”. So the Status class in tweepy has properties describing the tweet.
    https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object.html
    '''
    engine = create_engine('postgresql://postgres:password@host:5432/database')
    auth  = tweepy.OAuthHandler(credentials.API_KEY, credentials.API_SECRET_KEY)
    runtime = 10

    def __init__(self):
        '''
        Check if this table exits. If not, then create a new one.
        '''
        try:
            self.start_time = time.time()
            self.limit_time = self.runtime
            self.engine.connect()
            self.mydb = self.engine.raw_connection()
            self.mycursor = self.mydb.cursor()
            self.mycursor.execute("""
                SELECT COUNT(*)
                FROM information_schema.tables
                WHERE table_name = '{0}'
                """.format(settings.TABLE_NAME))
            if self.mycursor.fetchone()[0] != 1:
                self.mycursor.execute("CREATE TABLE {} ({})".format(settings.TABLE_NAME, settings.TABLE_ATTRIBUTES))
                self.mydb.commit()
            self.mycursor.close()
        except Exception as error:
            print("Problem connecting to the database: ",error)
    
    def connect(self):
        '''
        Connecting to the API.
        '''
        self.auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(self.auth)
        self.myStream = tweepy.Stream(auth = self.api.auth, listener = self)
        return None


    def on_status(self, status):
        '''
        Extract info from tweets
        '''
        
        if status.retweeted:
            # Avoid retweeted info, and only original tweets will be received
            return True
        # Extract attributes from each tweet
        id_str = status.id_str
        created_at = status.created_at
        text = self.deEmojify(status.text)    # Pre-processing the text  
        sentiment = TextBlob(text).sentiment
        polarity = sentiment.polarity
        subjectivity = sentiment.subjectivity
        
        user_created_at = status.user.created_at
        #print("User Location: ", status.user.location)
        user_location = self.deEmojify(status.user.location)
        #print("User Location End: ",user_location)
        user_description = self.deEmojify(status.user.description)
        user_followers_count =status.user.followers_count
        longitude = None
        latitude = None
        if status.coordinates:
            longitude = status.coordinates['coordinates'][0]
            latitude = status.coordinates['coordinates'][1]
            
        retweet_count = status.retweet_count
        favorite_count = status.favorite_count
        
        print(status.text)
        print("Long: {}, Lati: {}".format(longitude, latitude))
        
        # Store all data in Postgres
        try:
            '''
            Check if this table exits. If not, then create a new one.
            '''
            self.engine.connect()
            self.mydb = self.engine.raw_connection()
            self.mycursor = self.mydb.cursor()
            sql = "INSERT INTO {} (id_str, created_at, text, polarity, subjectivity, user_created_at, user_location, user_description, user_followers_count, longitude, latitude, retweet_count, favorite_count) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format(settings.TABLE_NAME)
            val = (id_str, created_at, text, polarity, subjectivity, user_created_at, user_location, \
                user_description, user_followers_count, longitude, latitude, retweet_count, favorite_count)
            self.mycursor.execute(sql, val)
            self.mydb.commit()
            self.mycursor.close()
        except Exception as error:
            print("Error inserting twitter: ",error)
        
        if (time.time() - self.start_time) < self.limit_time:
            print("Working")
            return True
        else:
            print("Time Complete")
            return False
    
    
    def on_error(self, status_code):
        '''
        Since Twitter API has rate limits, stop scraping data as it exceed to the thresold.
        '''
        if status_code == 420:
            # return False to disconnect the stream
            return False

    def clean_tweet(self, tweet): 
        ''' 
        Use sumple regex statemnents to clean tweet text by removing links and special characters
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 

    def deEmojify(self,text):
        '''
        Strip all non-ASCII characters to remove emoji characters
        '''
        if text:
            return text.encode('ascii', 'ignore').decode('ascii')
        else:
            return None
    
    def disconnect(self):
        self.mydb.close()
        return print("Stop Streaming")
    
    def run(self):
        print("Start Streaming")
        self.myStream.filter(languages=["en"], track = settings.TRACK_WORDS,is_async=True,locations=[-6.38,49.87,1.77,55.81])
        time.sleep(self.runtime)
        self.disconnect()
        return None