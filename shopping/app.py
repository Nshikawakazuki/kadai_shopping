from flask import Flask, render_template, request, redirect, url_for, session
import db, string, random
from datetime import timedelta

app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters, k=256))

@app.route('/', methods=['GET'])
def index():
    msg = request.args.get('msg')
    
    if msg == None:
        return render_template('index.html')
    else:
        return render_template('index.html', msg=msg)

@app.route('/', methods=['POST'])
def login():
    user_name = request.form.get('username')
    password = request.form.get('password')

    if db.login(user_name, password):
        session['user'] = True
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=30)
        return redirect(url_for('home'))
    else :
        error = 'ログインに失敗しました。'
        
        input_data = {'user_name':user_name, 'password':password}
        return render_template('index.html', error=error, data=input_data)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/mypage', methods=['GET'])
def mypage():
    if 'user' in session:
        return render_template('mypage.html')
    else:
        return redirect(url_for('index'))

@app.route('/regstar')
def register_form():
    return render_template('regstar.html')

@app.route('/regstar_exe', methods=['POST'])
def register_exe():
    user_name = request.form.get('user_name')
    mail = request.form.get('mail')
    password = request.form.get('password')
    
    if user_name == '':
        error = 'ユーザー名が入力されていません'
        return render_template('regstar.html', error=error)
    if password == '':
        error = 'パスワードが入力されていません'
        return render_template('regstar.html', error=error)
    if mail == '':
        error = 'メールアドレスが入力されていません'
        return render_template('regstar.html', error=error)

    
    count = db.insert_user(user_name, password, mail)
    
    if count == 1:
        msg = '登録が完了しました'
        return redirect(url_for('index', msg=msg))
    else:
        error = '登録に失敗しました'
        return render_template('regstar.html', error=error)

@app.route('/department')
def department_page():
    return render_template('department.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/sale')
def sale():
    return render_template('sale.html')
@app.route('/life')
def life():
    return render_template('life.html')
@app.route('/food')
def food():
    return render_template('food.html')
@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/merchan')
def merchan():
    return render_template('merchan.html')
@app.route('/merchan_exe', methods=['POST'])
def merchan_exe():
    merchan_name = request.form.get('merchan_name')
    price = request.form.get('price')
    
    if merchan_name == '':
        error = '商品名が入力されていません'
        return render_template('merchan.html', error=error)
    if price == '':
        error = '価格が入力されていません'
        return render_template('merchan.html', error=error)

    
    count = db.insert_merchan(merchan_name, price)
    if count == 1:
        msg = '登録が完了しました'
        return redirect(url_for('mer', msg=msg))
    else:
        error = '登録に失敗しました'
        return render_template('merchan.html', error=error)
     
app.route('/mer', methods=['GET'])
def mer():
    msg = request.args.get('msg')
    
    if msg == None:
        return render_template('merchan.html')
    else:
        return render_template('mrchan.html', msg=msg)
    
@app.route('/list')
def merchan_list():
    merchans = ['畑福人形(等身大)']
    prices = [10]
    return render_template('merchan/list.html', merchans=merchans,prices=prices)

@app.route('/admin_mypage', methods=['GET'])
def admin_mypage():
    if 'admin' in session:
        return render_template('admin_mypage.html')
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)