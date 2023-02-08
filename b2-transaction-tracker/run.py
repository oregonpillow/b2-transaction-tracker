import os
from reporter import Reporter

instance = Reporter(
    b2_email = os.environ.get('B2_EMAIL'),
    b2_pwd = os.environ.get('B2_PWD'),
    db_host = os.environ.get('DB_HOST', 'b2-db'),
    db_user = os.environ.get('DB_USER', 'user'),
    db_pwd = os.environ.get('DB_PWD', 'password'),
    db_port = os.environ.get('DB_PORT', '3306'),
    db_name = os.environ.get('DB_NAME', 'b2'),
    timestamp = os.environ.get('TIMESTAMP', 'true'),
    )
