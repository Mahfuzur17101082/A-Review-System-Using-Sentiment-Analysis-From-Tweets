import time
import sys,tweepy,csv,re
from textblob import TextBlob
import matplotlib.pyplot as plt
import pandas as pd
file = pd.ExcelFile('testData.xlsx')
p = file.parse('Sheet1')



class SentimentAnalysis:

    def __init__(self):
        self.tweets = []
        self.tweetText = []

    def DownloadData(self):
        # authenticating
        
        #consumerKey = 'i7QuDhcEPBaApQufnTUs5ePLU'
        #consumerSecret = 'FWJVWbr85yyyOCPLdhVxKq9pvrp4H4sq8XAmhI8RO9zQrJETjU'
        #accessToken = '859165648211111937-eYQRDQ74pnnBY97T4DMqjhzMWSwfu1f'
        #accessTokenSecret = 'BifTeXhLULU94h4O4awtx4dEW5vrdMRyf20Woe4jY27vY'
        
        consumerKey = "bTzm1DnOaM9shWxypP3YYBp8G"
        consumerSecret = "OE9xbUw8G3VJGQL3YP5miVx6PKBXqDuhkdVg1zdJVorhaVPAOs"
        accessToken = "1169642722631663616-OsDt1673xUfYFT3DNWVtbvmim61wz0"
        accessTokenSecret = "mDhagQjiLKEVCRdZ09ryk8GoQeUJdSyZqhWmsdefIIfDQ"
        
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth)
        neu=0
        wpo=0
        po=0
        spo=0
        wn=0
        n=0
        sn=0
        tp=0
        fp=0
        tn=0
        fn=0
        ac=0
        count=0
        #xaxis=list()
        #yaxis=list()
        for x in range (0,73):
            # input for term to be searched and how many tweets to search
            #searchTerm = input("Enter Keyword/Tag to search about: ")
            #NoOfTerms = int(input("Enter how many tweets to search: "))
            #xaxis[x]=fp
            #yaxis[x]=tp
            
            print(x)
            print("p: ",tp, " ", fp)
            searchTerm = p["Name"][x]
            NoOfTerms = 100
            if(x==0 or x==20 or x==40 or x==60):    
                time.sleep(60*20)
            # searching for tweets
            self.tweets = tweepy.Cursor(api.search, q=searchTerm, lang = "en").items(NoOfTerms)
    
            # Open/create a file to append data to
            csvFile = open('result.csv', 'a')
    
            # Use csv writer
            csvWriter = csv.writer(csvFile)
    
    
            # creating some variables to store info
            polarity = 0
            positive = 0
            wpositive = 0
            spositive = 0
            negative = 0
            wnegative = 0
            snegative = 0
            neutral = 0
    
    
            # iterating through tweets fetched
            for tweet in self.tweets:
                #Append to temp so that we can store in csv later. I use encode UTF-8
                self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))
                # print (tweet.text.translate(non_bmp_map))    #print tweet's text
                analysis = TextBlob(tweet.text)
                # print(analysis.sentiment)  # print tweet's polarity
                polarity += analysis.sentiment.polarity  # adding up polarities to find the average later
    
                if (analysis.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
                    neutral += 1
                elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
                    wpositive += 1
                elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
                    positive += 1
                elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
                    spositive += 1
                elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
                    wnegative += 1
                elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
                    negative += 1
                elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
                    snegative += 1
    
    
            # Write to csv and close csv file
            csvWriter.writerow(self.tweetText)
            csvFile.close()
    
            # finding average of how people are reacting
            positive = self.percentage(positive, NoOfTerms)
            wpositive = self.percentage(wpositive, NoOfTerms)
            spositive = self.percentage(spositive, NoOfTerms)
            negative = self.percentage(negative, NoOfTerms)
            wnegative = self.percentage(wnegative, NoOfTerms)
            snegative = self.percentage(snegative, NoOfTerms)
            neutral = self.percentage(neutral, NoOfTerms)
    
            # finding average reaction
            polarity = polarity / NoOfTerms
    
            # printing out data
            #print("How people are reacting on " + searchTerm + " by analyzing " + str(NoOfTerms) + " tweets.")
            #print()
            #print("General Report: ")
    
            if (polarity == 0):
                # print("Neutral")
                neu=neu+1
            elif (polarity > 0 and polarity <= 0.3):
                #print("Weakly Positive")
                wpo=wpo+1
                
                if(p["Comment"][x]==1):
                    tp=tp+1
                    ac=ac+1
                    #print("yo")
                else:
                    
                    fp=fp+1
                    print("vejal")
                    #print(p["Name"][1])
            elif (polarity > 0.3 and polarity <= 0.6):
                #print("Positive")
                po=po+1
                if(p["Comment"][x]==1):
                    tp=tp+1
                    ac=ac+1
                else:
                    fp=fp+1
                    print("vejal")
            elif (polarity > 0.6 and polarity <= 1):
                #print("Strongly Positive")
                spo=spo+1
                if(p["Comment"][x]==1):
                    tp=tp+1
                    ac=ac+1
                else:
                    fp=fp+1
                    print("vejal")
            elif (polarity > -0.3 and polarity <= 0):
                #print("Weakly Negative")
                wn=wn+1
                if(p["Comment"][x]==0):
                    tn=tn+1
                    ac=ac+1
                else:
                    fn=fn+1
            elif (polarity > -0.6 and polarity <= -0.3):
                #print("Negative")
                n=n+1
                if(p["Comment"][x]==0):
                    tn=tn+1
                    ac=ac+1
                else:
                    fn=fn+1
            elif (polarity > -1 and polarity <= -0.6):
                #print("Strongly Negative")
                sn=sn+1
                if(p["Comment"][x]==0):
                    tn=tn+1
                    ac=ac+1
                else:
                    fn=fn+1
    
            #print()
            #print(neu, wpo, po, spo, wn, n, sn, tp, fp, tn, fn)
            """print("Detailed Report: ")
            print(str(positive) + "% people thought it was positive")
            print(str(wpositive) + "% people thought it was weakly positive")
            print(str(spositive) + "% people thought it was strongly positive")
            print(str(negative) + "% people thought it was negative")
            print(str(wnegative) + "% people thought it was weakly negative")
            print(str(snegative) + "% people thought it was strongly negative")
            print(str(neutral) + "% people thought it was neutral")
    """ 
        count=po+wpo+spo+sn+n+wn
        print("Total Neutral: ", (neu*100)/count, "%")
        print("Total Weakly Positive: ", (wpo*100)/count, "%")
        print("Total Positive: ", (po*100)/count, "%")
        print("Total Strongly Positive: ", (spo*100)/count, "%")
        print("Total Weakly Negative: ", (wn*100)/count, "%")
        print("Total Negative: ", (n*100)/count, "%")
        print("Total Strongly Negative: ", (sn*100)/count, "%")
        print()
        print()
        print("Total ", (tp*100)/count, "% result is True Positive")
        print("Total ", (fp*100)/count, "% result is False Positive")
        print("Total ", (tn*100)/count, "% result is True Negative")
        print("Total ", (fn*100)/count, "% result is False Negative")
        print()
        print()
        precision=tp/(tp+fp)
        recall=tp/(tp+fn)
        print("Total Accuracy: ", (ac*100)/count,"%")
        print("Total Precision: ", precision)
        print("Total Recall: ", recall)
        print("F1 Score: ",2*((precision*recall)/(precision+recall)))
        print()
        print()
        self.plotPieChart(((tp*100)/count), ((fp*100)/count), ((tn*100)/count), ((fn*100)/count))
        #self.plotPieChart(positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, NoOfTerms)
        
    def cleanTweet(self, tweet):
        # Remove Links, Special Characters etc from tweet
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

    # function to calculate percentage
    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

    """def plotPieChart(self, positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, noOfSearchTerms):
        labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(wpositive) + '%]','Strongly Positive [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]',
                  'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(wnegative) + '%]', 'Strongly Negative [' + str(snegative) + '%]']
        sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
        colors = ['yellowgreen','lightgreen','darkgreen', 'gold', 'red','lightsalmon','darkred']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('How people are reacting on ' + searchTerm + ' by analyzing ' + str(noOfSearchTerms) + ' Tweets.')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()"""
    def plotPieChart(self, tp, fp, tn, fn):
        labels = ['True Positive [' + str(tp) + '%]', 'False Positive [' + str(fp) + '%]', 'True Negative [' + str(tn) + '%]', 'False Negative [' + str(fn) + '%]']
        sizes = [tp, fp, tn, fn]
        colors = ['darkgreen', 'gold', 'darkred', 'darkblue']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('Rafs')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()


if __name__== "__main__":
    
    sa = SentimentAnalysis()
    sa.DownloadData()
    #sa.plotPieChart(tp, fp, tn, fn)
    
    


