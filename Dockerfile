FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY ./tax_assistant.py /app/
COPY ./templates/ /app/
COPY ./templates/index.html /app/templates/

EXPOSE 5000
CMD ["python", "tax_assistant.py"]
