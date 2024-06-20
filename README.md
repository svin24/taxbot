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

More detailed overview [here](EXPLANATION.md)!

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
