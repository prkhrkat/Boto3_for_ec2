from types import MethodType
from flask import Flask, render_template
import script as aws
from flask import request
app = Flask(__name__)
 
@app.route("/")
def home():
    return render_template('home.html')


@app.route("/get-status")
def get_status():
    instances = aws.get_running_instances()
    print(instances)
    return render_template('status.html', instances=instances)


@app.route("/get-status/<instance_id>")
def ssh_and_command(instance_id):
    if instance_id != 'i-00232f159d124b644':
        resp = aws.ssh_and_send_command(instance_id)
        print(resp)
        return "We did SSH successfully and run 'echo hello world'. Here is the response we get from bash: {}".format(resp)
    return "This instance carry application server, So it does not support SSH"
   
@app.route("/create-instance")
def launch_instance():
    return render_template('launch.html')


@app.route("/create-instance/<instance_type>")
def create_instance(instance_type):
    instance_id = aws.create_instance(instance_type)
    print(instance_id)
    return render_template('create.html', instance_id=instance_id)


@app.route("/public-ip")
def public_ip():
    username = request.args.get('instance_id')
    print('instance_id')
    response = aws.get_public_ip()
    print(response)
    return "{}".format(response)
    
 
 
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
