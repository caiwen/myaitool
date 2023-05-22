import os
from vendor.DataBase import DataBase
from vendor.ModConfig import ModConfig


class UserModel(DataBase):
    def __init__(self):
        config = ModConfig()
        dbname = config.getConfig('mychatgpt', 'dbname')
        dbhost = os.getenv('TEST_DB_HOST')
        dbuser = os.getenv('TEST_DB_USER')
        dbpassword = os.getenv('TEST_DB_PWD')
        dbport = config.getConfig("mychatgpt", 'dbport')
        super(UserModel, self).__init__(dbname, dbhost, dbuser, dbpassword, dbport, dbcharset='utf8')

    def get_user_by_account(self, account):
        sql = "SELECT * FROM gpt_user WHERE account='%s' ORDER BY id DESC LIMIT 1"
        return self.fetch_one(sql % (account))

    def get_user_by_login(self, account, password):
        sql = "SELECT * FROM gpt_user WHERE account='%s' AND password='%s' ORDER BY id DESC LIMIT 1"
        return self.fetch_one(sql % (account, password))

    def get_user_by_account(self, account):
        sql = "SELECT * FROM gpt_user WHERE account='%s' ORDER BY id DESC LIMIT 1"
        return self.fetch_one(sql % account)

    def register_user(self, name, account, password, phone):
        sql = "INSERT INTO gpt_user (`name`,`phone`,`account`,`password`) VALUES('%s','%s','%s','%s')" % (
            name, phone, account, password,)
        return self.insert_row(sql)


if __name__ == '__main__':
    model = UserModel()
    print(model.get_user_by_account('caiwen'))
