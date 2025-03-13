from flask import Flask, request, render_template, redirect, url_for, make_response

app = Flask(__name__)

# Страница с формой для ввода данных
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

# Выход и удаление cookie
@app.route('/logout', methods=['POST'])
def logout():
    response = make_response(redirect(url_for('mail')))
    response.set_cookie('username', '', expires=0)  # Удаляем cookie
    return response

if __name__ == '__main__':
    app.run(debug=True)