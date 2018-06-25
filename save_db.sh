#!/bin/bash
# Copy database from container

docker cp twebreg1:/app/db.sqlite3 db.sqlite3
