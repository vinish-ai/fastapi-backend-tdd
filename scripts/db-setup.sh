#!/bin/sh

export PGUSER=postgres

psql -c "CREATE DATABASE web_dev;"
psql -c "CREATE DATABASE web_test;"
