# CNU Stats API

## Problem Statement

This is related to my [CNU Men's Basketball Data Dashboard](https://github.com/nathanroberts55/CNUMBBMLProject). For that project I use a Azure Local Storage account to save the data scraped from the websites and used by the dashboard. However, I think that a better solution to the issue would be if there was an API and database that the information was stored in and called to when the dashboard needs the statistics. Additionally, I was thinking to seperate the API as if I decide to expand the API to include more teams (e.g. like the other teams in the C2C conference) then it can be open to the public.

This project hopefully serves as a solution to the issue of easily gathering clean data that can be used by coaches, players, and other data professionals looking to analyze the statistics for one of the best Division 3 basketball teams in the country.

## Current Solution

I decided to create the API using python as it is the language that I know best and am working on mastering. Plus I found some great libraries that made it quick and simple to stand up an API. The API consists of the following:

- API: FastAPI and SQLModel
- Database: PostgreSQL

### API: FastAPI and SQLModel

[FastAPI](https://fastapi.tiangolo.com/) is a great python framework that allowed me to quickly stand up an API. It's very simple, intuitive, and fast/performant. It also has a super simple integrationg with the rest of the stack that I am using. Speaking of which, to initialize the database I decided to use [SQLModel](https://sqlmodel.tiangolo.com/), which is a library for interacting with SQL databases using python. I use SQLModel to define the tables and entities that are used by the API. Again, it's super simple, intuitive, and compatible with FastAPI (because it was created by the same person!).

### Database: PostgresSQL

I decided to use a PostgreSQL database because initially the way I setup the CNU Stats Dashboard streamlit app to work was every time that it was initialized that it scraped the university's athletics page for the stats and saved them locally. And while that would've been fine for me, I assume that if the website got some decent traffic that the university wouldn't like all the request that I would be making to the page. So instead I will scrape the data periodically and save it to the database, that way if there's traffic I will bombard my own resources and not theirs. This will be the source for the API.

## Future Work/Improvement Ideas

I have some other ideas that I wanted to implement as well and may become part of the project as time goes on.
Here are some of the ideas that I have:

- API Authentication
- CI/CD Pipeline for Updates
- Integrate ML Endpoint
  - The CNU Stats Dashboard I created I wanted to have ML features, but maybe if I get the ML working that I can bring it to the API for inference to be offloaded.
