import base64
from attr import dataclass
import helper
from flask import Flask, abort, jsonify, request, make_response, render_template
import pdfkit
from PIL import Image
import io

app = Flask(__name__)


def check_request(request):
    params = ["nickname", "sex", "email"]
    for i in params:
        if i not in request:
            return True
    return False


@app.route('/todoapp/api/v1.0/todos/<nickname>', methods=['GET'])
def get_todo(nickname):
    # Получаем запись из базы данных
    response = helper.get_todo(nickname)
    
    # Если не найдено - ошибка 404
    if response is None:
        abort(404)
    
    return response


@app.route('/todoapp/api/v1.0/todos', methods=['GET'])
def get_all_todos():
    return helper.get_all_todos()


@app.route('/todoapp/api/v1.0/todos', methods=['POST'])
def add_todo():
    if check_request(request.json):
        abort(400)

    response = helper.add_to_list(request.get_json())
    
    if response is None:
        abort(400)

    return response

@app.route('/todoapp/api/v1.0/todos/<nickname>', methods=['PUT'])
def update_todo(nickname):
    response = helper.get_todo(nickname)
    
    if response is None:
        abort(404)
     
    response = helper.update_todo(nickname, request.get_json())
      
    if response is None:
        abort(400)

    return response

@app.route('/todoapp/api/v1.0/todos/<nickname>', methods = ['DELETE'])
def delete_task(nickname):
    response = helper.get_todo(nickname)

    if response is None:
        abort(404)

    response = helper.remove_todo(nickname)

    return response

@app.route('/pdf/<nickname>', methods = ['GET'])
def get_pdf(nickname):
    data = helper.get_all(nickname)

    # Если не найдено - ошибка 404
    if data is None:
        abort(404)

    
    image = Image.open(io.BytesIO(data["photo"]))
    image.save("picture.jpg")
    im = Image.open("picture.jpg")
    d = io.BytesIO()
    im.save(d, "JPEG")
    encode_ = base64.b64encode(d.getvalue())

    rendered = render_template('html_temp.html', nickname=data["nickname"], photo=encode_.decode('utf-8'),
                                                cnt_game=data["cnt_game"], cnt_win=data["cnt_win"],
                                                cnt_lose=data["cnt_lose"])
    
    pdf = pdfkit.from_string(rendered, False)

    response = make_response(pdf)

    response.headers['Content-Type'] = "application/pdf"
    response.headers['Content-Disposition'] = 'inline;filename=output.pdf'

    return response