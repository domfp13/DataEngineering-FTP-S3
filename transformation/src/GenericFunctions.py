# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Luis Enrique Fuentes Plata

import boto3
from pathlib import Path

def get_client():
    """This function returns a boto3.client, for local testing activate the decorator adding your AWS credentials

    Returns:
        [boto3.client]: boto3.client object.
    """
    return boto3.client('s3')

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
