from flask import Flask, render_template, request, redirect, session
import pymysql

app = Flask(__name__)
app.secret_key = "bank_secret"

# Database connection
db = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    database="bank_db"
)

@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        # Naya login karne se pehle purana session clear karein
        session.clear() 
        
        email = request.form['email']
        password = request.form['password']

        cur = db.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cur.fetchone()

        if user:
            session['user_id'] = user[0] # User ID session mein save karein
            return redirect('/dashboard')
        else:
            return "Invalid Credentials"
    return render_template("login.html")

# account_no = request.form.get('account_no', 'BOI' + name[:3].upper() + '001')


@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        mobile = request.form['mobile']
        address = request.form['address']  # Yeh line check karein
        account_no = request.form.get('account_no', 'BOI' + name[:3].upper() + '001')

        cur = db.cursor()
        # Query mein address (6th column) ko add karein
        cur.execute("""
            INSERT INTO users(name, email, password, account_no, mobile, address) 
            VALUES(%s, %s, %s, %s, %s, %s)
        """, (name, email, password, "BOI"+mobile[-4:], mobile, address))
        db.commit()
        return redirect('/')
    return render_template("register.html")

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')

    cursor = db.cursor()
    # Dashboard par bhi sirf wahi user ki info dikhayien jo logged in hai
    cursor.execute("SELECT * FROM users WHERE id=%s", (session['user_id'],))
    user = cursor.fetchone()

    return render_template('dashboard.html', user=user)


@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect('/')

    cursor = db.cursor()
    # Session wali ID se data fetch karna taaki naye user ko purana data na dikhe
    cursor.execute("SELECT name, account_no, mobile, email, address, bank_name, branch FROM users WHERE id=%s", (session['user_id'],))
    user_info = cursor.fetchone()

    print(user_info)
    return render_template('profile.html', user=user_info)


@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    if 'user_id' not in session:
        return redirect('/')

    if request.method == 'POST':
        amount = int(request.form.get('amount'))
        user_id = session['user_id']

        cursor = db.cursor()
        # User ka naam fetch karein transaction history ke liye
        cursor.execute("SELECT name FROM users WHERE id=%s", (user_id,))
        name = cursor.fetchone()[0]

        # 1. Balance update karein
        cursor.execute("UPDATE users SET balance = balance + %s WHERE id = %s", (amount, user_id))
        
        # 2. Transaction table mein entry daalein
        cursor.execute(
            "INSERT INTO transactions (user_id, name, type, amount) VALUES (%s, %s, %s, %s)",
            (user_id, name, 'Deposit', amount)
        )

        db.commit()
        return redirect('/dashboard')
    
    return render_template('deposit.html')


@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    if 'user_id' not in session:
        return redirect('/')

    if request.method == 'POST':
        amount = int(request.form['amount'])
        user_id = session['user_id']

        cursor = db.cursor()
        cursor.execute("SELECT name, balance FROM users WHERE id=%s", (user_id,))
        user_data = cursor.fetchone()
        name = user_data[0]
        current_balance = user_data[1]

        if amount > current_balance:
            return "Insufficient Balance!"

        cursor.execute("UPDATE users SET balance = balance - %s WHERE id = %s", (amount, user_id))
        cursor.execute(
            "INSERT INTO transactions (user_id, name, type, amount) VALUES (%s, %s, %s, %s)",
            (user_id, name, 'Withdraw', amount)
        )

        db.commit()
        return redirect('/dashboard')

    return render_template('withdraw.html')

@app.route('/transactions')
def transactions():
    # Agar user logged in nahi hai, toh login page par bhejein
    if 'user_id' not in session:
        return redirect('/')
        
    user_id = session['user_id']
    cursor = db.cursor()
    
    # Sirf logged-in user ki transactions fetch karein
    cursor.execute("SELECT * FROM transactions WHERE user_id=%s ORDER BY date DESC", (user_id,))
    data = cursor.fetchall()
    
    return render_template('transactions.html', data=data)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)