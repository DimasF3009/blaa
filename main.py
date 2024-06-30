from flask import Flask, render_template,url_for, redirect

app = Flask(__name__)
app.config["SECRET_KEY"] = "iniSecretKeyKu"

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/artikel')
def artikel():
    return render_template('artikel.html')

@app.route('/redirect-about')
def redi_about():
    return redirect(url_for('about'))

@app.route('/redirect-index')
def redi_index():
    return redirect(url_for('index'))

@app.route('/redirect-contact')
def redi_contact():
    return redirect(url_for('contact'))

@app.route('/redirect-artikel')
def redi_artikel():
    return redirect(url_for('artikel'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
