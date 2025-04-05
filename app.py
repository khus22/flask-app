import os
import logging
import urllib.parse
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask app
app = Flask(__name__)


# Database credentials
DB_USER = 'flaskwebuser'
DB_PASSWORD = 'Pandaa2218!'
DB_HOST = '172.31.1.156'  # Private IP of your database-hosting EC2 instance
DB_NAME = 'flaskweb'

# URL-encode the password to handle special characters
encoded_password = urllib.parse.quote_plus(DB_PASSWORD)
# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{encoded_password}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# -------------------- LOGGING CONFIG --------------------
log_dir = '/home/ec2-user/flask-app/logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'{log_dir}/app.log'),
        logging.StreamHandler()
    ]
)

# -------------------- MODEL --------------------
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

# -------------------- ROUTES --------------------

# Home route - Display tasks and create new ones
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        content = request.form['content']
        new_task = Task(content=content)
        try:
            db.session.add(new_task)
            db.session.commit()
            app.logger.info(f"Task added: {content}")
            return redirect('/')
        except Exception as e:
            app.logger.error(f"Error adding task: {e}")
            return f"An error occurred: {e}"
    else:
        tasks = Task.query.all()
        app.logger.info("Fetched all tasks")
        return render_template('index.html', tasks=tasks)

# Edit route - Edit an existing task
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    task = Task.query.get_or_404(id)
    
    if request.method == 'POST':
        task.content = request.form['content']
        db.session.commit()
        app.logger.info(f'Updated task: {task.content}')
        return redirect('/')
    
    return render_template('edit.html', task=task)

# Delete route - Delete a task
@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    app.logger.info(f'Deleted task: {task.content}')
    return redirect('/')
# ----------------------------Testing DB -------------#
# Test DB Connection route
@app.route('/test-db')
def test_db():
    try:
        db.session.execute('SELECT 1')
        return "✅ Database connected successfully!"
    except Exception as e:
        return f"❌ Database connection failed: {e}"
# -------------------- MAIN ------------------
# -------------------- MAIN --------------------
if __name__ == "__main__":
    # Test the logging configuration
    app.logger.info('This is a test log message.')

    app.run(host='0.0.0.0', port=8001)

