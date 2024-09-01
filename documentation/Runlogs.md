Basic implemenation of the guessor, this is simply a route to guess the password and does no tracking of the user, or count of how many attempts.

2 routes, one to show the homepage, one to guess the route.

## Infra setup

Single worker bottle api with `bottle run`
Running on docker with port forwarding.

#### bottle server, single worker:

```bash
Success! The correct word is: azzz
The time took to guess the word was: 556.23 seconds
The requests per second was: 31.60
The average request time was: 0.37s

```

#### bottle server, gunicorn, 3 workers

```bash
Success! The correct word is: azzz
The time took to guess the word was: 52.23 seconds
The requests per second was: 336.49
The average request duration was: 0.03 seconds

```

#### bottle server, g, w1
```bash
Success! The correct word is: azzz
The time took to guess the word was: 56.13 seconds
The requests per second was: 313.03
The average request duration was: 0.03 seconds
The max requests per second was: 355.31
The min requests per second was: 3.27

```

same server with AIO guessor

```bash
Success! The correct word is: azzz
The time took to guess the word was: 8.66 seconds
----------------------------------------------------------------------------------------
The average request duration was: 0.22 seconds
The longest request duration was: 0.53 seconds
The shortest request duration was: 0.22 seconds
----------------------------------------------------------------------------------------
The requests per second was: 2033.60
The max requests per second was: 2033.60
The min requests per second was: 2.65
```

Then golang

```bash
Success! The correct word is: azzz
The time took to guess the word was: 4.48 seconds
The average request duration was: 0.10 seconds
The longest request duration was: 0.54 seconds
The shortest request duration was: 0.10 seconds
The requests per second was: 3933.32
The max requests per second was: 3933.54
The min requests per second was: 2.59
Found: azzz

```

