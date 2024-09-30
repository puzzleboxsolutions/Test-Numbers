from flask import Flask, request, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import datetime
import os

app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["500 per day", "20 per minute"],
    storage_uri=os.environ['STORAGE_URI'],
    storage_options={"socket_connect_timeout": 30},
    strategy="fixed-window"
)
SECRET_PASSKEY=int(os.environ['SECRET_PASSKEY'])

@app.route('/', methods=['GET'])
def home_get():
    return render_template('index.html')

@app.route('/', methods=['POST'])
@limiter.limit("5 per minute")
def home_post():  
    print(request)
    print(request.form)

    now = datetime.datetime.now()
    if now.minute % 2 != 0:
        message="Hmm let me think!"
        return render_template('index.html', message=message)

    try:
        passkey = int(request.form.get('passkey'))
        if passkey == SECRET_PASSKEY:
            message = "congratulations!! passkey is 7"
        elif passkey < SECRET_PASSKEY:
            message = "passkey is bigger than " + str(passkey)
        elif passkey > SECRET_PASSKEY:
            message = "passkey is less than " + str(passkey)
    except ValueError:
        message = "That's not a number!"
    return render_template('index.html', message=message)


if __name__ == '__main__':
    limiter = Limiter(get_remote_address, app=app)
