#https://app.localstack.cloud/inst/default/status
#https://testwebsite.s3-website.localhost.localstack.cloud:4566/
install:
	pip install localstack

start:
	localstack start

docker-start:
	docker run -d --name localstack -p 4566:4566 -p 4571:4571 localstack/localstack

terrafrom_init:
	terraform init

terrafrom_fmt:
	terraform fmt

terrafrom_validate:
	terraform validate

terrafrom_apply:
	terraform apply

ls_s3:
	aws --endpoint-url=http://localhost:4566 s3 ls

services:
	localstack status services
