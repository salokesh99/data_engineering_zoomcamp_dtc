import sys

import pandas as pd

df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})


month = sys.argv[2]


df['month'] = month

print(df.head())


df.to_parquet(f"output_day_{sys.argv[1]}.parquet")


# Our pipeline here

print(sys.argv)

day = sys.argv[1]

print('Completed the task successfully!!!! for the day {}'.format(day))
