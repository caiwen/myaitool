import base64
import time, hashlib


class MyTools:
    @staticmethod
    def base64_save_img(base64str, img_path):
        imgdata = base64.b64decode(base64str)
        file = open(img_path, 'wb')
        file.write(imgdata)
        file.close()

    @staticmethod
    def create_id():
        m = hashlib.md5(str(time.perf_counter()).encode("utf-8"))
        return m.hexdigest()

    @staticmethod
    def md5(s):
        md5 = hashlib.md5()
        md5.update(s.encode('utf-8'))
        return md5.hexdigest()


if __name__ == '__main__':
    print(MyTools.md5('caiwen123'))
