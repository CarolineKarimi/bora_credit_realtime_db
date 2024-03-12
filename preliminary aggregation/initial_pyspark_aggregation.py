# Import necessary PySpark modules
from pyspark.sql import SparkSession
from pyspark.sql.functions import count
from pyspark.sql.functions import col, initcap

# Initialize Spark session
spark = SparkSession.builder.appName("BoraCreditRealTimeDashboard").getOrCreate()

# Load cleaned data to PySpark DataFrame
cleaned_data = spark.read.csv("bora_credit_demographic_data_clean.csv", header=True)

# Read questions data, this has additional information to help user navigate the dashboard
questions = spark.read.csv("survey_questions.csv", header=True)

# Define the columns to include
select_one = ['gender', 'marital_status', 'children', 'age', 'education', 'employment_status']

# Create an empty DataFrame to hold the final summary data
summary_data = spark.createDataFrame([], schema=["source", "answer", "loan_id", "loan_share"])

# Iterate over the selected columns
for cat in select_one:
    # Group by source and the current categorical variable (cat)
    grouped_data = cleaned_data.groupby("source", cat).agg(countDistinct("loan_id").alias("loan_id_count"))
    total_loans = grouped_data.groupby("source").agg(countDistinct("loan_id").alias("total_loans"))
    joined_data = grouped_data.join(total_loans, on="source", how="inner")
    # Calculate the loan share
    summary_data = joined_data.withColumn("loan_share", round(joined_data["loan_id_count"] / joined_data["total_loans"], 2))
    summary_data = summary_data.withColumn("aggregation", lit(cat))
    # Append the current summary data to the final DataFrame
    summary_data = summary_data.union(summary_data)

# Merge with questions data with update summary
summary_data = summary_data.join(questions, on="aggregation", how="left")

# Rename columns to easier to understand names
summary_data = summary_data.withColumnRenamed("loan_id_count", "cnt") \
                           .withColumnRenamed("loan_share", "value") \
                           .replace({"gender": "By Gender", "marital_status": "By Marital Status",
                                     "children": "By Children Status", "age": "By Age",
                                     "education": "By Highest Education Level",
                                     "employment_status": "By Current Employment Status"})
                                     
# Capitalize column names
for col_name in summary_data.columns:
    summary_data = summary_data.withColumnRenamed(col_name, col_name.capitalize())

# Structure responses
for col in ['source', 'answer', 'aggregation', 'question', 'y_axis']:
    summary_data = summary_data.withColumn(col, initcap(col))
                                  
# Write the summary data to a file
summary_data.write.csv("aggregated_demographic_data.csv", header=True, mode="overwrite")


#stop the session
spark.stop()
