# Converts a string to lowercase formatting
def convert(string):
    if len(string) < 3:
        return string.lower()
    s = string
    first = s[0]
    if not first.isalnum():
        if first != "#":
            s = s[1:]
    last = s[len(s) - 1]
    if not last.isalnum():
        s = s[:(len(s) - 1)]
    return s.lower()


# Gets all tweets and the POSs of all words in the tweets
def gettweetsandPOSs():

    tweets_all = {}
    tweet_POSs_all = {}
        
    data = pd.read_csv("all_tweets.csv")
    
    people = list(data.person.unique())

    tweets = []
    tweet_POSs = []

    for index, row in data.iterrows():
        text = row["text"]
        try:
            
            words = text.split(" ")
            tweet = [convert(word) for word in words]
            
            sentence = " ".join(tweet)
            text = nltk.word_tokenize(sentence)
            tagged_text = nltk.pos_tag(text)
            tweet_POSs = [tag[1] for tag in tagged_text]

            tweets.append(tweet)
            tweet_POSs.append(tweet_POSs)

        except:
            print(text)

    tweets_all[person] = tweets
    tweet_POSs_all[person] = tweet_POSs

    return tweets_all, tweet_POSs_all