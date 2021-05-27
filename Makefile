SHELL = /bin/bash

include .env

.PHONY: setup
setup: ## (Local Testing): It will rebuild the container and remove orphan containers
	@ echo "1.- Rebuilding Docker Image"
	sam build
	@ echo "2.- Prune build images"
	docker container prune --force
	@ echo "3.- Removing Middle step images"
	docker image prune --force

.PHONY: cleanup
cleanup: ## (Local Testing): Removes old image versions
	@ echo "1.- Removing old images"
	docker rmi --force $(docker images -q 'processingfunction' | uniq)

.PHONY: invoke
invoke: ## (Local Testing): invoke local event
	sam local invoke ProcessingFunction --event events/event.json

.PHONY: run
run: ## (Local Testing): Run app.lambda_handler
	@ $(MAKE) setup invoke

.PHONY: buildcontainer
buildcontainer: ## (Local Testing): Build container image
	@ echo "********** Building image **********"
	docker image build --rm -t python-runner .
	@ echo "********** Cleaning old version **********"
	docker image prune -f

.PHONY: buildcompose
buildcompose: ## (Local Testing): Docker-Compose up
	@ echo "spinning up containers"
	docker-compose up -d

.PHONY: package
package: ## (Cloud): Package code
	@ sam build
	@ sam package --output-template-file packaged-template.yaml \
		--region ${REGION} \
		--image-repository ${IMAGE-REPOSITORY}

.PHONY: deploy
deploy: ## (Cloud): Deploy code
	@ sam deploy \
		--template-file packaged-template.yaml \
		--parameter-overrides BucketName=${BUCKETNAME} TopicName=${TOPICNAME} EndpointEmail=${ENDPOINTEMAIL} \
		--stack-name ${STACK-NAME} \
		--capabilities CAPABILITY_IAM \
		--region ${REGION} \
		--image-repository ${IMAGE-REPOSITORY}

PHONY: undeploy
undeploy: ## (Cloud): Undeploy code
	@ aws s3 rm --recursive s3://${BUCKETNAME}/
	@ aws cloudformation delete-stack --stack-name ${STACK-NAME}

help:
	@ echo "Please use \`make <target>' where <target> is one of"
	@ perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
