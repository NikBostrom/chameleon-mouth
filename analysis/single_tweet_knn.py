# Python 3

import k_nearest

print("Loading...")
print()
knn = k_nearest.k_Nearest()

k = 10

while(True):

    user_input = input("Please Enter Your Tweet (Control-C to Quit): ")

    prediction = knn.get_author_prediction(user_input, k)

    print("Prediction: " + prediction)
    print()