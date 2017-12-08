# Python 3

import k_nearest

knn = k_nearest.k_Nearest()

k = 10

tweet = "hello"

prediction = knn.get_author_prediction(tweet, k)

print(prediction)