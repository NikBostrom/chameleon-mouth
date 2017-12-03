# Python 3
from ..data/clean_general import convert
# def convert(string):
#     if len(string) < 3:
#         return string.lower()
#     s = string
#     first = s[0]
#     if not first.isalnum():
#         if first != "#":
#             s = s[1:]
#     last = s[len(s) - 1]
#     if not last.isalnum():
#         s = s[:(len(s) - 1)]
#     return s.lower()

# files = os.listdir("raw_tweets")
# people = list(map(lambda x: x.split("_")[0], files))

# for person, file in zip(people, files):
    
#     data = pd.read_csv("raw_tweets/" + file)
    
#     dict_item = dict()
#     pos_dict = dict()
    
#     for index, row in data.iterrows():
#         text = row["text"]
#         try:
#             words = text.split(" ")
#             words = [convert(word) for word in words]
#             sentence = " ".join(words)
#             text = nltk.word_tokenize(sentence)
#             tagged_text = nltk.pos_tag(text)
#             for (word, POS) in tagged_text:
                
#                 if word not in dict_item.keys():
#                     dict_item[word] = 1
#                 else:
#                     dict_item[word] += 1
#                 if POS not in pos_dict.keys():
#                     pos_dict[POS] = 1
#                 else:
#                     pos_dict[POS] += 1
#         except:
#             print(text)


# class k_Nearest:
#     def __init__(self):

print(convert("test"))