#!/bin/bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000 &
sleep 3
python frontend.py