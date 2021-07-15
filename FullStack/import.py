import pandas as pd
from pandas import DataFrame
from sqlalchemy import create_engine

# 跟DB連結
engine = create_engine('mysql://root:password321@127.0.0.1:3306/csv')

df = pd.read_csv("C:/Users/BrianSu/PycharmProjects/FullStack/root/dns_sample.csv", error_bad_lines=False)

print(df)
df = df.dropna()
# Read from and write to Mysql table
df = df.fillna(0)
df.to_sql('app_csvdata', engine, index=False, if_exists='append')
print('Read from and write to Mysql table successfully!')
