import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    '''
    Dropping all tables.
    :param cur: Cursor used to execute query.
    :param conn: Connection used to commit changes.
    :return: No return value.
    '''
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()

def create_tables(cur, conn):
    '''
    Creating staging, fact and dimension table schemas.
    :param cur: Cursor used to execute query.
    :param conn: Connection used to commit tables.
    :return: No return value.
    '''
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()

def main():
    '''
    Main function drops all tables and recreates them according to configuration stored in 'dwh.cfg' file.
    :return: No return values.
    '''
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
