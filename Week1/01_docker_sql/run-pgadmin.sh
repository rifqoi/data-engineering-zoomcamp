#!/bin/bash

docker run -it \
	--rm \
	-d \
	--name pgadmin \
	--network=pg-network \
	-e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
	-e PGADMIN_DEFAULT_PASSWORD="root" \
	-p 8080:80 \
	dpage/pgadmin4:6.4

