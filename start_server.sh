#!/usr/bin/env bash
gunicorn --certfile ./cert/full_chain.pem --keyfile ./cert/private.key -b 0.0.0.0:443 wsgi