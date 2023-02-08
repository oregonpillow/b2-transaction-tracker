import mysql.connector as sql


class DataDumper():


  def __init__(self, db_host, db_user, db_pwd, db_port, db_name, table_name):

    self.db_host = db_host
    self.db_user = db_user
    self.db_pwd = db_pwd
    self.db_port = db_port
    self.db_name = db_name
    self.tbl_name = table_name

    self.connect_db()
    self.setup_db()
  

  def connect_db(self):

    self.connection = sql.connect(
    host = self.db_host,
    user = self.db_user,
    password = self.db_pwd)

    print(self.connection)
    self.cursor = self.connection.cursor()


  def setup_db(self):
  
    self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_name}")
    self.cursor.execute(f"USE {self.db_name};")

    table_setup = f"""CREATE TABLE IF NOT EXISTS {self.tbl_name}(
    transaction_name VARCHAR(100),
    transaction_count MEDIUMINT(20),
    transaction_type CHAR(1),
    date DATETIME,
    PRIMARY KEY(transaction_name, date));"""

    self.cursor.execute(table_setup)


  def update_db(self, data):

    update_values = f"""INSERT INTO {self.tbl_name} 
    (transaction_name, transaction_count, transaction_type, date)
    VALUES ({",".join(data)})
    ON DUPLICATE KEY UPDATE 
    transaction_name={data[0]}, transaction_count={data[1]}, transaction_type={data[2]};"""

    self.cursor.execute(update_values)
    self.connection.commit()


  def disconnect_db(self):
    self.connection.close()
