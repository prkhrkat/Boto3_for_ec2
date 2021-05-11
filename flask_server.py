from flask import Flask, render_template
import script as aws
app = Flask(__name__)
 
@app.route("/")
def home():
    status = aws.get_running_instances()
    print(status)
    return "Here is the list of running instances {}".format(status)
 
@app.route("/create_instance")
def learn():
    aws.create_key_pair()
    response = aws.create_instance()
    print(response)
    return "{}".format(response)
 
 
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)