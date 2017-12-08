# Python 3

import k_nearest

knn = k_nearest.k_Nearest()

k = 10

user_input = input("Please Enter Your Tweet: ")

prediction = knn.get_author_prediction(user_input, k)

print("Prediction: " + prediction)