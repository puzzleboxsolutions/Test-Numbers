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
SECRET_EASTEREGG1=os.environ['SECRET_EASTEREGG1']
SECRET_EASTEREGG2=os.environ['SECRET_EASTEREGG2']
SECRET_EASTEREGG3=os.environ['SECRET_EASTEREGG3']


@app.route('/', methods=['GET'])
def home_get():
    return render_template('index.html')

@app.route('/', methods=['POST'])
@limiter.limit("1 per minute")
def home_post():  
    print(request.form)

    try:
        passkey = int(request.form.get('gusse'))
        if passkey == SECRET_PASSKEY:
            message = "Congratulations!! this is the number I am thinking."
        elif passkey < SECRET_PASSKEY:
            message = "My number is bigger than this."
        elif passkey > SECRET_PASSKEY:
            message = "My number is lower than this."
    except ValueError:
        message = "That's not a number!"
    except Exception as e:
        message = "Something went wrong try again."
    return render_template('index.html', message=message)






@app.route('/easter', methods=['GET'])
def easter_get():
    return render_template('easter.html')

@app.route('/easter', methods=['POST'])
@limiter.limit("3 per minute")
def easter_post():  
    print(request.form)
    success_message = "Congratulations!! submit the key to https://forms.gle/mT7vjPFx5su8CVx28"    
    try:
        easterkey = request.form.get('easter-gusse')
        if easterkey == SECRET_EASTEREGG1:
            message = success_message
        elif easterkey == SECRET_EASTEREGG2:
            message = success_message
        elif easterkey == SECRET_EASTEREGG3:
            message = success_message
        else:
            message = "This is not right!"
    except Exception as e:
        message = "Something went wrong try again."
    return render_template('easter.html', message=message)


@app.errorhandler(429)
def ratelimit_handler(e):
    return render_template('429.html'), 429

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    limiter = Limiter(get_remote_address, app=app)
