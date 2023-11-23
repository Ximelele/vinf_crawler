import os
import re
import sys
from pyspark.sql import SparkSession

os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

def mergeData():
    spark_session = SparkSession.builder.master('local[*]').appName('buffparser').getOrCreate()
    
    directory = '/workspaces/VINF_CRAWLER/buffcleaned/'
    test = os.listdir(directory)
    directory2 = '/workspaces/VINF_CRAWLER/cleaned/'
    test2 = os.listdir(directory2)

    filtered2 = [x for x in test2 if re.match(r'.*_Counters.html$', x)]
    filtered =  [x for x in test if re.match(r'.*counters.*$', x)]
    filtered = sorted(filtered) 
    filtered2 = sorted(filtered2) 

    for i,j in zip(filtered2,filtered):
        df = spark_session.read.text(os.path.join(directory2, i))
        df2 = spark_session.read.text(os.path.join(directory, j))
        print(os.path.join(directory, j))
        print(os.path.join(directory2, i))
        result_df = df.union(df2)
        rdd_data = result_df.rdd.map(lambda row: [str(item) for item in row])
        new_name = "upadate_" + str(i)
        with open(os.path.join('/workspaces/VINF_CRAWLER/cleaned/', new_name), 'w') as new_file:
            for row in rdd_data.collect():
                row_str = ' '.join(row) + '\n'
                new_file.write(row_str)
            
        # removing duplicated files
        os.remove(os.path.join('/workspaces/VINF_CRAWLER/cleaned/', i))
    spark_session.stop()
