from flask import Flask, render_template, request, jsonify
import os
from main import run
from threading import Thread
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

# Path to the file where emails will be stored
EMAIL_FILE_PATH = 'TEXT/emails.txt'

def email_exists(email):
    """Check if the email already exists in the file."""
    try:
        with open(EMAIL_FILE_PATH, 'r') as file:
            for line in file:
                if line.strip() == email:
                    return True
    except FileNotFoundError:
        # If the file does not exist, return False
        return False
    return False

@app.route('/')
@app.route('/home')
@app.route('/newsletter')
def index():
    return render_template('main.html')


@app.route('/latest')
def latest():
    return render_template('latest.html')


@app.route('/blog')
@app.route('/blogs')
def blog():
    # Specify the folder path
    folder_path = 'templates/blogs'

    # Get a list of all files in the 'templates/blogs' folder
    blog_posts = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    print(blog_posts)
    # Pass the blog_posts list to the template
    return render_template('blog.html', blog_posts=blog_posts)


@app.route('/blog/<filename>')
def render_blog(filename):
    print(filename)
    return render_template(f'blogs/{filename}')



@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form['email']
    if email:
        if email_exists(email):
            return jsonify({'message': 'This email is already subscribed.'}), 400
        with open(EMAIL_FILE_PATH, 'a') as file:
            file.write(email + '\n')
        return jsonify({'message': 'Thank you for subscribing!'})
    return jsonify({'message': 'Failed to subscribe. Please try again.'}), 400




@app.route('/secret', methods=['GET', 'POST'])
def secret_trigger():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        valid_username = "test"
        valid_password = "test"
        
        if username == valid_username and password == valid_password:
            # Send initial response
            response = jsonify({'message': 'Newsletter Process Initiated'})
            response.status_code = 200
            # Start the run function in a separate thread
            Thread(target=run).start()
            return response
        else:
            return jsonify({'message': 'failure'}), 401

    # For GET requests, just render the template
    return render_template("secrethashreading.html")

    
    


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



if __name__ == '__main__':
    # Initialize the scheduler only once
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=run, trigger='cron',day_of_week='wed', hour=16, minute=34)
    scheduler.start()
    
    try:
        app.run(host='0.0.0.0', port=80, debug=False)
    finally:
        # Ensure the scheduler shuts down gracefully
        scheduler.shutdown()
