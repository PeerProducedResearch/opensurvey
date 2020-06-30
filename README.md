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

### Translations / i18n


#### Activate a new language

To activate a new language edit the **LANGUAGES** setting in **settings.py**

```
LANGUAGES = [
  ('en', _('English')),
  ('fr', _('French')),
  ('de', _('German')),
]
```

You need to do this first before translating because the language name itself needs to be translated.

#### Add a new language
To add a new language simply add a new directory in /locale with the language code as name, for example: 
**/locale/fr** for french.

Then to generate the translation files run:

`python manage.py makemessages`

It will create **django.po** files inside each /\<lang\>/LC_MESSAGES directory.

You can edit these files directly with any text editor or specialized software / web application. 

Once the translations are complete, to generate the binary files optimized for consumption by Django, run:

`python manage.py compilemessages`

It will create **django.mo** files inside each /\<lang\>/LC_MESSAGES directory.
