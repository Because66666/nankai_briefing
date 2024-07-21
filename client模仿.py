from flask import Flask,jsonify,request,json

app = Flask(__name__)





# "http://127.0.0.1:5700/send_group_msg?group_id="  +str(group_num)+
#                  "&message=" + data)

@app.route('/send_group_msg',methods=['GET'])
def write():
    return '<h1>OK<h1>'

if __name__=='__main__':
    app.run('127.0.0.1',port=5700,debug=True)