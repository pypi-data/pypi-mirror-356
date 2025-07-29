import os

PG_TEST_HOST = os.getenv('PG_TEST_HOST', '127.0.0.1')
PG_TEST_PORT = os.getenv('PG_TEST_PORT', '5432')
PG_TEST_USER = os.getenv('PG_TEST_USER', 'postgres')
PG_TEST_PASSWORD = os.getenv('PG_TEST_PASSWORD', 'example')
