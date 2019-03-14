from flask import Flask, render_template, request


class ima_rest:
    app = Flask(__name__, template_folder="templates")

    @app.route('/send', methods=["POST"])
    def send_config():
        agentIP = request.json
        return agentIP

    @app.route('/')
    def home():
        return render_template('home.html')

    if __name__ == '__main__':
        app.run(debug=True)


