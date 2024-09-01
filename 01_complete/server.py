import bottle

app = bottle.Bottle()
PASSWORD = 'azzz'

DATABASE = {}


@app.route('/')
def index() -> str:
    return f"Guess the password! <a href='/guess/<my_guess>'>Guess it at '/guess/<my_guess>'</a>"


@app.route('/register')
def register(username: str) -> str:
    print(f"User {username} registered")

    if username in DATABASE.keys():
        return f"User {username} already registered"

    DATABASE[username] = 0

    return username


@app.route('/guess/<guess>')
def guess(guess: str, username: str) -> bottle.HTTPResponse:
    if username not in DATABASE.keys():
        return bottle.HTTPResponse("User not registered", status=400)

    DATABASE[username] += 1
    success = guess == PASSWORD

    return bottle.HTTPResponse(
        f"""You guessed "{guess}" that's {'right' if success else 'wrong'}! ({DATABASE[username]} attempts)""",
        status=200 if success else 400
    )


if __name__ == '__main__':
    print(f"Starting server on port 8080")
    app.run(host='0.0.0.0', port=8080, debug=False, reloader=False)
