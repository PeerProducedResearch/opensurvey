## Demo of how Open Humans to OpenClinica workflow can work

### Install

Assumes you have a basic understanding of how Django, `pipenv`, & `heroku` work:

- `pipenv install`
- `pipenv shell`
- `heroku local:run python manage.py migrate`
- `heroku local`

Web-server should be up on `127.0.0.1:5000`

### Setup

Copy the `env.sample` as `.env` and fill in the missing bits. Required:
- An Open Humans project
- Having a _Participate_ enabled Open Clinica survey and the corresponding token to add participants etc.

Demo deployment runs on https://opensurveytest.herokuapp.com/

Logging in with Open Humans will:
- Create Open Clinica participant
- Schedule first survey for them
- Get participant access survey_token
- Email this via Open Humans to just registered participant
