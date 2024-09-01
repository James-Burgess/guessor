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
- [*] Set up logging and metrics for the running server
- [ ] Set up a nice way to view all the results of different guessers and servers
- [*] Set up a way to blast the server with requests
- [ ] Add a basic user system
- [ ] Add a basic user system with a database


## License
WTFPL
