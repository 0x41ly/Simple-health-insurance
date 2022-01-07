from mysql.connector import connect, Error
from db import db_con


print(db_con([f"select Plan_id from Customer where Cust_id='1';"])[0][0][0])