# 370p2

$ export FLASK_APP=server.py
$ python -m flask run

# TODO:

## BACKEND:
- [x] sql connect and disconnect before and after every transaction (https://stackoverflow.com/questions/47711689/error-while-using-pymysql-in-flask)
- [x] Date system
- [x] Login
- [x] Registration
- [x] Registration should allow user to enter first and last name
- [x] Map
- [x] Show user bookings
- [x] Cancel user booking
- [x] Create user booking
- [x] Search
- [x] search needs to link to hotel URLS
- [x] search needs to only show hotels, not rooms
- [x] search needs to show hotel room prices
- [x] -> Also needs to show how many rooms match this
- [x] hotel needs to link to the booking for that room
- [x] Hotel pages
- [x] booking needs to be cancellable from hotel page
- [x] Hotel administration panel
- [x] Create hotel franchise

## FRONT END

- [x] Map
- [x] User
- [x] Hotel
- [x] Search
- [x] search needs to be sortable

## DATABASE

- [x] Diagram

#### Queries
- [x] Login
- [x] Registration
- [x] Map
- [x] Search
- [x] Show customer bookings
- [x] Show hotel admin bookings
- [x] Create booking
- [x] Remove booking
- [x] Create hotel franchise
#### Tables
- [x] Account
- [x] Hotel chain
- [x] Hotel franchise
- [x] Address
- [x] Room
- [x] Booking

## QA

- [ ] Unit tests
- [ ] make sure date appears on every relevant page.
- [x] each hotel chain must have at least two franchises
- [x] must be at least 3 hotel chains.
- [ ] include login/password for ALL hotel chains

## PROJECT REPORT

- [ ] Complete instructions on how to access and run the team's application
- [ ] Teacher must have information for him to access the accounts of all the hotel administrators (to add more hotels, etc)
- [ ] Explanation of how to navigate between diferetn screens, e.g. how to access the search engine
- [ ] List of team meetings
- [ ] Summary of project architecture
- [ ] List of project responsibilities to team members i.e. what did each person do
- [ ] A list of the project goals/milestones
- [ ] A timeline of progress for the completion of the project milestones
- [ ] A list of unit tests AND a timetable when each test was successfully passed
- [ ] If necessary, what corrective steps were taken if the work fell behind schedule
