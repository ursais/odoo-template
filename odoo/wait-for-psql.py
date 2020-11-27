#!/usr/bin/env python3
import argparse
import logging
import sys
import time

import psycopg2

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--db_host", required=True)
    arg_parser.add_argument("--db_port", required=True)
    arg_parser.add_argument("--db_user", required=True)
    arg_parser.add_argument("--db_password", required=True)
    arg_parser.add_argument("--timeout", type=int, default=5)

    args = arg_parser.parse_args()

    start_time = time.time()
    while (time.time() - start_time) < args.timeout:
        try:
            conn = psycopg2.connect(
                user=args.db_user,
                host=args.db_host,
                port=args.db_port,
                password=args.db_password,
                dbname="postgres",
            )
            error = ""
            break
        except psycopg2.OperationalError as e:
            error = e
        else:
            conn.close()
        time.sleep(1)
    if error:
        logging.error("Database connection failure: %s" % error)
        sys.exit(1)
        