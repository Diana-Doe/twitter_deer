from flask import Flask, request,render_template
import twitter
app = Flask(__name__)


@app.route('/')
def my_form():
    return render_template('my-form.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    m = twitter.find_loc(processed_text)
    return m._repr_html_()



if __name__ == '__main__':
    app.run(debug=True)
