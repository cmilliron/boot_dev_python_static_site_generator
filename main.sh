#!/bin/bash

python3 src/main.py "boot_dev_python_static_site_generator"
cd docs && python3 -m http.server 8888
