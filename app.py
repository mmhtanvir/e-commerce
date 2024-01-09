from flask import Flask, url_for, render_template, redirect, request, session
import uuid
from flask_mysqldb import MySQL
import mysql.connector

app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = 'static/images'


app.secret_key = 'your-secret-key'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'rafiath'  
# get data with db column name instead of index
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

@app.route("/")
def index():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM items ORDER BY id DESC")
        items = cur.fetchall()
        cur.close()


        if 'email' in session:
            email = session['email']
        else:
            email = None 
        return render_template('index.html', email = email, items=items)

@app.route("/cart")
def cart():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM cart")
    item = cur.fetchall()
    cur.close()

    return redirect(url_for('index', item = item))

@app.route("/item", methods=['GET', 'POST'])
def item():
    cur = mysql.connection.cursor()

    if request.method == "POST":
        product_name = request.form['product_name']
        price = request.form['price']
        available_quantity = request.form['available_quantity']
        description = request.form['description']
        img = str(uuid.uuid4())
        img1 = str(uuid.uuid4())
        m_image = request.files['m_image']
        m_image.save('static/images/' + img + '.jpg')
        m_image_filename = 'images/' + img + '.jpg'
        xtra_image = request.files['xtra_image']
        xtra_image.save('static/images/' + img1 + '.jpg')
        xtra_image_filename = 'images/' + img1 + '.jpg'

        
        print(img)
        print(img1)

        try:
            cur.execute("INSERT INTO items (product_name, price, available_quantity, description, m_image, xtra_image) VALUES (%s, %s, %s, %s, %s, %s)",
                        (product_name, price, available_quantity, description, m_image_filename, xtra_image_filename),)
            mysql.connection.commit()
        except Exception as e:
            print(f"Error: {e}")
            mysql.connection.rollback() 

    session['item'] = {'key': 'value'}

    # Perform any additional operations with 'cur' if needed

    return redirect(url_for('admin'))


@app.route("/favorite")
def favorite():
        return redirect(url_for('index'))

@app.route('/delete/<string:id>', methods = ['GET', 'POST'])
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM cart WHERE id = %s", [id])
    mysql.connection.commit()
    return redirect(url_for('index'))

@app.route("/category")
def category():
        return render_template('category.html')

@app.route("/feelona-admin")
def admin():
    item = session.get('item', None)

    return render_template('admin.html', item=item)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        sql = "SELECT id, email, password from users WHERE email = %s"
        cur = mysql.connection.cursor()
        cur.execute(sql, (email,))
        user = cur.fetchone()
        cur.close()

        if user and password == user['password']:
            session['email'] = user['email']

            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid email or Password")

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        cur = mysql.connection.cursor()

        sql = "INSERT INTO users (name, email, password) VALUES(%s, %s, %s)"
        data = (name, email, password)
        cur.execute(sql, data)
        cur.close()
        mysql.connection.commit()
        return redirect(url_for('login'))

    return render_template('sign_up.html')

@app.route('/fflog', methods=['GET', 'POST'])
def flogin():

    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']

        sql = "SELECT id, user_id, password FROM admin WHERE user_id = %s"
        cur = mysql.connection.cursor()
        cur.execute(sql, (user_id,))
        user = cur.fetchone()
        cur.close()

        if user and password == user['password']:
            session['user_id'] = user['user_id']
            return redirect(url_for('admin'))
        else:
            return render_template('admin_login.html', error="Invalid id or Password")

    return render_template('admin_login.html')

@app.route('/ffid', methods=['GET', 'POST'])
def fsignup():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        user_id = request.form['user_id']
        password = request.form['password']
        
        cur = mysql.connection.cursor()

        # Check if the id already exists in the database
        cur.execute("SELECT * FROM admin WHERE user_id = %s", (user_id,))
        existing_user = cur.fetchone()

        if existing_user:
            cur.close()
            return render_template('admin_sign_up.html', error = "User ID already exists. Please choose a different user id.")
        else:
            # Insert new user data into the database
            sql = "INSERT INTO admin (name, email, password, user_id) VALUES(%s, %s, %s, %s)"
            data = (name, email, password, user_id)
            cur.execute(sql, data)
            cur.close()
            mysql.connection.commit()
            return redirect(url_for('flogin'))

    return render_template('admin_sign_up.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)