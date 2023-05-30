import os

from flask import Flask, jsonify, request, session, redirect
from flask import render_template

import approot
from entity.ImgRecordModelEntity import ImgRecordModelEntity
from model.ImgRecordModel import ImgRecordModel
from model.UserModel import UserModel
from service.OpenAi import OpenAi
from tools.mytools import MyTools

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)


@app.route('/login')
def login():
    userinfo = session.get('UserInfo')
    print(userinfo)
    if not userinfo:
        return render_template('login.html')
    else:
        return redirect('/picture')


@app.route('/register')
def register():
    userinfo = session.get('UserInfo')
    print(userinfo)
    if not userinfo:
        return render_template('register.html')
    else:
        return redirect('/picture')


@app.route('/do_login', methods=["POST"])
def do_login():
    account = request.form['account']
    password = request.form['password']
    user_model = UserModel()
    user_info = user_model.get_user_by_login(account, MyTools.md5(password))
    print(user_info)
    if user_info is None:
        return jsonify({
            "code": 1,
            "msg": "用户名或密码错误"
        })

    session['UserInfo'] = {
        'name': user_info['name'],
        'phone': user_info['phone'],
        'account': user_info['account'],
        'id': user_info['id']
    }
    return jsonify({
        "code": 0,
        "msg": ""
    })


@app.route('/do_register', methods=["POST"])
def do_register():
    account = request.form['account']
    password = request.form['password']
    repassword = request.form['repassword']
    phone = request.form['phone']
    if password != repassword:
        return jsonify({
            "code": 1,
            "msg": "两次输入密码不一致"
        })
    print(account, password, repassword, phone)
    user_model = UserModel()
    user_info = user_model.get_user_by_account(account)
    if user_info:
        return jsonify({
            "code": 1,
            "msg": "账号已存在"
        })
    lastrowid = user_model.register_user(name=account, account=account, phone=phone, password=MyTools.md5(password))
    if lastrowid is False:
        return jsonify({
            "code": 1,
            "msg": "注册失败"
        })
    session['UserInfo'] = {
        'name': account,
        'phone': phone,
        'account': account,
        'id': lastrowid
    }
    return jsonify({
        "code": 0,
        "msg": ""
    })


@app.route('/logout')
def log_out():
    session.clear()
    return redirect('/login')


@app.route('/')
def index():
    userinfo = session.get('UserInfo')
    if not userinfo:
        return redirect('/login')
    return redirect('/picture')


@app.route('/chat')
def chat():
    userinfo = session.get('UserInfo')
    if not userinfo:
        return redirect('/login')
    record_model = ImgRecordModel()
    latest_record = record_model.get_latest_record(userinfo['id'])
    latest_record['img_url'] = latest_record['img_url'].split('|')
    print(latest_record)
    return render_template('chat.html', latest_record=latest_record, userinfo=userinfo)


@app.route('/picture')
def picture():
    userinfo = session.get('UserInfo')
    if not userinfo:
        return redirect('/login')
    record_model = ImgRecordModel()
    latest_record = record_model.get_latest_record(userinfo['id'])
    latest_record['img_url'] = latest_record['img_url'].split('|')
    print(latest_record)
    return render_template('picture.html', latest_record=latest_record, userinfo=userinfo)


@app.route('/image/generate', methods=["POST"])
def img_generate():
    userinfo = session.get('UserInfo')
    if not userinfo:
        return jsonify({
            "code": 1,
            "msg": "未登录，请登录"
        })
    prompt = request.form['prompt']
    print(prompt)
    try:
        data = OpenAi.create_image(
            prompt=prompt,
            n=5, size="1024x1024")
    except Exception as e:
        print(repr(e))
        return jsonify({
            "code": 1,
            "msg": repr(e)
        })

    img_name_lists = []
    save_list = []
    datas = data['data']
    for item in datas:
        temp_img_name = MyTools.create_id() + ".jpg"
        MyTools.base64_save_img(item['b64_json'],
                                approot.get_root() + os.sep + 'static' + os.sep + 'images' + os.sep + temp_img_name)
        img_name_lists.append(temp_img_name)

    save_list.append(ImgRecordModelEntity(
        prompt=prompt,
        user_id=userinfo['id'],
        img_url="|".join(img_name_lists)
    ))
    print(img_name_lists)
    record_model = ImgRecordModel()
    print(save_list)
    record_model.batch_save(save_list)
    response = {
        "code": 0,
        "img_list": img_name_lists
    }
    return jsonify(response)


@app.route('/image/record_list')
def record_list():
    userinfo = session.get('UserInfo')
    if not userinfo:
        return jsonify({
            "code": 1,
            "msg": "未登录，请登录"
        })
    page_num = request.args.get('page', 1)
    page_size = request.args.get('limit', 20)
    m = ImgRecordModel()
    rows = m.get_record_list_by_uid(userinfo['id'], page_num, page_size)
    count = m.get_record_cnt(userinfo['id'])
    response = {
        "code": 0,
        "count": count['cnt'],
        "data": rows
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9514)
