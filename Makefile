default: test

COMPOSE_FILE_DEV = docker-compose-dev.yml
COMPOSE_FILE_BUILD = docker-compose-build.yml

export OPACSSM_BUILD_DATE=$(shell date -u +"%Y-%m-%dT%H:%M:%SZ")
export OPACSSM_VCS_REF=$(strip $(shell git rev-parse --short HEAD))
export OPACSSM_WEBAPP_VERSION=$(strip $(shell cat VERSION))

webapp_version:
	@echo "Version file: " $(OPACSSM_WEBAPP_VERSION)

vcs_ref:
	@echo "Latest commit: " $(OPACSSM_VCS_REF)

build_date:
	@echo "Build date: " $(OPACSSM_BUILD_DATE)

remove_celery_pid:
	rm celerybeat.pid

remove_celery_schedule:
	rm celerybeat-schedule

############################################
## atalhos docker-compose desenvolvimento ##
############################################

dev_compose_build:
	@docker-compose -f $(COMPOSE_FILE_DEV) build

dev_compose_up:
	@docker-compose -f $(COMPOSE_FILE_DEV) up -d

dev_compose_logs:
	@docker-compose -f $(COMPOSE_FILE_DEV) logs -f

dev_compose_stop:
	@docker-compose -f $(COMPOSE_FILE_DEV) stop

dev_compose_ps:
	@docker-compose -f $(COMPOSE_FILE_DEV) ps

dev_compose_rm:
	@docker-compose -f $(COMPOSE_FILE_DEV) rm -f
	rm celerybeat.pid
	rm celerybeat-schedule

dev_compose_django_shell:
	@docker-compose -f $(COMPOSE_FILE_DEV) run --rm django python manage.py shell

dev_compose_django_createsuperuser:
	@docker-compose -f $(COMPOSE_FILE_DEV) run --rm django python manage.py createsuperuser

dev_compose_django_bash:
	@docker-compose -f $(COMPOSE_FILE_DEV) run --rm django bash

dev_compose_django_test:
	@docker-compose -f $(COMPOSE_FILE_DEV) run --rm django python manage.py test

dev_compose_django_fast:
	@docker-compose -f $(COMPOSE_FILE_DEV) run --rm django python manage.py test --failfast

dev_compose_django_makemigrations:
	@docker-compose -f $(COMPOSE_FILE_DEV) run --rm django python manage.py makemigrations

dev_compose_django_migrate:
	@docker-compose -f $(COMPOSE_FILE_DEV) run --rm django python manage.py migrate

dev_compose_haystack_clear_index:
	@docker-compose -f $(COMPOSE_FILE_DEV) run --rm django python manage.py clear_index

dev_compose_haystack_update_index:
	@docker-compose -f $(COMPOSE_FILE_DEV) run --rm django python manage.py update_index

dev_compose_haystack_rebuild_index:
	@docker-compose -f $(COMPOSE_FILE_DEV) run --rm django python manage.py rebuild_index

dev_compose_haystack_haystack_info:
	@docker-compose -f $(COMPOSE_FILE_DEV) run --rm django python manage.py haystack_info


# add rebuild index, clean_index, update_index

#####################################################
## atalhos docker-compose build e testes no traivs ##
#####################################################

travis_compose_build:
	@echo "[Travis Build] opac version: " $(OPACSSM_WEBAPP_VERSION)
	@echo "[Travis Build] lates commit: " $(OPACSSM_VCS_REF)
	@echo "[Travis Build] build date: " $(OPACSSM_BUILD_DATE)
	@echo "[Travis Build] compose file: " $(COMPOSE_FILE_BUILD)
	@docker-compose -f $(COMPOSE_FILE_BUILD) build

travis_compose_up:
	@docker-compose -f $(COMPOSE_FILE_BUILD) up -d

travis_compose_django_test:
	@docker-compose -f $(COMPOSE_FILE_BUILD) run --rm django python manage.py test

travis_compose_django_test_fast:
	@docker-compose -f $(COMPOSE_FILE_BUILD) run --rm django python manage.py test --failfast

travis_compose_django_collectstatic:
	@docker-compose -f $(COMPOSE_FILE_BUILD) run --rm django python manage.py collectstatic --no-input

travis_compose_django_migrate:
	@docker-compose -f $(COMPOSE_FILE_BUILD) run --rm django python manage.py migrate

travis_run_audit:
	@docker run \
	-it --net host --pid host \
	--cap-add audit_control \
	-v /var/lib:/var/lib \
  	-v /var/run/docker.sock:/var/run/docker.sock \
  	-v /usr/lib/systemd:/usr/lib/systemd \
  	-v /etc:/etc \
  	--label docker_bench_security \
  	docker/docker-bench-security

###########################################################
## atalhos docker-compose build e push para o Docker Hub ##
###########################################################

release_docker_build:
	@echo "[Building] Release version: " $(OPACSSM_WEBAPP_VERSION)
	@echo "[Building] Latest commit: " $(OPACSSM_VCS_REF)
	@echo "[Building] Build date: " $(OPACSSM_BUILD_DATE)
	@echo "[Building] Image full tag: $(TRAVIS_REPO_SLUG):$(COMMIT)"
	@docker build \
	-t $(TRAVIS_REPO_SLUG):$(COMMIT) \
	--build-arg OPACSSM_BUILD_DATE=$(OPACSSM_BUILD_DATE) \
	--build-arg OPACSSM_VCS_REF=$(OPACSSM_VCS_REF) \
	--build-arg OPACSSM_WEBAPP_VERSION=$(OPACSSM_WEBAPP_VERSION) .

release_docker_tag:
	@echo "[Tagging] Target image -> $(TRAVIS_REPO_SLUG):$(COMMIT)"
	@echo "[Tagging] Image name:latest -> $(TRAVIS_REPO_SLUG):latest"
	@docker tag $(TRAVIS_REPO_SLUG):$(COMMIT) $(TRAVIS_REPO_SLUG):latest
	@echo "[Tagging] Image name:latest -> $(TRAVIS_REPO_SLUG):travis-$(TRAVIS_BUILD_NUMBER)"
	@docker tag $(TRAVIS_REPO_SLUG):$(COMMIT) $(TRAVIS_REPO_SLUG):travis-$(TRAVIS_BUILD_NUMBER)

release_docker_push:
	@echo "[Pushing] pushing image: $(TRAVIS_REPO_SLUG)"
	@docker push $(TRAVIS_REPO_SLUG)
	@echo "[Pushing] push $(TRAVIS_REPO_SLUG) done!"

#########
## gRPC #
#########

generate_grpc:
	@python3 -m grpc_tools.protoc -I grpc_ssm --python_out=grpc_ssm --grpc_python_out=grpc_ssm grpc_ssm/opac.prot

#########
## test #
#########

test:
	@python manager test
