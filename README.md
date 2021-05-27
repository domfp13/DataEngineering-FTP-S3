# FTP Event Driven

This project contains source code and supporting files for a serverless application. It includes the following files and folders.

- transformation - Code for the application's Lambda function.
- events - Invocation events that you can use to invoke the function locally.
- tests - Unit tests for the application code, this is to run locally. 
- template.yaml - A template that defines the application's AWS resources.

The application uses several AWS resources, including Lambda Function, S3 bucket, CloudWatch logs, IAM policies, etc. These resources are defined in the `template.yaml` file in this project. You can update the template to add AWS resources through the same deployment process that updates your application code. The code is package in a container that extends the official AWS python 3.7 image.

### Architecture Diagram
![Screenshot 2021-05-27 at 10 43 39](https://user-images.githubusercontent.com/7782876/119795152-7f20c700-bed8-11eb-8320-17c170a731d6.png)

### Class Diagram
![Screenshot 2021-05-27 at 10 45 19](https://user-images.githubusercontent.com/7782876/119795364-b000fc00-bed8-11eb-935b-002120a38514.png)

## Use the SAM CLI to build and test locally

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. It uses Docker container to run your functions in an Amazon Linux environment that matches Lambda locally. It can also emulate your application's build environment and API.

To use the SAM CLI, you need the following tools.

* AWS CLI - [Install the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

You may need the following for local testing.
* [Python 3 installed](https://www.python.org/downloads/)

Build your application with the `sam build` command.

```bash
ftp_event_driven$ sam build
```

The SAM CLI builds a docker image from AWS and then installs dependencies defined in `transformation/requirements.txt` inside the docker image. The processed template file is saved in the `.aws-sam/build` directory, for simplicity .gitignore is excluding this directory but it will be generated at build time.

Test a single function by invoking it directly with a test event. An event is a JSON document that represents the input that the function receives from the event source. Test events are included in the `events` folder in this project.

Run functions locally and invoke them with the `sam local invoke` command.

```bash
ftp_event_driven$ sam local invoke ProcessingFunction --event events/event.json
```

The SAM CLI can also emulate your application's events.
This repository also includes a Makefile so this complexity gets solve just by running make commands to target *make recipes*.
```bash
ftp_event_driven$ make help
```

## Deploy the application
CloudFormation will need a few variables in order to create the resources, the first thing you will need is an Elastic Cloud Repository, this will be used to host the container image, to create an ECR repository run the following command, and copy the URI (IMAGE-REPOSITORY) that its generated.
```bash
aws ecr create-repository \
    --repository-name <your_repo_name> \
    --image-tag-mutability IMMUTABLE \
    --image-scanning-configuration scanOnPush=true
```
The ECR gives you a place to upload the application image so that [AWS CloudFormation](https://aws.amazon.com/cloudformation/) can access the container image when it runs the deploy process.

CloudFormation will need 4 variables, you will need to fill out these variables under *.env* directory within this repository, variables are the following: 
* STACK-NAME=<name_of_your_stack>
* REGION=<aws_region>
* IMAGE-REPOSITORY=<your_ecr_uri>
* BUCKETNAME=<globally_unique_bucket_name>
* TOPICNAME=<name_of_sns_topic_that_will_be_created>
* ENDPOINTEMAIL=<email_address_for_error_notification>

Once you fill out these variables, the next step is to build your application

To build and deploy your application, the first thing is to build the application, run the following in your shell:

```bash
ftp_event_driven$ sam build
```
This command will compile and build `template.yaml` file in `.aws-sam/build/` directory. 

To package the application run:

```bash
make package
```
Finally to deploy the package run:
```bash
make deploy
```

## Add a resource to your application
The application template uses AWS Serverless Application Model (AWS SAM) to define application resources. AWS SAM is an extension of AWS CloudFormation with a simpler syntax for configuring common serverless application resources such as functions, triggers, and APIs. For resources not included in [the SAM specification](https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md), you can use standard [AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html) resource types.

## Fetch, tail, and filter Lambda function logs

To simplify troubleshooting, SAM CLI has a command called `sam logs`. `sam logs` lets you fetch logs generated by your deployed Lambda function from the command line. In addition to printing the logs on the terminal, this command has several nifty features to help you quickly find the bug.

`NOTE`: This command works for all AWS Lambda functions; not just the ones you deploy using SAM.

```bash
ftp_event_driven$ sam logs -n ProcessingFunction --stack-name <stack_name>
```

You can find more information and examples about filtering Lambda function logs in the [SAM CLI Documentation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-logging.html).

## Unit tests

Tests are defined in the `tests` folder in this project. Use PIP to install the [pytest](https://docs.pytest.org/en/latest/) and run unit tests from your local machine.

```bash
ftp_event_driven$ pip install pytest pytest-mock --user
ftp_event_driven$ python -m pytest tests/ -v
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name <stack_name>
```

## Authors
* **Luis Enrique Fuentes Plata** - *2021-05-04*
