import mysql.connector
import uuid


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

    def execute_query(self, sql, val=None, is_select=False):
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

                if is_select:
                    result = cursor.fetchall()  # 获取查询结果
                    if not result:
                        result = None

                else:
                    result = cursor.rowcount  # 获取受影响的行数

                self.db.commit()
        except mysql.connector.Error as e:
            error = str(e)

        return (result, error)  # 返回元组形式的结果和错误信息

    def user_exists(self, userAccount):
        sql = "SELECT * FROM user WHERE userAccount =%s"
        val = (userAccount,)
        result, error = self.execute_query(sql, val, is_select=True)
        return result

    def collate_token(self, token):
        sql = "SELECT * FROM user WHERE token =%s"
        val = (token,)
        result, error = self.execute_query(sql, val)
    def getInfo(self,account):
        sql = "SELECT * FROM user where userAccount = %s"
        val = (account,)
        result, error = self.execute_query(sql,val,is_select=True)
        print(result)
        return result
    def register(self, account, password):
        try:
            sql = "INSERT INTO user ( userAccount, userPassword,token,updateTime,username) VALUES ( %s, %s,%s,NOW(),%s)"
            token = uuid.uuid4().hex
            name = f'用户{account}'
            val = (account, password, token,name)
            result, error = self.execute_query(sql, val, is_select=False)
            if error:
                return {
                    'message': f'注册失败 {error}',
                    'code': 400
                }, 400
            else:
                if result >0:
                    return {
                        'message': '注册成功',
                        'token': token,
                        'code': 200,
                        'name':name
                    }, 200
                else:
                    return {
                        'message': '注册失败',
                        'code': 400
                    }, 400
        except Exception as e:
            return {
                'message': '注册失败，发生异常: {}'.format(str(e)),
                'code': 500
            }, 500

    def login(self, account, password):
        try:
            sql = "UPDATE user set token = %s WHERE userAccount = %s and userPassword = %s"
            token = uuid.uuid4().hex
            val = (token, account, password)
            result, error = self.execute_query(sql, val, is_select=False)
            if error:
                return {
                    'message': f'登录失败，{error}',
                    'code': 400
                }, 400
            else:
                if result > 0:  # 检查受影响的行数来判断登陆成功
                    info = self.getInfo(account)[0]
                    print(info)
                    return {
                        'message': '登录成功',
                        'token': token,
                        'name':info[1],
                        'code': 200
                    }, 200
                else:  # 否则表示用户名或密码错误
                    return {
                        'message': '用户名或密码错误',
                        'code': 400
                    }, 400
        except Exception as e:
            return {
                'message': '登录失败，发生异常: {}'.format(str(e)),
                'code': 500
            }, 500
