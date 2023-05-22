import approot
import string


class SqlTemplate:
    @staticmethod
    def template(tpl_name):
        path = approot.get_root() + "/templates/sqltpl/" + tpl_name
        with open(path) as file_object:
            return file_object.read()


if __name__ == '__main__':
    print(SqlTemplate.template('img_record_list.tpl'))
    sql = string.Template(SqlTemplate.template('img_record_list.tpl')).substitute(user_id=1, offset=0, page=1)
    print(sql)
