#gtj-events-scraper

#Usage

#Installation

#Requirements

#Tests
- `cd gtjevents && ptw`

#Authors
`gtj-events-scraper` was written by Sam Getz Sheftel

#Deploying
- `git push heroku master`

#Logs
- `heroku logs --tail`
- `heroku logs -n 1500`

TODOs

- [x] Determine the email/account I will use for the app services*
- [x] Finish the Scraper
- [x] Validate the scraper
- [x] Setup events database on MongoHQ
- [x] Create v0.1.0 of the event data service API using Python and EVE
- [ ] Add basic Authentication to the data service and restring all HTTP verbs except GET from calling the api without authentication
- [x] Deploy the events data service
- [x] Create the srapper worker dyno and integrate it with the data service
- [ ] validate the scrapper is able to detect updates to events and new events*
- [ ] Deploy the scrapper worker dyno to Heroku
