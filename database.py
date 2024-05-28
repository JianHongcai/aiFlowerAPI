import mysql.connector
class dataBaseManager:
    HOST = '1.92.131.215'
    USERNAME = 'aiFlower'
    PASSWORD = '123654987'
    DATABASE = 'aiflower'

    def __init__(self):
        self.db = mysql.connector.connect(
            host=self.HOST,
            user=self.USERNAME,
            password=self.PASSWORD,
            database=self.DATABASE
        )

    def execute_query(self, sql, val=None):
        result = None
        error = None
        try:
            if not self.db.is_connected():
                self.db.reconnect()
            with self.db.cursor() as cursor:
                if val:
                    cursor.execute(sql, val)
                else:
                    cursor.execute(sql)
                result = cursor.fetchone()
                self.db.commit()
        except mysql.connector.Error as e:
            error = str(e)
        return result, error

    def card_exists(self, username):
        sql = "SELECT * FROM user WHERE username =%s"
        val = (username,)
        result, error = self.execute_query(sql, val)
        return result

    def register(self, username, account, password):
        sql = "INSERT INTO user (username, userAccount, userPassword) VALUES (%s, %s, %s)"
        val = (username, account, password)
        result, error = self.execute_query( sql, val)
        if error:
            return {
                'message': '注册失败!!!，请联系管理园!',
                'code': 401
            }
        else:
            return {
                'message': '注册成功',
                'code': 200
            }