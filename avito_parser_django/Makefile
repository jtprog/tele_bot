#!/bin/sh

export PYTHONPATH:=$(shell pwd)/avito

run_admin:
	python avito/manage.py runserver

parse:
	python avito/manage.py parse_avito
