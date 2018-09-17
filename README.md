# instigatorDetection
Looking into twitter events to model spread of local correlated events

[Twitter App](https://apps.twitter.com/app/15848846)

## Setup
createdb instigator_detection
cd alembic
export SQLALCHEMY_DATABASE_URI=postgresql:///instigator_detection
alembic upgrade head

## API Documentation
[Rate-Limits](https://developer.twitter.com/en/docs/basics/rate-limits)
[Paging](https://developer.twitter.com/en/docs/tweets/timelines/guides/working-with-timelines)
