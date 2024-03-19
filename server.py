from bbs_app.main import bbs_app
from diary_app.main import diary_app
from __init__ import app,socketio

app.register_blueprint(bbs_app, url_prefix='/bbs_app')
app.register_blueprint(diary_app, url_prefix='/diary_app')
if __name__ == '__main__':
    socketio.run(app,debug=True,host="0.0.0.0",port=3000)
