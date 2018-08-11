import MySQLdb



def database_write(list_string):
    
    db = MySQLdb.connect('localhost', 'admin', 'bitterwolf', 'roboreef_db')
    curs=db.cursor()
    add_data=("""INSERT INTO robo_data
              (Date, Time ,Temp, pH, ORP,DO,DO2,EC,EC2)
              values (%s,%s, %s,%s,%s,%s,%s,%s,%s)""")
        
    curs.execute(add_data,list_string)
    
    db.commit()
    print(' ')
    db.close()
#db = MySQLdb.connect('localhost', 'admin', 'bitterwolf', 'roboreef_db')
#curs=db.cursor()    
#curs.execute ("SELECT * FROM robo_data")
#x=curs.fetchall()


