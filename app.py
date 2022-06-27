from flask import Flask, render_template, request, url_for, session, redirect, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from flask import request
import pickle
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup
from html.parser import HTMLParser
    
import re 
import os as _os
import nltk
nltk.download('punkt')
from nltk import word_tokenize
import string 
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import LogisticRegression
app = Flask(__name__)
model=pickle.load(open('Voting.pkl','rb'))
tfidf=pickle.load(open('tfid.pkl','rb'))


app.secret_key = 'neha'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'happy'
mysql = MySQL(app)

def prep(review):
    
    # Remove HTML tags.
    review = BeautifulSoup(review,'html.parser').get_text()
    
    # remove punctuation
    review = re.sub("[^a-zA-Z]", " ", review)
    
    # upper case
    review = review.upper()
    

     # Tokenize to each word.
    token = nltk.word_tokenize(review)
    
    # Stemming
    review = [nltk.stem.SnowballStemmer('english').stem(w) for w in token]
    
    return " ".join(review)



 

@app.route('/')
  
@app.route('/first')
def first():
 	return render_template("first.html")

 
@app.route('/performance') 
def performance():
	return render_template('performance.html') 
  
@app.route('/loginad') 
def loginad():
	return render_template('loginad.html')
    
@app.route('/upload') 
def upload():
	return render_template('upload.html') 
@app.route('/preview',methods=["POST"])
def preview():
    if request.method == 'POST':
        dataset = request.files['datasetfile']
        df = pd.read_csv(dataset,encoding = 'unicode_escape')
        df.set_index('Id', inplace=True)
        return render_template("preview.html",df_view = df) 
@app.route('/login', methods = ['GET',"POST"])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM REGISTER WHERE username = %s AND password = %s', (username, password))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            global Id,Name
            session['Id'] = account['Id']
              
            Id = session['Id']
            session['username'] = account['username']
            Name=account['username']
            # Redirect to home page
            return redirect(url_for('profile'))
        else:
            # Account doesnt exist or username/password incorrect
            flash('Incorrect username/password! Please login with correct credentials')
            return redirect(url_for('login'))
    # Show the login form with message (if any)

    return render_template('login.html', msg=msg)

@app.route('/register',methods= ['GET',"POST"])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,10}$"
        pattern = re.compile(reg)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # Check if account exists using MySQL)
        cursor.execute('SELECT * FROM REGISTER WHERE Username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not re.search(pattern,password):
            msg = 'Password should contain atleast one number, one lower case character, one uppercase character,one special symbol and must be between 6 to 10 characters long'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into employee table
            cursor.execute('INSERT INTO REGISTER VALUES (NULL, %s, %s, %s)', (username, email, password))
            mysql.connection.commit()
            flash('You have successfully registered! Please proceed for login!')
            return redirect(url_for('login'))
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
        return msg
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)
  
@app.route('/index')
def index():
 	return render_template("index.html")

 

@app.route('/chart',methods=['POST','GET'])
def chart():
  
    if request.method == 'POST':    
        
        query_content=request.form['news_content']
        
       
        
        total= query_content
        #total = re.sub('<[^>]*>', '', total)
        #total = re.sub(r'[^\w\s]','', total)
        #total = total.lower()
        result = prep(total)
        data=[result]
        vect=tfidf.transform(data).toarray()
        prediction=model.predict(vect)
        pred=format(prediction[0])
   
        login()
        details = request.form
        
        news_content = details['news_content']
         
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO main(news_content,pred,userid) VALUES ( %s, %s,%s) ", (news_content,pred,Id))
         
        mysql.connection.commit()
        cur.close()
        return redirect('/user')
         
 
         
     
         
    return render_template('index.html')
@app.route('/profile')    
def profile():
    
     
         
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM register WHERE Id = %s', (Id,))
        account = cursor.fetchone()
       
        return render_template('profile.html', account=account)      
@app.route('/user')
def user():
     
    cur = mysql.connection.cursor()
    resultValue = cur.execute(" SELECT * from register INNER JOIN main ON register.ID = main.USERID ")
     
    if resultValue > 0:
        userDetails = cur.fetchall()
         
        return render_template('user.html',userDetails=userDetails)
        
@app.route('/admin')
def admin():
    cur = mysql.connection.cursor()
    resultValue = cur.execute(" SELECT * from register INNER JOIN main ON register.ID = main.USERID;")
     
    if resultValue > 0:
        userDetails = cur.fetchall()
         
        return render_template('admin.html',userDetails=userDetails)  
@app.route('/fake')
def fake():  
   cur = mysql.connection.cursor()      
   cur.execute("SELECT * from main WHERE pred ='Happy'")
   fakes=cur.fetchall()
    
       
   return render_template('fake.html',fakes=fakes) 
   
 
@app.route('/unhappy')
def unhappy():  
   cur = mysql.connection.cursor()      
   cur.execute("SELECT * from main WHERE pred ='Unhappy'")
   unhappys=cur.fetchall()
    
       
   return render_template('Unhappy.html',unhappys=unhappys) 
         
         
   
 
@app.route('/userdetail')
def userdetail():  
   cur = mysql.connection.cursor()      
   cur.execute("SELECT * from register")
   useradmin=cur.fetchall()
   print(useradmin)
       
   return render_template('userdetail.html',useradmin=useradmin) 
   
@app.route('/charts')
def charts():
    legend = "main by pred"
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("SELECT pred from main GROUP BY pred")
        # data = cursor.fetchone()
        rows1 = cursor.fetchall()
        labels = list()
        i = 0
        for row1 in rows1:
            labels.append(row1[i])
         

         
        cursor.execute("SELECT pred from main GROUP BY pred")
        # data = cursor.fetchone()
        rows2 = cursor.fetchall()
        
        label = list()
        j = 0
        values = list()
        k = 0
        for row2 in rows2:
            label.append(row2[j])
            cursor.execute("SELECT COUNT(id) from main WHERE  pred=%s", (row2[j],))
            rows3 = cursor.fetchall()
             
            #j=j+1
        # Convert query to objects of key-value pairs
            
            for row3 in rows3:
	              values.append(row3[k])
            #k=k+1
        mysql.connection.commit()
        cursor.close()
        
        
        
    except:
        print('Error: unable to fetch items')    

    return render_template('charts.html', values=values, labels = labels, legend=legend)   
     
if __name__ == '__main__':
    app.run()