# Taxbot

An AI chatbot that will help you with taxes!

## Project structure

```  
EXPLANATION.md # additional explanation
README.md
api_key # place your api_key here
instance/taxbot_data.db 
requirements.txt
tax_assistant.py # main program
templates/index.html  # HTML for the project
```

More detailed overview [here](Presentation.pdf)!

### Setup

Requires `Python 3.12`,`pip`.

```bash
python -m venv venv 
source venv/bin/activate 
pip install -r requirements.txt
python tax_assignment.py 
```

### Docker(alternative)
```
docker build -t taxbot .
docker run -p 5000:5000 -e OPENAI_API_KEY=XXXXXXXXX taxbot # if you do not have api-key as a file  
docker run -p 5000:5000 taxbot
```
Alternatively you can also pull the image `docker pull ghcr.io/svin24/taxbot:latest`

### Podman(even better)
```
podman build -t taxbot .
podman run -p 5000:5000 -e OPENAI_API_KEY=XXXXXXXXX localhost/taxbot:latest # if you do not have api-key as a file 
podman run -p 5000:5000 localhost/taxbot:latest
```
Alternatively you can also pull the image `podman pull ghcr.io/svin24/taxbot:latest`
### API key is missing! (DOCKER/PODMAN) 

either your api key needs to be put in the file `api-key` or you need to set your `OPENAI_API_KEY` environment variable

### Access the application

Open up your browser at `http://127.0.0.1:5000/` to view the application

More info about that part of the program can be found on its dedicated README

### REST api examples  

GET entire conversation log:
```
curl -X GET http://localhost:5000/log
```
GET database data from id:
```
curl -X GET http://localhost:5000/data/IDNUMBER
```
DELETE database data from id:
```
curl -X DELETE http://localhost:5000/data/IDNUMBER  
```
POST to submit data:  
```  
curl -X POST http://localhost:5000/submit -d "income=50000&expenses=10000&prompt=Help me with my taxes"
```

# Application explanation

`tax_assistant.py` - Includes the main application logic, implements REST, and uses openAI
`templates\index.html` - Webpage template, includes basic CSS and Javascript that uses the REST API

## Flask/SQLalchemy

Application uses Flask as the web framework and Flask-SQLalchemy for handling the database.
The backend is SQLite and this is the database model:

```
id [int] - primary key
income [float] - nullable
expenses [float] - nullable
prompt [str] - not nullable
ai_resp [str] - not nullable
```

Possibility of not getting a response from the AI exists resulting in ai_resp being NoneType, probably should initialize it as an empty string?

## REST
It also uses Flask to implement the REST API: the functions implemented can be found above in the **REST api examples** section.
The functions in program are:

`submit()` - submits data to database (used by JS)

`log()` - Gets all data from database (used by JS)

`get_data()` - Gets data using an ID number

`delete_data()` - Deletes data using an ID number

It is not secure at all but it functions: I do have some ideas on how to improve it on further iterations.

## OpenAI

Reads either the key from an `api_key` file in the project directory or reads the `OPENIAI_API_KEY` environment variable
Environment variable is prioritized.

AI programming is done in the `get_ai_response(prompt, past_interactions)` function.
The bot is programmed using json formatted `messages`, using "roles".

A short explanation of the "roles" as I understand them:

`system` - Defines conversation topic

`user` - The user input

`assistant` - The responses to user inputs.

Right now the process is very inefficient because it reads the entire database log, it is really not scalable. 
But honestly matters little for such a small scale assignment.
**I do have some ideas for improving this however.**
