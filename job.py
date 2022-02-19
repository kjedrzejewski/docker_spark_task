import pandas as pd
import urllib.request
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.functions import mean
from sqlalchemy import create_engine
import os



csv_url = 'https://web.stanford.edu/class/archive/cs/cs109/cs109.1166/stuff/titanic.csv'
urllib.request.urlretrieve(csv_url, '/tmp/titanic.csv')

spark = SparkSession.builder.appName("Titanic survival statistics").getOrCreate()

df = spark.read.options(header='True', inferSchema='True').csv("/tmp/titanic.csv")



surv_u18_general = df.where(col("Age") < 18).select(mean("Survived")).toPandas()
surv_u18_general.columns = ['survival_rate']
surv_u18_general.insert(0,'cohort','surv_u18_general')

surv_18_40_general = df.where(col("Age").between(18, 40)).select(mean("Survived")).toPandas()
surv_18_40_general.columns = ['survival_rate']
surv_18_40_general.insert(0,'cohort','surv_18_40_general')

surv_18_40_sex = df.where(col("Age").between(18, 40)).groupBy("Sex").mean("Survived").toPandas()
surv_18_40_sex.Sex = surv_18_40_sex.Sex.apply(lambda x: f"surv_18_40_{x}")
surv_18_40_sex.columns = ['cohort', 'survival_rate']

surv_o40_general = df.where(col("Age") > 40).select(mean("Survived")).toPandas()
surv_o40_general.columns = ['survival_rate']
surv_o40_general.insert(0,'cohort','surv_o40_general')

surv_o40_sex = df.where(col("Age") > 40).groupBy("Sex").mean("Survived").toPandas()
surv_o40_sex.Sex = surv_o40_sex.Sex.apply(lambda x: f"surv_o40_{x}")
surv_o40_sex.columns = ['cohort', 'survival_rate']

surv_class_sex = df.groupBy(["Pclass","Sex"]).mean("Survived").toPandas()
surv_class_sex = surv_class_sex.sort_values(["Pclass","Sex"])
surv_class_sex = pd.DataFrame({
  'cohort': surv_class_sex.apply(lambda row : f"surv_class{row['Pclass']}_{row['Sex']}", axis = 1),
  'survival_rate': surv_class_sex['avg(Survived)']
})


result_dfs = [surv_u18_general, surv_18_40_general, surv_18_40_sex, surv_o40_general, surv_o40_sex, surv_class_sex]
survival_rates = pd.concat(result_dfs).reset_index(drop = True)



db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_db   = os.environ['MYSQL_DATABASE']

engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
                       .format(user=db_user, pw=db_pass, host=db_host, db=db_db))

survival_rates.to_sql('survival_rates', con=engine, if_exists='replace')

engine.dispose()
