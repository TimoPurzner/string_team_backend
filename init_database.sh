#!/bin/bash

rm database.db
sqlite3 database.db < init_database.sql
