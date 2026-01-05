#!/usr/bin/env python
# coding: utf-8

import click
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm


def run(
    year: int,
    month: int,
    pg_user: str,
    pg_pass: str,
    pg_host: str,
    pg_port: int,
    pg_db: str,
    chunksize: int,
    target_table: str,
):

    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
    url = prefix + f'yellow_tripdata_{year}-{month:02d}.csv.gz'



    dtype = {
        "VendorID": "Int64",
        "passenger_count": "Int64",
        "trip_distance": "float64",
        "RatecodeID": "Int64",
        "store_and_fwd_flag": "string",
        "PULocationID": "Int64",
        "DOLocationID": "Int64",
        "payment_type": "Int64",
        "fare_amount": "float64",
        "extra": "float64",
        "mta_tax": "float64",
        "tip_amount": "float64",
        "tolls_amount": "float64",
        "improvement_surcharge": "float64",
        "total_amount": "float64",
        "congestion_surcharge": "float64"
    }

    parse_dates = [
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime"
    ]



    # load a small portion to infer schema (the dtype and parse_dates are provided below)
    df = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
    )

    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

    # print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))


    df_iter = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunksize,
    )

    first = True
    for df_chunk in tqdm(df_iter):
        if first : 
            df_chunk.head(0).to_sql(
                name=target_table, 
                con=engine, 
                if_exists='replace'
                )
            first = False

        print(len(df_chunk))

        df_chunk.to_sql(
            name=target_table,
            con=engine,
            if_exists='append'
            )
        print('Data Inserted')


@click.command()
@click.option('--year', default=2021, type=int, help='Year of the data file')
@click.option('--month', default=1, type=int, help='Month of the data file (1-12)')
@click.option('--pg-user', default='root', type=str, help='Postgres user')
@click.option('--pg-pass', default='root', type=str, help='Postgres password')
@click.option('--pg-host', default='localhost', type=str, help='Postgres host')
@click.option('--pg-port', default=5432, type=int, help='Postgres port')
@click.option('--pg-db', default='ny_taxi', type=str, help='Postgres database name')
@click.option('--chunksize', default=100000, type=int, help='CSV read chunksize')
@click.option('--target-table', default='yellow_taxi_data', type=str, help='Target table name')
def main(year, month, pg_user, pg_pass, pg_host, pg_port, pg_db, chunksize, target_table):
    """CLI entrypoint for data ingestion."""
    run(year, month, pg_user, pg_pass, pg_host, pg_port, pg_db, chunksize, target_table)


if __name__ == '__main__':
    main()