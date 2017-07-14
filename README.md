# Running:

```shell
	docker build -t docker-windows-release-updater .
	docker run \
		-e BUCKET_NAME \
		--rm docker-windows-release-updater 17.06.1-ee-rc1 test https://download.docker.com/components/engine/windows-server/17.03/docker-17.03.1-ee.zip
```
