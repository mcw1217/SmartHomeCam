from flask_mysqldb import MySQL
import MySQLdb.cursors
import bcrypt

from app001.routes import app

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'pythondb'
app.config['MYSQL_PORT'] = 3306

# Intialize MySQL
mysql = MySQL(app)

class User():
    def login_check(input_username, input_password):
        # bcrypt hash transfer
        input_password = input_password.encode('utf-8')
        # MySQL DB에 해당 계정 정보가 있는지 확인
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(f'SELECT * FROM accounts WHERE username = "{input_username}"') 
        # 값이 유무 확인 결과값 account 변수로 넣기
        account = cursor.fetchone()
        if account:
            check_password = bcrypt.checkpw(input_password, account['password'].encode('utf-8'))
            return account, check_password
        return None, False      
    def get_information(id):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', id)
        account = cursor.fetchone()
        return account
    
    def update_fromip(fromip, id):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE accounts SET fromip=%s WHERE id=%s', (fromip, str(id)))
        mysql.connection.commit()
        
    def useradd(username, password, email):
        # bcrypt hash transfer
        password = (bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())).decode('utf-8')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO accounts (username, password, email, role) VALUES (%s, %s, %s,%s)", (username, password, email,"일반 회원"))
        mysql.connection.commit()
        
    def check_username_exist(username):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(f'SELECT * FROM accounts WHERE username="{username}"')
        account = cursor.fetchone()
        return account
          
    def check_email_exist(email):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(f'select * from accounts where email= "{email}"')
        account = cursor.fetchone()
        return account

    def update_survey(userid,survey_content, hospital, y, m, d):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO survey (userid,survey_content, hospital, y, m, d) VALUES (%s,%s, %s, %s,%s,%s)", (str(userid),survey_content, str(hospital), str(y), str(m), str(d)))
        mysql.connection.commit()

    def get_bookinglist(id):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(f"select * from survey where hospital={id}")
        booking = dict()
        for i,fet in enumerate(cursor.fetchall()):
            booking[i] = fet
        return booking

    def delete_booking(hospital, userid,y,m,d):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(f"delete from survey where hospital={hospital} and userid={userid} and y={y} and m={m} and d={d}")
        mysql.connection.commit()

    def save_survey(survey_content):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(f"INSERT INTO save_survey (survey_content) VALUES ({survey_content})")
        mysql.connection.commit()
        
    def get_save_survey():
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from save_survey")
        booking = list()
        for fet in cursor.fetchall():
            fet = fet['survey_content']
            fet = fet.split(",")
            booking.append(fet)
        return booking
        
    


    
        
        
        
                       
      