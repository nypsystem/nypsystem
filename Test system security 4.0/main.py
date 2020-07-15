from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from cryptography.fernet import Fernet
from itsdangerous import SignatureExpired, URLSafeTimedSerializer
from flask_wtf.csrf import CSRFProtect
from form import RegisterForm, LoginForm
import MySQLdb.cursors
import bcrypt
from flask_mail import Mail, Message


app = Flask(__name__)
# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'systemsecurity'
csrf = CSRFProtect(app)
# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'systemsecurity'
app.config['MYSQL_PASSWORD'] = 'systemsecurity'  # Change to own account password
app.config['MYSQL_DB'] = 'systemsecurity'

app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Lc126kZAAAAAIeFBGu9dsBlAwOudaVXSoUdveW9'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6Lc126kZAAAAAAMqDIJ54D_8obQMsdJ1uY-2PQcr'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'black'}

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'wakextuptodrinkmilk@gmail.com'
app.config['MAIL_PASSWORD'] = 'king48YU421'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

# Intialize MySQL
mysql = MySQL(app)
mail = Mail(app)
s = URLSafeTimedSerializer(app.secret_key)


# http://localhost:5000/MyWebApp/ - this will be the login page, we need to use both GET and POST requests


@app.route('/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'], email=session['email'])

    # If User is not loggedin, redirect to login page
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    form = RegisterForm()
    # Post Request
    if request.method == 'POST':
        if form.validate_on_submit():
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            mobile = request.form['mobile']

            token = s.dumps(email, salt='email-confirm')
            msg = Message('Confirm Email', sender='wakextuptodrinkmilk@gmail.com', recipients=[email])
            link = url_for('confirm_email', token=token, _external=True)
            msg.body = 'Your link is {} \n The link will expire in 5 Minutes'.format(link)
            mail.send(msg)

            salt = bcrypt.gensalt(rounds=16)
            hash_password = bcrypt.hashpw(password.encode(), salt)

            key = Fernet.generate_key()
            f = Fernet(key)
            n = Fernet(key)
            encryptedEmail = f.encrypt(email.encode())
            encryptedMobile = n.encrypt(mobile.encode())

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO accounts VALUES(NULL, %s, %s, %s, %s,%s, %s)',
                           (username, hash_password, encryptedEmail, key, encryptedMobile, 0))
            mysql.connection.commit()
            # Register Success
            return render_template("register.html", form=form, msg='You have successfully registered!')
        # Input Error
        else:
            return render_template("register.html", form=form, msg=form)
    # Get Request
    else:
        return render_template('register.html', msg=msg, form=form)


@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ""
    form = LoginForm()
    # Post Request
    if request.method == 'POST':
        if form.validate_on_submit():
            username = request.form['username']
            password = request.form['password']


            # Check if account exists in MySQL
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
            account = cursor.fetchone()

            # If Account Exist
            if account:
                if int(account['admin']) == 0:
                    # Extract the Salted-hash password from DB to local variable
                    hashAndSalt = account['password']
                    # Convert salted-hash password to bytes by using the .encode() method
                    # bycrypt.checkpw() will verify if the password input by user matches that from the database
                    if bcrypt.checkpw(password.encode(), hashAndSalt.encode()):
                        key = account['symmetrickey']
                        f = Fernet(key)
                        n = Fernet(key)
                        # Call f.decrypt() to decrypt the data. Convert data from Database to bytes/binary by using .encode()
                        decryptedEmail_Binary = f.decrypt(account['email'].encode())
                        decryptedMobile_Binary = f.decrypt(account['mobile'].encode())
                        # call .decode () to convert from Binary to String – to be displayed in Home.html.
                        decryptedEmail = decryptedEmail_Binary.decode()
                        decryptedMobile = decryptedMobile_Binary.decode()
                        # Create session data, we can access this data in other routes
                        session['loggedin'] = True
                        session['id'] = account['id']
                        session['username'] = account['username']
                        session['email'] = decryptedEmail
                        session['mobile'] = decryptedMobile

                        # redirect to home page
                        return redirect(url_for('home'))
                    else:
                        # password incorrect
                        return render_template('index.html', msg='Incorrect username/password!', form=form)
                else:
                    # Extract the Salted-hash password from DB to local variable
                    hashAndSalt = account['password']
                    # Convert salted-hash password to bytes by using the .encode() method
                    # bycrypt.checkpw () will verify if the password input by user matches that from the database
                    if bcrypt.checkpw(password.encode(), hashAndSalt.encode()):
                        # Create session data, we can access this data in other routes
                        # Decrypt Email and Mobile Number
                        # Extract the Symmetric-key from Accounts DB
                        key = account['symmetrickey']
                        # Load the key
                        f = Fernet(key)
                        # Call f.decrypt() to decrypt the data. Convert data from Database to bytes/binary by using .encode()
                        decryptedEmail_Binary = f.decrypt(account['email'].encode())
                        decryptedMobile_Binary = f.decrypt(account['mobile'].encode())
                        # call .decode () to convert from Binary to String – to be displayed in Home.html.
                        decryptedEmail = decryptedEmail_Binary.decode()
                        decryptedMobile = decryptedMobile_Binary.decode()

                        session['loggedin'] = True
                        session['id'] = account['id']
                        session['username'] = account['username']
                        session['email'] = decryptedEmail
                        session['mobile'] = decryptedMobile

                        # redirect to ADMIN PAGE!!! NOTE THIS
                        return redirect(url_for('home'))
                    else:
                        # password incorrect
                        return render_template('index.html', msg='Incorrect username/password!', form=form)
            else:
                # Account doesn't exist or Username incorrect
                return render_template('index.html', msg='Incorrect username/password!', form=form)
        else:
            # Input Error
            return render_template('index.html', msg=form, form=form)
    # Get Request
    else:
        return render_template('index.html', msg=msg, form=form)


@app.route('/MyWebApp/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=300)
    except SignatureExpired:
        return '<h1>The token is expired Please register again!</h1>'
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))


@app.route('/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account,email=session['email'],mobile=session['mobile'])

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
