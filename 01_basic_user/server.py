import bottle
from bottle import template
from bottle import static_file


PASSWORD = 'azzz'
DATABASE = {}

app = bottle.Bottle()


@app.route('/static/<filename:path>', name='static')
def serve_static(filename):
    return static_file(filename, root='./static')


@app.route('/')
def index() -> str:
    return template('./templates/index.html', username=bottle.request.get_cookie('username'))


@app.route('/register', method='POST')
def register() -> str:
    username = bottle.request.forms.get('username')
    print(f"User {username} registered")

    if username in DATABASE.keys():
        return f"User {username} already registered"

    DATABASE[username] = 0

    return username


@app.route('/guess/<guess>')
def guess(guess: str) -> bottle.HTTPResponse:
    username = bottle.request.get_cookie('username')
    if username not in DATABASE.keys():
        return bottle.HTTPResponse("User not registered", status=400)

    DATABASE[username] += 1
    success = guess == PASSWORD

    return bottle.HTTPResponse(
        {"attempts": DATABASE[username], "success": success},
        status=200 if success else 400
    )


if __name__ == '__main__':
    print(f"Starting server on port 8080")
    app.run(host='0.0.0.0', port=8080, debug=True, reloader=True)
