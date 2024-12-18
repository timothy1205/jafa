# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.13-alpine

#Install all dependencies.
RUN apk add --no-cache net-tools 

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Gunicorn port
EXPOSE 8080

RUN mkdir /opt/jafa/backend -p
WORKDIR /opt/jafa

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt --no-cache-dir

COPY . ./backend

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--worker-class", "gevent", "backend.app:create_app()"]
