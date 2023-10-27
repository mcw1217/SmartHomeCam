from flask import render_template, request, redirect, url_for, session, Flask, request, Response, stream_with_context
import re
from app001 import app
from app001.models import User
import numpy as np
import csv
from app001.streamer import Streamer
from threading import Thread

app.secret_key = "your secret key"
streamer = Streamer()

thread = Thread(target=streamer.run) # 백엔드에서 process 함수를 무한으로 돌려 영상의 프레임을 model에서 prediction 한다.
thread.daemon = True
thread.start()


@app.route("/login/", methods=["GET", "POST"])
def login():
    msg = ""
    # username과 password에 입력값이 있을 경우
    if (
        request.method == "POST"
        and "username" in request.form
        and "password" in request.form
    ):
        # 쉬운 checking을 위해 변수에 값 넣기
        username = request.form["username"]
        password = request.form["password"]
        # MySQL DB에 해당 계정 정보가 있는지 확인
        account, check_password = User.login_check(username, password)
        if check_password:
            session["loggedin"] = True
            session["id"] = account["id"]
            session["username"] = account["username"]
            session["role"] = account["role"]
            fromip = request.environ.get("HTTP_X_REAL_IP", request.remote_addr)
            User.update_fromip(fromip, account["id"])
            return redirect(url_for("home"))
        else:
            msg = "Incorrect username/password!"
    if "loggedin" in session:
        return redirect(url_for("home"))
    return render_template("login.html", msg=msg)


@app.route("/home")
def home():
    if "loggedin" in session:
        if session["role"] == "관리자":
            return render_template(
                "admin_home.html", username=session["username"], id=session["id"]
            )
        else:
            return render_template(
                "home.html", username=session["username"], session=session
            )
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("loggedin", None)
    session.pop("id", None)
    session.pop("username", None)
    return redirect(url_for("login"))


@app.route("/profile")
def profile():
    if "loggedin" in session:
        account = User.get_information([session["id"]])
        if session["role"] == "관리자":
            return render_template("admin_profile.html", account=account)
        else:
            return render_template("profile.html", account=account)
    return redirect(url_for("login"))

@app.route('/stream', methods=["GET","POST"])
def stream():
    if "loggedin" in session:            
        src = request.args.get( 'src', default = 0, type = int )
        
        try :
            
            return Response(
                                    stream_with_context( stream_gen( src ) ),
                                    mimetype='multipart/x-mixed-replace; boundary=frame' )
            
        except Exception as e :
            
            print('[wandlab] ', 'stream error : ',str(e))
    return redirect(url_for("login"))

def stream_gen( src ):   
  
    try : 
        while True :
            frame = streamer.bytescode()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                    
    except GeneratorExit :
        print( 'disconnected stream' )
        
