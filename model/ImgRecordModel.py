from tools.SqlTemplate import SqlTemplate
from vendor.DataBase import DataBase
from vendor.ModConfig import ModConfig
import string, os


class ImgRecordModel(DataBase):
    def __init__(self):
        config = ModConfig()
        dbname = config.getConfig('mychatgpt', 'dbname')
        dbhost = os.getenv('TEST_DB_HOST')
        dbuser = os.getenv('TEST_DB_USER')
        dbpassword = os.getenv('TEST_DB_PWD')
        dbport = config.getConfig("mychatgpt", 'dbport')
        super(ImgRecordModel, self).__init__(dbname, dbhost, dbuser, dbpassword, dbport, dbcharset='utf8')

    def batch_save(self, models: list):
        key_fields = list(models[0].__dict__.keys())
        key_fields = ','.join(key_fields)
        print(key_fields)
        insert_data = []
        for mode in models:
            value = map(lambda x: "'" + str(x) + "'", list(mode.__dict__.values()))
            value = ','.join(value)
            insert_data.append('(' + value + ')')
        insert_data = ','.join(insert_data)
        sql = "INSERT INTO gpt_img_record (" + key_fields + ") VALUES %s" % (
            insert_data)
        print(sql)
        return self.execute(sql)

    def get_record_list_by_uid(self, uid, page_num, page_size):
        offset = (int(page_num) - 1) * int(page_size)
        tpl = SqlTemplate.template('img_record_list.tpl')
        sql = string.Template(tpl).substitute(user_id=uid, offset=offset, page_size=page_size)
        return self.parse_list(self.fetch_all(sql))

    def get_record_cnt(self, uid):
        tpl = SqlTemplate.template('img_record_cnt.tpl')
        sql = string.Template(tpl).substitute(user_id=uid)
        return self.fetch_one(sql)

    @staticmethod
    def parse_list(rows):
        my_rows = []
        for row in rows:
            row['created_time'] = row['created_time'].strftime('%Y-%m-%d %H:%M:%S')
            row['updated_time'] = row['updated_time'].strftime('%Y-%m-%d %H:%M:%S')
            my_rows.append(row)
        return my_rows

    def get_latest_record(self, uid):
        tpl = SqlTemplate.template('latest_record.tpl')
        sql = string.Template(tpl).substitute(user_id=uid)
        return self.fetch_all(sql)


if __name__ == '__main__':
    m = ImgRecordModel()
    rows = m.get_record_list_by_uid(1, 1, 20)
    print(rows)
