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

### Design dev

Assumes you have a basic understanding of how node and yarn/npm work.  
Node version used: 12.16.1

We use [PostCSS](https://github.com/postcss/postcss) to enhance browser compatibility, accessibility and preformances.  
A `package.json` and a `postcss.config.js` config file exist at the document root. Add or remove plugin from there.

In order to edit the styles, you need to:

- run `yarn install` or `npm i`
- edit the styles in `src > css > parts`
- run `yarn watch` or `npm run watch` while in developement (watches the changes)
- run `yarn build` or `npm run dev` for production

The optimized and minified style file is under `static > css`
