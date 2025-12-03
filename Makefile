build:
	docker build -t dudevpn_supportbot_image .
run:
	docker run -it -d --env-file .env --restart=unless-stopped --name dudevpn_supportbot dudevpn_supportbot_image
stop:
	docker stop dudevpn_supportbot
attach:
	docker attach dudevpn_supportbot
dell:
	docker rm dudevpnsupport_bot
	docker image remove dudevpn_supportbot_image
update:
	make stop
	make dell
	make build
	make run