import bottle
# from bottle import

app = bottle.Bottle()
PASSWORD = 'azzz'


@app.route('/')
def index() -> str:
    return f"Guess the password! <a href='/guess/<my_guess>'>Guess it at '/guess/<my_guess>'</a>"


@app.route('/guess/<guess>')
def guess(guess: str) -> bottle.BaseResponse:
    success = guess == PASSWORD
    return bottle.HTTPResponse(
        f"""You guessed "{guess}" that's {'right' if success else 'wrong'}!""",
        status=200 if success else 400
    )


if __name__ == '__main__':
    print(f"Starting server on port 8080")
    app.run(host='0.0.0.0', port=8080, debug=False, reloader=False)
