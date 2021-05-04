# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Luis Enrique Fuentes Plata

import json, requests, os, logging
from pathlib import Path
from src.GenericFunctions import get_path, get_client
from src.TransformationClasses import FileFactory

logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s: %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """This function handles what to do when an event PUT/POST happends in a bucket. 
    
    Parameters
    ----------
    event: dict, required
        API S3 Lambda Proxy Input Format

    context: object, required
        API Gateway Lambda Proxy Input Format

    """
    try:
        logger.info('### 1. Getting the event ###')

        bucket_name = event['Records'][0]['s3']['bucket']['name']
        object_name = event['Records'][0]['s3']['object']['key']
        file_name = os.path.basename(object_name)
        file_path = os.path.dirname(object_name)
        logger.info(f'### 1.1. bucket: {bucket_name} object: {object_name}:')

        logger.info('### 2. Creating file Path ###')
        path = get_path(file_name=file_name)

        logger.info('### 3. Creating file Path ###')
        s3_client = get_client()

        logger.info('### 4. Downloading file ###')
        with path.open('wb+') as file:
            s3_client.download_fileobj(bucket_name, object_name, file)

        logger.info('### 5. Reading ###')

        file_obj = FileFactory(path).creates()

        print(file_obj.df.head(5))

        logger.info('###6. Returning response###')
        return {
            "statusCode" : 200,
            "body" : json.dumps(
                {"message" : "path"}
            )
        }

    except Exception as e:
        logger.exception(e)
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}
