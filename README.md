# Snaplost
A Lost and Found web application

## Installation Guide
(Make sure that you have Python and pip installed)
### Prerequisites
```
pip install flask
git clone https://github.com/sq125/snaplost.git 
cd snaplost
source venv3/bin/activate # To activate virtual environment
pip install -r requirements.txt
```
### Set the Environment Variables
```
# Use ‘set’ instead of ‘export’ if you are using Windows Command Prompt
export FLASK_APP=snaplost:app 
export FLASK_ENV=development 
export ELASTICSEARCH_URL=http://localhost:9200
export SECRET_KEY= <YOUR_SECRET_KEY>
export MAIL_PASSWORD= <YOUR_EMAIL_PASSWORD>
# Ensure that your google account allows less secure apps.
export MAIL_USERNAME= <YOUR_EMAIL_ADDRESS> 
export S3_BUCKET_NAME= <YOUR_BUCKET_NAME>
export AWS_ACCESS_KEY_ID= <S3_ACCESS_KEY>
export AWS_SECRET_ACCESS_KEY= <S3_SECRET_ACCESS_KEY> 
```

### Run the application in command line
```
# To begin the service for the search bar
sudo service elasticsearch start 
flask run
```


