from flask import Flask, url_for, render_template, redirect, request, session, g
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

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='rafiath'
)

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
    if request.method == "POST":
        item_id = request.form.get('item_id')
        available_quantity = int(request.form.get('available_quantity'))
        price = request.form.get('price')
        m_image = request.form.get('m_image')

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM items WHERE item_id = %s available_quantity = %s price = %s m_image = %s", (item_id, available_quantity, price, m_image, ))
        existing_item = cur.fetchone()

        if existing_item:
            cur.close()
            return render_template('index.html')
        else:
            # Insert new user data into the database
            sql = "INSERT INTO cart (item_id, available_quantity, price, m_image) VALUES(%s, %s, %s, %s)"
            data = (item_id, available_quantity, price, m_image)
            cur.execute(sql, data)
            cur.close()
            mysql.connection.commit()

        return redirect(url_for('index'))

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
                        (product_name, price,  available_quantity, description, m_image_filename, xtra_image_filename),)
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

@app.route("/category")
def category():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM items")
    items = cur.fetchall()
    cur.close()

    return render_template('category.html', item = items)

@app.route("/category/<string:category>")
def categoryitem():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM items")
    items = cur.fetchall()
    cur.close()
    
    
    cur = mysql.connection.cursor()

    if category == "":
        cur.execute("SELECT * FROM ")
        items = cur.fetchall()
    elif category == "":
        cur.execute("SELECT * FROM ")
        items = cur.fetchall()

    cur.close()

    return render_template('category-item.html', items = items)

@app.route("/33214r")
def admin():
    items = session.get('item', None)

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM items")
    items = cur.fetchall()
    cur.close()

    if 'user_id' in session:
        user_id = session['user_id']
    else:
        user_id = None  

    return render_template('admin.html', items = items, user_id = user_id) 

@app.route('/edit/<string:id>', methods=['GET', 'POST'])
def edit(id):
    items = session.get('item', None)
    
    if request.method == 'POST':
        id = request.form['id']
        product_name = request.form['product_name']
        price = request.form['price']
        available_quantity = request.form['available_quantity']
        sql = f"UPDATE items SET product_name = '{product_name}', price = '{price}', available_quantity = '{available_quantity}' WHERE id = {id}"
        print(sql)
        cur = mysql.connection.cursor()
        cur.execute(sql)
        mysql.connection.commit()

    return render_template('edit.html', items=items)

from flask import Flask, render_template, request, session


# ... (previous imports and configurations) ...

@app.route('/review/<string:id>', methods=['GET', 'POST'])
def review(id):
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        username = request.form['username']
        comment = request.form['comment']
        rating = request.form['rating']

        try:
            cur.execute("INSERT INTO reviews (id, username, comment, rating) VALUES (%s, %s, %s, %s)",
                        (id, username, comment, rating))
            mysql.connection.commit()
        except Exception as e:
            print(f"Error: {e}")
            mysql.connection.rollback()

    # Fetch id from the items table and name from the users table
    cur.execute("SELECT * FROM items WHERE id = %s", (id,))
    items = cur.fetchone()

    # Fetch reviews for the specific item
    reviews = cur.fetchall()

    cur.close()

    return render_template('review.html', item=items, reviews=reviews)

# ... (previous routes) ...






# Delete route
@app.route('/delete/<string:id>', methods=['POST'])
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM items WHERE id = %s", (id,))
    mysql.connection.commit()
    return redirect(url_for('admin'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'email' in session:
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
    if 'username' in session:
        return redirect(url_for('index'))

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

@app.route('/signout')
def signout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)