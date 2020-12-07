#!/bin/bash

# not limited to Linux, if you can make through the package installs.

cd backend; flask run &
cd ../frontend/profiler
npm run serve