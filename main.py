import sys
import tweepy
import csv
import re
from textblob import TextBlob
import matplotlib.pyplot as plt

class Sentiment_Analysis:
    def fatchdata(self):
        self.tweets = []
        self.tweetText = []
        consumerKey = "your_key"
        consumerSecret = "your_key"
        accessToken = "your_key"
        accessTokenSecret ="your_key"
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth)
        search = input("Enter Keyword to search about: ")
        No = int(input("Enter how many tweets to search: "))
        self.tweets = tweepy.Cursor(api.search, q=search, lang = "en").items(No)
        csvFile = open('result.csv', 'a')
        csvWriter = csv.writer(csvFile)
        posi = 0
        wposi = 0
        sposi = 0
        nega = 0
        wnega = 0
        snega = 0
        neut = 0
        polarity = 0
        for tweet in self.tweets:
            self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))
            analysis = TextBlob(tweet.text)
            polarity += analysis.sentiment.polarity  
            if (analysis.sentiment.polarity == 0): 
                neut += 1
            elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
                wposi += 1
            elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
                posi += 1
            elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
                sposi += 1
            elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
                wnega += 1
            elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
                nega += 1
            elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
                snega += 1
        csvWriter.writerow(self.tweetText)
        csvFile.close()
        posi = self.percentage(posi, No)
        wposi = self.percentage(wposi, No)
        sposi = self.percentage(sposi, No)
        nega = self.percentage(nega, No)
        wnega = self.percentage(wnega, No)
        snega = self.percentage(snega, No)
        neut = self.percentage(neut, No)
        polarity = polarity / No
        print("How people are reacting on " + search + " by analyzing " + str(No) + " tweets.")
        print()
        print("General Report: ")
        if (polarity == 0):
            print("Neut")
        elif (polarity > 0 and polarity <= 0.3):
            print("Weakly Positive")
        elif (polarity > 0.3 and polarity <= 0.6):
            print("Positive")
        elif (polarity > 0.6 and polarity <= 1):
            print("Strongly Positive")
        elif (polarity > -0.3 and polarity <= 0):
            print("Weakly Negative")
        elif (polarity > -0.6 and polarity <= -0.3):
            print("Negative")
        elif (polarity > -1 and polarity <= -0.6):
            print("Strongly Negative")
        print()
        print("Detailed Report: ")
        print(str(posi) + "% people thought it was positive")
        print(str(wposi) + "% people thought it was weakly positive")
        print(str(sposi) + "% people thought it was strongly positive")
        print(str(nega) + "% people thought it was negative")
        print(str(wnega) + "% people thought it was weakly negative")
        print(str(snega) + "% people thought it was strongly negative")
        print(str(neut) + "% people thought it was neutral")
        self.plotPieChart(posi, wposi, sposi, nega, wnega, snega, neut, search, No)
    def cleanTweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())
    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')
    def plotPieChart(self, posi, wposi, sposi, nega, wnega, snega, neut, search, no):
        labels = ['Positive [' + str(posi) + '%]', 'Weakly Positive [' + str(wposi) + '%]','Strongly Positive [' + str(sposi) + '%]', 'Neutral [' + str(neut) + '%]',
                  'Negative [' + str(nega) + '%]', 'Weakly Negative [' + str(wnega) + '%]', 'Strongly Negative [' + str(snega) + '%]']
        sizes = [posi, wposi, sposi, neut, nega, wnega, snega]
        colors = ['yellowgreen','lightgreen','darkgreen', 'gold', 'red','lightsalmon','darkred']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('How people are reacting on ' + search + ' by analyzing ' + str(no) + ' Tweets.')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()
Sentiment_Analysis()
Sentiment_Analysis().fatchdata()
