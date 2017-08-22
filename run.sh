#!/bin/bash
python3 ./Brick.py &
backgroundPID=$!
cd ./MusicBot
python3 ./run.py
trap "kill $backgroundPID" EXIT
