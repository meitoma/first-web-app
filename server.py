from web_app_BBS.main import app,socketio

if __name__ == '__main__':
    socketio.run(app,debug=True,host="0.0.0.0",port=3000)
