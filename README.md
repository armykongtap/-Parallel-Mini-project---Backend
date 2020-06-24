# Parallel_MiniProject_Backend
This project is path of 2110315 Parallel and Distributed Systems (2019/2)

HOW_TO_RUN
1. docker run -p 6379:6379 -d redis:5
2. python manage.py migrate //only for first time
3. python manage.py runserver

if you want some sample data
1. python manage.py shell
2. copy code from intnitial_data.py
