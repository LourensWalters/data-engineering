import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries

def load_staging_tables(cur, conn):
    '''
    Copy data from S3 to Redshift staging tables.
    :param cur: Cursor used to execute query.
    :param conn: Connection used to commit changes.
    :return: No values returned.
    '''
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    '''
    Insert data into Redshift dimensional tables from staging tables.
    :param cur: Cursor used to execute query.
    :param conn: Connection used to commit changes.
    :return: No values returned.
    '''
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    '''
    Main function loads staging tables from S3 and then inserts data into dimensional model tables according to
    configuration stored in 'dwh.cfg' file.
    :return: No return values.
    '''
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()