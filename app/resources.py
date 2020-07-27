import boto3
from flask import current_app

def get_client():
    if current_app.config['S3_KEY'] and current_app.config['S3_SECRET']:
        return boto3.client(
            's3',
            aws_access_key_id=current_app.config['S3_KEY'],
            aws_secret_access_key=current_app.config['S3_SECRET']
        )
    else:
        return boto3.client('s3')

def delete_obj(obj_file):
	s3 = boto3.resource("s3")
	obj = s3.Object(current_app.config['S3_BUCKET'], obj_file)
	obj.delete()


