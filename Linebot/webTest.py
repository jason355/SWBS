from flask import Flask, request, render_template

app = Flask(__name__, template_folder='templates')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        print(user_input)

    return render_template('index.html')


if __name__ == '__main__':
    app.run()
