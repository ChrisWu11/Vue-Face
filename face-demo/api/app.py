import os, base64
from flask import Flask, request, Response, render_template

app = Flask(__name__)


@app.route("/test/")
def test():
    return "hello world"


@app.route('/register/', methods=['POST'])
def register():
    img = request.files.get('photo')  # 从post请求中获取图片数据
    username = request.form.get('username', '')
    suffix = '.' + img.filename.split('.')[-1]  # 获取文件后缀名
    basedir = os.path.abspath(os.path.dirname(__file__))  # 获取当前文件路径
    photo = '/static/uploads/' + username + suffix  # 拼接相对路径
    img_path = basedir + photo  # 拼接图片完整保存路径,时间戳命名文件防止重复
    img.save(img_path)  # 保存图片

    return {'msg': 'ok'}


@app.route('/check', methods=['POST'])
def check():
    src = request.data
    print(src)
    data = str(src).split(',')[1][:-3]
    img_data = base64.b64decode(data)
    with open("./test/temp.png", 'wb') as f:
        f.write(img_data)

    return {'msg': 'ok'}


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000)
