# Python 3

import pandas as pd
import bagofwords

f_1 = {"obama": 0.1, "trump": 0.3, "neil": 0.5, "kim": 0.1}
f_2 = {"obama": 0.3, "trump": 0.1, "neil": 0.2, "kim": 0.4}

bag = bagofwords.BagOfWords()
bag_data = bag.run(["trump"])
print(bag_data)
