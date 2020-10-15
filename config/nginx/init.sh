#!/usr/bin/env bash

echo "Starting SSH ..."
service ssh start

nginx -g "daemon off;"