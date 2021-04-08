from flask import Flask, render_template, request
import os
from flask_cors import CORS, cross_origin
import pusher
from flask_mysqldb import MySQL

app =Flask(__name__)

port = int(os.environ.get('PORT', 5000))

#configure db
app.config['MYSQL_HOST'] = 'us-cdbr-east-03.cleardb.com'
app.config['MYSQL_USER'] = 'b5e21d77835cb7'
app.config['MYSQL_PASSWORD'] = 'fe68c78a'
app.config['MYSQL_DB'] = 'heroku_user'

mysql = MySQL(app)

pusher_client = pusher.Pusher(
  app_id='1184922',
  key='172519f8f1cb46b08df5',
  secret='2097baf12c51e484c5a3',
  cluster='us2',
  ssl=True
)

@app.route("/")
def index():
    
    return render_template('index.html')

@app.route("/enviar", methods=['POST'])
def enviar():
  if request.method == 'POST':
    try:
      inforform = request.form
      nome_user = inforform['nome']    
      email_user = inforform['email']    
      senha_user = inforform['senha']    

      cur = mysql.connection.cursor()
      cur.execute("INSERT INTO heroku_3aabea2c4385c93.tbl_users(nome_user,email_user,senha_user) VALUES(%s,%s,%s)", (nome_user,email_user,senha_user))
      mysql.connection.commit()
      cur.close()
      return 'succes'
    except Exception as e:
      print(e)
      return 'error'

@app.route("/message", methods=['POST'])
def message():
  try:
    username = request.form.get('username')
    message = request.form.get('message')
    print(username)
    print(message)
    pusher_client.trigger('chat-channel', 'new-message', {'username' : username, 'message': message})
  except Exception as e:
    print(e)
  return 'ok'

if __name__ == '__main__':
    app.run(debug=True, port=port)