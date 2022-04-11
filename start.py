import traceback
import time
from db_utils import DBUtils
import pandas as pd
import os
import sys

code_dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(code_dir_path, "..", "data"))
# def setup_postgres():
#     os.system(
#         "docker run --name zluriPostgresDb -p 5455:5432 -e POSTGRES_USER=zluriUser -e POSTGRES_PASSWORD=jarvis -e "
#         "POSTGRES_DB=zluriTransactionDB -v ${HOME}/docker-postgres-data:/var/lib/postgresql/data -d postgres")


if __name__ == '__main__':
    # setup_postgres()
    start_time = time.time()
    util_obj = DBUtils()
    try:
        # create table
        # DROP TABLE IF EXISTS product_details cascade;
        create_table_query = """
                    CREATE TABLE IF NOT EXISTS product_details (
                        sku                 TEXT PRIMARY KEY,
                        name                TEXT,
                        description         TEXT
                    );
                """
        util_obj.execute_query(create_table_query)
        print("product_details table created")
        # create index on name column
        index_query = "CREATE INDEX IF NOT EXISTS idx_product_name ON product_details(name);"
        util_obj.execute_query(index_query)
        print("index created on product_name")
        # read csv file
        file_path = "Zluri_Assignment_Dataset.csv"
        # file_path = "short_data.csv"
        df = pd.read_csv(file_path)
        filtered_df = df.groupby(['sku'], as_index=False).last()

        # insert data
        util_obj.batch_insert(filtered_df, "product_details")

        # create aggregated view
        agg_query = 'CREATE MATERIALIZED VIEW IF NOT EXISTS aggregated_view as select name, count(sku) as "no. of ' \
                    'products" from product_details group by name;'
        util_obj.execute_query(agg_query)
        print("aggregated_view created on product_details table")

        print(f"total time taken: {time.time() - start_time} sec")
        # if needed, refresh aggregated view. Assuming aggregation is needed less frequently
        # refresh_query = "REFRESH MATERIALIZED VIEW CONCURRENTLY aggregated_view"
        # util_obj.execute_query(refresh_query)
    except Exception as e:
        print(traceback.format_exc())
    finally:
        util_obj.cursor.close()
        util_obj.connection_object.close()
