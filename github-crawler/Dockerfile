
FROM python:3.6

# Create app directory
WORKDIR /app

# Install app dependencies
COPY . ./

RUN pip install -r requirements.txt

EXPOSE 5000
CMD [ "python", "app.py" ]