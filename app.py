from flask import Flask, render_template, request, url_for, redirect
from gevent.wsgi import WSGIServer
app = Flask(__name__)
import denon
ip = '192.168.1.102'
@app.route('/', methods=['GET','POST'])
def index():
    data = denon.get(ip)
    if request.method == 'GET':
        return render_template('index.html', vol = data['VOL'], power = data['POWER'], inp = data['INPUT'])
        
    response = request.form.to_dict()
    print(response)
    for item in response.keys():
        denon.send(ip, item, response[item])
    return redirect(url_for('index'))
    
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
    #WSGIServer(('', 5000), app).serve_forever()
