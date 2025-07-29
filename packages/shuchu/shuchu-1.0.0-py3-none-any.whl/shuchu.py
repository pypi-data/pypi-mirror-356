def run():
    """""
    from pyspark import SparkContext

    sc = SparkContext("local", "CityTemperatureAnalysis")
    # 读取数据
    data = sc.textFile("city_temperatures.txt")
    # 转换为 RDD
    city_temp_rdd = data.map(lambda line: line.split(",")).map(lambda x: (x[0],
                                                                          int(x[1])))
    # 1. 读取文件并转换为 RDD
    # 已经完成
    # 2. 计算每个城市的平均温度
    avg_temp = city_temp_rdd.mapValues(lambda temp: (temp, 1)) \
        .reduceByKey(lambda a, b: (a[0] + b[0], a[1] + b[1])) \
        .mapValues(lambda x: x[0] / x[1]) \
        .mapValues(lambda x: round(x, 2))
    print("每个城市的平均温度:")
    avg_temp.collect()
    # 3. 找出每个城市中温度最高的记录
    max_temp = city_temp_rdd.reduceByKey(lambda a, b: a if a > b else b)
    print("\n每个城市中温度最高的记录:")
    max_temp.collect()
    # 4. 统计每个城市中温度大于等于 30 的天数
    high_temp_count = city_temp_rdd.filter(lambda x: x[1] >= 30) \
        .map(lambda x: (x[0], 1)) \
        .reduceByKey(lambda a, b: a + b)
    print("\n每个城市中温度大于等于 30 的天数:")
    high_temp_count.collect()
    # 5. 找出温度最高的 3 个城市
    top_3_temps = city_temp_rdd.map(lambda x: (x[1], x[0])) \
        .sortByKey(False) \
        .map(lambda x: (x[1], x[0])) \
        .take(3)
    print(top_3_temps)
    sc.stop()

    from pyspark import SparkContext
    sc = SparkContext("local", "CityTemperatureAnalysis")
    # 读取数据
    data = sc.textFile("city_temperatures.txt")
    # 转换为 RDD
    city_temp_rdd = data.map(lambda line: line.split(",")).map(lambda x: (x[0], int(x[1])))
    # 1. 读取文件并转换为 RDD
    # 已经完成
    # 2. 计算每个城市的平均温度
    avg_temp = city_temp_rdd.mapValues(lambda temp: (temp, 1)) \
        .reduceByKey(lambda a, b: (a[0] + b[0], a[1] + b[1])) \
        .mapValues(lambda x: x[0] / x[1]) \
        .mapValues(lambda x: round(x, 2))
    print("每个城市的平均温度:")
    avg_temp.collect()
    # 3. 找出每个城市中温度最高的记录
    max_temp = city_temp_rdd.reduceByKey(lambda a, b: a if a > b else b)
    print("\n每个城市中温度最高的记录:")
    max_temp.collect()
    # 4. 统计每个城市中温度大于等于 30 的天数
    high_temp_count = city_temp_rdd.filter(lambda x: x[1] >= 30) \
        .map(lambda x: (x[0], 1)) \
        .reduceByKey(lambda a, b: a + b)
    print("\n每个城市中温度大于等于 30 的天数:")
    high_temp_count.collect()
    # 5. 找出温度最高的 3 个城市
    top_3_temps = city_temp_rdd.map(lambda x: (x[1], x[0])) \
        .sortByKey(False) \
        .map(lambda x: (x[1], x[0])) \
        .take(3)
    print(top_3_temps)
    sc.stop()

    from pyspark.sql import SparkSession
    from pyspark.sql.functions import col, avg, max, min, collect_list
    spark = SparkSession.builder.appName("MovieRatingAnalysis").getOrCreate()
    # 读取数据
    movies_ratings_df = spark.read.csv("movies_ratings.csv", header=True, inferSchema=True)
    # 注册临时表
    movies_ratings_df.createOrReplaceTempView("movies_ratings")
    # 2. 查询所有电影的标题和类型
    movies_ratings_df.select("title", "genres").distinct().show()
    # 3. 查询评分大于等于 4 的电影及其评分
    movies_ratings_df.filter(col("rating") >= 4).select("title", "rating").show()
    # 4. 统计每部电影的平均评分
    movies_ratings_df.groupBy("movieId",
                              "title").agg(avg("rating").alias("avg_rating")).orderBy("avg_rating",
                                                                                      ascending=False).show()
    # 5. 查询评分次数最多的前 5 部电影
    movies_ratings_df.groupBy("movieId", "title").count().orderBy("count",
                                                                  ascending=False).limit(5).show()
    # 6. 查询每个用户的平均评分
    movies_ratings_df.groupBy("userId").agg(avg("rating").alias("avg_rating")).orderBy("avg_rating",
                                                                                       ascending=False).show()
    # 7. 查询评分在 3 到 5 分之间的用户及其评分电影数量
    movies_ratings_df.filter((col("rating") >= 3) & (col("rating") <=
                                                     5)).groupBy("userId").count().show()
    # 8. 查询类型为 "Comedy" 的电影的平均评分
    movies_ratings_df.filter(col("genres").like("%Comedy%")).groupBy("title").agg(avg
                                                                                  ("rating").alias("avg_rating")).show()
    # 9. 查询每部电影的最高评分和最低评分
    spark.sql("""
              SELECT movieId, title, MAX(rating) as max_rating, MIN(rating) as min_rating
              FROM movies_ratings
              GROUP BY movieId, title
              """).show()
    # 10. 创建视图并查询评分最高的用户及其评分电影列表
    spark.sql("""
              SELECT userId, COLLECT_LIST(title) as movie_list
              FROM movies_ratings
              GROUP BY userId
              ORDER BY AVG(rating) DESC LIMIT 1
              """).show()
    spark.stop()

    # 3.1.1 使用cast函数（考试建议）
    from pyspark.sql import SparkSession
    from pyspark.sql.types import IntegerType, StringType, DoubleType
    spark = SparkSession.builder.appName("TypeConversion").getOrCreate()
    # 示例DataFrame
    data = [("Alice", 34, 5000.50), ("Bob", 45, 6000.75)]
    df = spark.createDataFrame(data, ["name", "age", "salary"])
    # 转换类型
    df_converted_age = df.withColumn("age", df["age"].cast(StringType()))
    df_converted_salary = df.withColumn("salary", df["salary"].cast(IntegerType()))
    # 或
    df_converted_age = df.withColumn("age", df["age"].cast("string"))
    df_converted_salary = df.withColumn("salary", df["salary"].cast("integer"))
    df_converted.show()
    """