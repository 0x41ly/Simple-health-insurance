from mysql.connector import connect, Error


def db_con(query):
    try:
        myhost = 'localhost'
        mydatabase = 'health_insurance_company'
        myuser = 'root'
        mypass = ''

        connection = connect(host = myhost,
                      database = mydatabase,
                      user = myuser,
                      password = mypass)

        records = []
        cur = connection.cursor()
        for i in query:
            cur.execute(i)
            records.append(cur.fetchall())
        cur.close()
        connection.commit()
        connection.close()
        
        return records
        
    except Error as e:
        return e

