from flask import Flask, render_template_string
import subprocess
import datetime
import getpass
import pytz 

app = Flask(__name__)

@app.route('/htop')
def htop_endpoint():
    full_name = "Vishnu Prasad" 

    username = getpass.getuser()

    ist = pytz.timezone('Asia/Kolkata')
    now_ist = datetime.datetime.now(ist)
    server_time_ist = now_ist.strftime("%Y-%m-%d %H:%M:%S %Z%z")

    try:
        top_output = subprocess.check_output(['top', '-b', '-n', '1'], text=True)
    except subprocess.CalledProcessError as e:
        top_output = f"Error running top: {e}"

    template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>HTOP Endpoint</title>
        <style>
            body { font-family: monospace; white-space: pre-wrap; }
        </style>
    </head>
    <body>
        <h1>HTOP Information</h1>
        <p>Name: {{ name }}</p>
        <p>Username: {{ username }}</p>
        <p>Server Time (IST): {{ server_time }}</p>
        <h2>Top Output:</h2>
        <div>{{ top_output }}</div>
    </body>
    </html>
    """

    return render_template_string(template, name=full_name, username=username,
                                   server_time=server_time_ist, top_output=top_output)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 