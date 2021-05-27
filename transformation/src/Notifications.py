# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Luis Enrique Fuentes Plata

import logging
from src.GenericFunctions import get_sns_topic_arn

logger = logging.getLogger(__name__)

class SnsWrapper:
    """Encapsulates Amazon SNS topic and subscription functions."""
    def __init__(self, sns_client):
        """
            :param sns_resource: A Boto3 Amazon SNS resource.
        """
        self.sns_client = sns_client
        self.sns_topic_arn:str = get_sns_topic_arn()
    
    def send_email(self, object_name:str, e:str) -> str:
        """Sends an email to the sns endpoint subscribers for this topic:

        Returns:
            str: The ID of the message.
        """
        try:
            message:str = f"The following file: {object_name} had the following error: {e}"
            subject:str = f"Error Lambda Function: {object_name}"
            response = self.sns_client.publish(
                TargetArn=self.sns_topic_arn,
                Message=message,
                Subject=subject
            )
            message_id = response['MessageId']
            logger.info("Published message")
        except Exception as e:
            logger.exception("Couldn't publish message to topic %s.", self.sns_topic_arn)
            raise
        else:
            return message_id
