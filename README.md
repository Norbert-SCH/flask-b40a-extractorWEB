# import flask here
from flask import Flask, render_template
#import os here
import os

# Create the Flask Object here
app = Flask(__name__)

# Define a basic route here
@app.route("/")
def home():
    return "Welcome to my Flask website!"

# Define another route with a dynamic URL here
@app.route("/hello/<name>")
def hello(name):
    return f"Hello, {name}!"

# Run the application
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Get the port from environment variable
    app.run(host="0.0.0.0", port=port, debug=True)
