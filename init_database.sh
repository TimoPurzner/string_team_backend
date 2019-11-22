#!/bin/bash

rm database.db
sqlite database.db < init_database.sql
