# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Luis Enrique Fuentes Plata

import boto3
from pathlib import Path
from os import environ

def get_s3_client():
    """This function returns a boto3.client for s3.

    Returns:
        [boto3.client]: boto3.client object.
    """
    return boto3.client('s3')

def get_sns_client(region_name:str='us-east-1'):
    """This function returns a boto3.client for sns.

    Returns:
    [boto3.client]: boto3.client object.
    """
    return boto3.client('sns', region_name=region_name)

def decorator_get_path(function):
    """Returns a pathlib.Path object, since this is being run in a container the Path is using the /tmp directory,
    when decorator is activated, please specified the path of the object in the Path down below.

    Args:
        file_name (str): The file name that will be used to generate the Path

    Returns:
        Path: [description]
    """
    def wrapper(file_name:str):
        return Path('', file_name)
    return wrapper
#@decorator_get_path
def get_path(file_name:str) -> Path:
    """Returns a pathlib.Path object, since this is being run in a container the Path is using the /tmp directory.

    Args:
        file_name (str): The file name that will be used to generate the Path

    Returns:
        Path: [description]
    """
    return Path(f'/tmp/{file_name}')

def get_sns_topic_arn() -> str:
    """Getting the SNS Topic ARN, if running locally, you must activate the decorator and add the arn
        that is generated after the service has been deployed through cloudformation.

    Returns:
        str: SNS arn
    """

    sns_topic_arn:str = environ.get('SNS_TOPIC_ARN')

    if sns_topic_arn:
        return sns_topic_arn
    else:
        return 'arn:aws:sns:<REGION>:<NAME>'
