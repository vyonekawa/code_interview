from pyspark.sql import SparkSession
from pyspark.sql.functions import monotonically_increasing_id, col, year, month, dayofmonth, to_date
from pyspark.sql.utils import AnalysisException


def main():
    try:
        # Initialize Spark
        spark = SparkSession.builder \
            .appName("Dimensional Modeling") \
            .getOrCreate()

        # Input/Output file path
        # TODO - criar um arquivo para as variáveis ou configurar em um ambiente de vaiaveis
        raw_data_path = "../data/dados_brutos.csv"
        output_path = "../data"

        # Read raw data
        raw_df = spark.read.option("header", True).csv(raw_data_path)

        # Create Customer Dimension
        dim_customer = raw_df.select("nome_cliente", "cidade", "estado").dropDuplicates()
        dim_customer = dim_customer.withColumn("customer_id", monotonically_increasing_id())

        # Create Product Dimension
        dim_product = raw_df.select("nome_produto", "categoria", "fabricante").dropDuplicates()
        dim_product = dim_product.withColumn("product_id", monotonically_increasing_id())

        # Create Date Dimension
        raw_df = raw_df.withColumn("data", to_date("data", "yyyy-MM-dd"))
        dim_date = raw_df.select("data").dropDuplicates()
        dim_date = dim_date.withColumn("date_id", monotonically_increasing_id())
        dim_date = dim_date.withColumn("year", year("data")) \
                             .withColumn("month", month("data")) \
                             .withColumn("day", dayofmonth("data"))

        # Create Fact Table
        fact_df = raw_df \
            .join(dim_customer, on=["nome_cliente", "cidade", "estado"], how="left") \
            .join(dim_product, on=["nome_produto", "categoria", "fabricante"], how="left") \
            .join(dim_date, on=["data"], how="left")
        fact_sales = fact_df.select(
            monotonically_increasing_id().alias("sale_id"),
            "customer_id", "product_id", "date_id",
            col("qtd_vendida").cast("int").alias("quantity_sold"),
            col("valor_total").cast("double").alias("total_value")
        )

        # Export CSV files
        # dim_customer.coalesce(1).write.csv(f"{output_path}/dim_customer.csv", header=True, mode="overwrite")
        # dim_product.coalesce(1).write.csv(f"{output_path}/dim_product.csv", header=True, mode="overwrite")
        # dim_date.coalesce(1).write.csv(f"{output_path}/dim_date.csv", header=True, mode="overwrite")
        # fact_sales.coalesce(1).write.csv(f"{output_path}/fact_sales.csv", header=True, mode="overwrite")

        # Helper function to save a single CSV in Windows Env
        import os
        import shutil

        def save_as_single_csv(df, output_csv_path):
            temp_dir = output_csv_path + "_temp"
            df.coalesce(1).write.mode("overwrite").option("header", True).csv(temp_dir)
            part_file = [f for f in os.listdir(temp_dir) if f.startswith("part-") and f.endswith(".csv")][0]
            shutil.move(os.path.join(temp_dir, part_file), output_csv_path)
            shutil.rmtree(temp_dir)

        # Save each table
        save_as_single_csv(dim_customer, os.path.join(output_path, "dim_customer.csv"))
        save_as_single_csv(dim_product, os.path.join(output_path, "dim_product.csv"))
        save_as_single_csv(dim_date, os.path.join(output_path, "dim_date.csv"))
        save_as_single_csv(fact_sales, os.path.join(output_path, "fact_sales.csv"))

        # Stop Spark
        spark.stop()
        print("Process completed successfully!")

    except AnalysisException as e:
        print(f"AnalysisException: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()