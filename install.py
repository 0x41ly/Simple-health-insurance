from os import system
from mysql.connector import connect, Error
 
cmd = 'pip3 install -r requirements.txt'
system(cmd)

try:  
  connection = connect(
    host="localhost",
    user="root",
    password=""
  )

  cur = connection.cursor()


  f = open("Health_insurance_company.sql", "r")
  cur.execute(f.read())
  cur.fetchall()
  cur.close()
  connection.close()
except Error as e:
  print(e)