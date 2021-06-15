"""
Quick script to process the json pumped out by the scraper.
One hot encodes and saves as a CSV
"""

import pandas as pd
import os
from sklearn.preprocessing import MultiLabelBinarizer
import re

data_file = os.path.join(
    os.path.dirname(__file__),
    'name_origin.json'
)
df = pd.read_json(data_file)

df['usage'] = df.usage.apply(
    lambda x: [re.sub("[\(\[].*?[\)\]]", "", i).strip() for i in x]
)

df['name'] = df.name.str.upper()

mlb = MultiLabelBinarizer()

hot_encoded = mlb.fit_transform(df.usage)


df_hot = df[['name']].join(pd.DataFrame(
        hot_encoded,
        columns = mlb.classes_
))

df_long = df.explode('usage')

print(df_long.head())

df_hot.to_csv('name_origins_processed.csv', index=False)
df_long.to_csv('name_origin_long.csv', index=False)