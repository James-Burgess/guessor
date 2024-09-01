# Guessor
Guess the 4 letter word at [jbx.co.za](https://jbx.co.za)

## Server
There are two versions of the server:

#### Basic [basic-no-user]
The basic version of the server which does not track reuquests or users.

#### (INPROGRESS) Basic with user [basic-user]
The basic with user version of the server which tracks user requests.


### To run the server:

```bash
docker run --rm -it -p 8080:8080 jimmyburgess/guessor:[server-name]
```

To build and deploy locally:
```bash
git clone https://github.com/james-burgess/guessor.git
cd guessor
docker run --rm -it -p 8080:8080 $(docker build -q ./00_basic_no_user)
```


## Running the guessors
To run the python guessors:

```bash
git clone https://github.com/james-burgess/guessor.git
cd guessor/guessors
pip install -r requirements.txt
```

```bash
python guessors/brute_aio.py
```


## TODO
- [x] Set up logging and metrics for the running server
- [ ] Set up a nice way to view all the results of different guessers and servers
  - [x] setup basic plotly dash
  - [ ] update the dash to show everything at once
  - [ ] update the dash to show the results of different guess/server runs
  - [ ] add the results of a guess run to the results page (single run, 5 parallel and 50 parallel)
- [x] Set up a way to blast the server with requests
- [ ] Add a basic user system
- [ ] Add a basic user system with a database
- [ ] Implement fast api version of the server
- [ ] Implement an async version of the server
- [ ] Implement an queuing version of the server
- [ ] Implment a golang version of the server
- [ ] Implement a elixir version of the server
- [ ] Live server stats page
- [ ] LOIC test
- [ ] writeup

## License
WTFPL
