# import pandas as pd
import pandas as pd
import os
from sqlalchemy import create_engine
from time import time
import argparse


def parser():
    parser = argparse.ArgumentParser(description="Ingest CSV data to Postgres")

    parser.add_argument("--user", help="Postgres username")
    parser.add_argument("--password", help="Postgres password")
    parser.add_argument("--host", help="Postgres host")
    parser.add_argument("--port", help="Postgres exposed port")
    parser.add_argument("--db", help="Database name for postgres")
    parser.add_argument("--table_name", help="Name of the target table ")
    parser.add_argument("--url", help="URL of the csv file")

    args = parser.parse_args()
    return args


def download_data(url, output):
    os.system(f"wget {url} -O {output}")


def main():

    args = parser()
    user = args.user
    password = args.password
    host = args.host
    port = args.port
    db = args.db
    table_name = args.table_name

    print(user)
    if args.url:
        url = args.url
        output = os.path.basename(url)
        download_data(url, output)

    engine = create_engine(
        f"postgresql://{user}:{password}@{host}:{port}/{db}")
    engine.connect()

    df_iter = pd.read_csv(
        "./yellow_tripdata_2022-01.csv",
        parse_dates=["tpep_pickup_datetime", "tpep_dropoff_datetime"],
        iterator=True,
        chunksize=100000,
    )

    print(next(df_iter).columns)

    total_row = 0
    for i, data in enumerate(df_iter, 1):
        row, _ = data.shape
        total_row += row
        time_start = time()
        data.to_sql(name=table_name, con=engine, if_exists="append")
        time_end = time()
        print(
            f"Appending {row} data to {table_name}, took {time_end - time_start} seconds"
        )

    print("Total data inserted: ", total_row)


if __name__ == "__main__":
    main()
