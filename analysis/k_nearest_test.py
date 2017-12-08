import pandas as pd

test_set = pd.read_csv("test_set_sample.csv")

knn = k_Nearest()
k = 10

tweets = list(test_set["text"])
predictions = [knn.get_author_prediction(tweet, k) for tweet in tweets]

test_set["prediction"] = predictions
test_set["correct"] = test_set["prediction"] == test_set["person"]

correct = test_set[test_set["correct"] == True]
num_correct = len(correct)
test_set.to_csv("knn_predictions.csv", index=False)
num_total = len(test_set)
print("Percent Correct" + str(num_correct/num_total))

people = list(set(test_set["person"]))

for person in people:
    temp = test_set[test_set["person"] == person]
    num = len(temp)
    correct = temp[temp["correct"] == True]
    c = len(correct)
    print("Person: " + person)
    print("Tweets: " + str(num))
    print("Number Correct: " + str(c))
    print("Percentage Correct: " + str(c / num))
    print()
