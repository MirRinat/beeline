#!/usr/bin/env python
# coding: utf-8

# In[16]:


import findspark
findspark.init()

from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.types import IntegerType
from pyspark.sql import Window
from pyspark import SparkContext, SparkConf, SQLContext
from IPython.display import display

spark = SparkSession.builder.appName('spark_csv').getOrCreate()


# ### Считать csv-файл из первого этапа и преобразовать данные этого файла в spark-dataframe

# In[3]:


df = spark.read.csv(path ='phones.csv',header=True)


# In[4]:


display(df.show(truncate=False))


# In[5]:


split_col = F.split(df['title'], ' ')

#Разделить поле title на два отдельных – smartphone_brand и smartphone_model. 
df1 = df.withColumn('smartphone_brand', F.split(df['title'],' ').getItem(0))
df1 = df1.withColumn('smartphone_brand1', split_col.getItem(F.size(split_col)-1))
df1 = df1.withColumn('smartphone_brand2', split_col.getItem(F.size(split_col)-2))
df1 = df1.drop('seller','ram','memory')
df1 = df1.withColumn('smartphone_model',F.expr('substring(title,length(smartphone_brand)+2, length(title)-length(smartphone_brand)-length(smartphone_brand1)-length(smartphone_brand2)-3)')).drop('smartphone_brand2','smartphone_brand1')
# я не знал как сделать по-другому - ничего не нашел


#Найти средние стоимости моделей смартфонов. 
df1 = df1.withColumn("price", df1["price"].cast(IntegerType()))
df1 = df1.groupby('smartphone_brand','smartphone_model').agg(F.avg('price').alias('smartphone_price'))

#Каждой уникальной записи dataframe’а необходимо присвоить свой порядковый smartphone_id, начиная с 1
df1= df1.withColumn("new_column",F.lit("ABC"))
w = Window().partitionBy('new_column').orderBy(F.lit('A'))
df1 = df1.withColumn("smartphone_id", F.row_number().over(w)).drop("new_column")
df1 = df1.select('smartphone_id', 'smartphone_brand', 'smartphone_model', 'smartphone_price')
df1.show(10,False)




# In[11]:


df1.write.mode('overwrite').parquet("phones.parquet")


# In[33]:


# import os
# os.environ['PYSPARK_SUBMIT_ARGS'] = '--jars ~/Downloads/postgresql-42.2.18.jar pyspark-shell'


# In[34]:


url = "jdbc:postgresql://localhost:5432/beeline_db"
properties = {
    "driver": "org.postgresql.Driver",
    "user": "rinatmirzagalamov",
    
}


# In[36]:


mode = 'overwrite'
df1.write.jdbc(url=url, table="smartphones", mode=mode, properties=properties)


# In[ ]:
#run in terminal
###spark-submit --driver-class-path ~/Downloads/postgresql-42.2.18.jar spark_csv.py


