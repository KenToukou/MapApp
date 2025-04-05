import numpy as np
import pandas as pd

df = pd.read_csv("./data/cities.csv")
print(df)

df["乗客"] = np.random.randint(100, 200, size=len(df))


df.to_csv("./data/cities.csv", index=False)
