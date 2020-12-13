import os
import sys
import pandas as pd
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "baby_names.settings")
import django
django.setup()

sys.path.append(os.getcwd())
from names.models import BabyName

data_files = [
    '../baby_data/2018boysnames.csv',
    '../baby_data/2018girlsnames.csv'
]

for name_file in data_files:
    df = pd.read_csv('../baby_data/2018boysnames.csv')
    df = df.astype({'rank': 'int32', 'count': 'int32'})
    print(df.head())
    for index, row in df.iterrows():
        if index % 100 == 0:
            print(row['name'])
        name, created = BabyName.objects.get_or_create(
            name=row['name'],
            sex=row['sex']
        )
        name.save()
