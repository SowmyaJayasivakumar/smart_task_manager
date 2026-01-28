from flask import Flask, render_template, request, redirect, url_for,session
import pymysql

app = Flask(__name__)
app.secret_key = "super_secret_key_sowmyaviji_123"

#Database connection function
def get_connection():
    return pymysql.connect(
        host = 'localhost',
        user = 'smart_task',
        password = 'task123',
        database = 'smart_task_manager'
    )

#-----------------------Task Routes______________________________________#
#Home route -> Shows all tasks
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect('/login')
    conn = get_connection()
    cursor = conn.cursor()
    user_id = session.get('user_id')
    username = session.get('username')
    cursor.execute("SELECT * FROM TASKS WHERE user_id = %s",(user_id,))
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html',tasks = tasks,username = username)

#Add new task
@app.route('/add',methods =['POST'])
def add_task():
    title = request.form['title']
    description = request.form['description']
    status = "Pending"
    conn = get_connection()
    user_id = session['user_id']
    cursor = conn.cursor()
    cursor.execute("INSERT INTO TASKS (title,description,status,user_id) VALUES (%s,%s,%s,%s)",(title,description,status,user_id))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/')

#Update Task -> Mark as completed
@app.route('/update/<int:task_id>')
def update_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE TASKS SET STATUS='Completed' WHERE id=%s",(task_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/')

#Delete Task
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM TASKS WHERE id = %s",(task_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

#-------------------------USER ROUTES------------------------------------#

@app.route('/signup',methods = ['GET','POST'])
def signup():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO USERS (username,password) VALUES (%s,%s)",(username,password))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM USERS WHERE username=%s AND password =%s',(username,password))

        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('index'))
        else:
            return "Invalid Credentials, Try Again!"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))        

#---------------------------Run Flask Server-----------------------------#
if __name__=='__main__':
    app.run(debug = True)