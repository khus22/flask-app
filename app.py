from flask import Flask, render_template

app = Flask(__name__)

# Define the route for the home page
@app.route('/')
def home():
    return render_template('index.html')  # This will render the index.html page

if __name__ == "__main__":
    app.run(debug=True)
