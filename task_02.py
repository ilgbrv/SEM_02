from flask import Flask, flash, request, render_template, redirect, url_for, abort, make_response
from markupsafe import escape

app = Flask(__name__)

app.secret_key = b'5f214cacbd30c2ae4784b520f17912ae0d5d8c16ae98128e3f549546221265e4'


@app.route('/base', methods=['GET', 'POST'])
def base():
    if request.method == 'POST':
        username = request.form.get('username')
    return render_template('base.html')



@app.route('/greeting_page/<name>')
def greeting_page(name):
    return f'''
    <h2>Здравствуйте, { name }!</h2>
    <p>Вы успешно отправили своё имя.</p>
    <a href="/base">Назад</a>
    '''


@app.route('/image')
def image():
    return render_template('image.html')

@app.route('/upload_image', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        file = request.files.get('image')
        if file:
            file.save(f"static/{file.filename}")
            return f'Изображение {file.filename} загружено!'
    return '''
    <h2>Загрузите изображение</h2>
    <form action="/upload_image" method="POST" enctype="multipart/form-data">
        <input type="file" name="image" required>
        <button type="submit">Загрузить</button>
    </form>
    <br>
    <a href="/image"><button>Назад</button></a>
    '''


@app.route('/authorization', methods=['GET', 'POST'])
def authorization():
    if request.method == 'POST':
        login = request.form.get('username')
        password = request.form.get('password')

        print(f"Login: {login}, Password: {password}")

        if login == 'admin' and password == '12345':
            return redirect(url_for('status', message='welcome', username=login))
        else:
            return redirect(url_for('status', message='error'))
    return render_template('authorization.html')


@app.route('/status')
def status():
    message = request.args.get('message')
    username = request.args.get('username')

    if message == 'welcome' and username:
        return f'''
            <h2>Добро пожаловать, {username}!</h2>
            <p>Вы успешно вошли в систему.</p>
            <a href="/authorization">Выйти</a>
        '''
    else:
        return '''
            <h2>Ошибка авторизации</h2>
            <p>Неверный логин или пароль.</p>
            <a href="/authorization">Попробовать снова</a>
        '''


        
@app.route('/text', methods=['GET', 'POST'])
def text():
    if request.method == 'POST':
        user_text = request.form.get('user_text')
        word_count = len(user_text.split())
        return redirect(url_for('result', text=user_text, word_count=word_count))
    return render_template('text.html')

@app.route('/result')
def result():
    user_text = request.args.get('text')
    word_count = request.args.get('word_count', type=int) 
    return f'''
    <h2>Вы ввели следующий текст:</h2>
    <p>{ user_text }</p>

    <h3>Количество слов в тексте:</h3>
    <p>{ word_count }</p>
    <br>
    <a href="/text"><button>Назад</button></a>
    '''

@app.route('/calculate', methods=['GET', 'POST'])
def calculate():
    if request.method == 'POST':
        first_number = float(request.form.get('first_number'))
        second_number = float(request.form.get('second_number'))
        operation = request.form.get('operation')

        if operation == 'add':
            result = first_number + second_number
        elif operation == 'subtract':
            result = first_number - second_number
        elif operation == 'multiply':
            result = first_number * second_number
        elif operation == 'divide':
            if second_number == 0:
                return 'Ошибка: Деление на ноль!'
            result = first_number / second_number

        return redirect(url_for('res', result=result))
    return render_template('calculate.html')

@app.route('/res')
def res():
    result = request.args.get('result')
    result = int(float(result))
    return f'''
            <h2>Результат:</h2>
            <p>{result}</p>
            <br>
            <a href="/calculate"><button>Попробовать снова</button></a>
        '''
 
@app.errorhandler(403)
def access_denied(e):
    context = {
        'title': 'Доступ запрещен по возрасту',
        'url': request.base_url,
    }
    return render_template('403.html', **context), 403



@app.route('/age', methods=['GET', 'POST'])
def age():
    MIN_AGE = 18
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        user_age = request.form.get('user_age')
        if int(user_age) >= MIN_AGE:
            return f'{user_name}, Вы вошли!'
        else:
            abort(403)
    return render_template('age.html')
    
  
@app.route('/square', methods=['GET', 'POST'])
def square():
    NUMBER = 5
    return redirect(url_for('square_res', number=int(NUMBER**2)))

@app.route('/square/<int:number>')
def square_res(number: int):
    NUMBER = 5
    return str(number)


@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        if not request.form['name']:
            flash('Введите имя!', 'danger')
            return redirect(url_for('form'))
        flash('Форма успешно отправлена!', 'success')
        return redirect(url_for('form'))
    return render_template('form.html')



@app.route('/mail', methods=['GET', 'POST'])
def mail():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        user_email = request.form.get('user_email')

        if not user_name or not user_email:  
         return "Ошибка: заполните все поля!", 400

        response = make_response(redirect(url_for('welcome')))  
        response.set_cookie('username', user_name)  
        return response

    return render_template('mail.html')  

@app.route('/welcome')
def welcome():
    user_name = request.cookies.get('username')

    if not user_name:  
        return redirect(url_for('mail'))

    return f'''
    <h1>Добро пожаловать, {user_name}!</h1>
    <form action="{url_for('logout')}" method="POST">
        <button type="submit">Выйти</button>
    </form>
    '''

@app.route('/logout', methods=['POST'])
def logout():
    response = make_response(redirect(url_for('mail')))
    response.set_cookie('username', '', expires=0)  # Удаляем cookie
    return response


if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True)