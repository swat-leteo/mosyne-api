# Mosyne API

**Mosine** is a web application that try to help to Alzheimer persons an its families.
With **Mosine** you can register some relevat info of your familiar/friend with alzheimer (angels like we call them). Info like health and personal data and a listh of emergency contacts.

With this info **Mosine** generate a QR code that you can print and make badge or a nice bracelet that your angel can wear it.

If your angel is loss and a good person find him/her, he/she can scan the QR code with a phone camera and quickly they will have access to relevant info to help your angel and get in touch with you.

**Mosine API** is a REST API service that allow manage the backend operations of **Mosine** App.

## Tech Stack

- Programming Language: Python
- Web Framework: [FatAPI](https://fastapi.tiangolo.com/)
- DB: PostgresSQL (CloudSQL)
- ORM: [TortoiseORM](https://tortoise-orm.readthedocs.io/en/latest/) and [Aerich](https://github.com/tortoise/aerich) as migration tool.
- Authentication: JWT (cookie bassed)
- Server: AppEngine
- Storage: Google Cloud Storage

## Features

- `Services`:
  - Allow to upload image to cloud storage
  - QR code generator
  - Email for verification and password recovery

- `Code`:
  - RESTFul API
  - Request & Response Validation
  - Swagger Documentation
  - Docker Based
  - e2e Testing - (Coverage: 87%)
  - Automatic migrations
  - Github Actions for CICD
  - Automatic deploy to AppEngine after tests
  - Black (PEP8) format tool

## Usage

- Clone this repository:

```bash
git clone git@github.com:swat-leteo/mosyne-api.git
```

- Prerequisites:
  - Poetry
  - Docker
  - docker-compose
  - git

- Prepare your computer for dev:
  - Install all dependencies with: `poetry install`.
  - Switch to the virtual env: `poetry shell`.
  - If you use VsCode modify the .vscode file with:

```json
{
  "python.venvPath": "~/.cache/pypoetry/virtualenvs",
  "python.pythonPath": "~/.cache/pypoetry/virtualenvs/<name_of_your_virtualenv>"
}
```

- Build the Docker image

```bash
source scripts/build.sh

# or

docker-compose build
```

This command create all required images and initialize the DB.

- Lauch the server

```bash
docker-compose up

# or

source scripts/start.sh
```

- Use the linter and format scripts:
**Use this before all commits**

```bash
# lintern (optional)
source scripts/lint.sh

# code formater
source scripts/format.sh
```

## Project architecture

**app**
  - ***main.py*** - Server entrypoint.
  - ***db.py*** - Db confgigurations.
  - ***config.py*** - App settings.
  - ***prestart.sh*** - Prestart script - Manage migrations.
  - `tests` - e2e Testing.
  - `services` - App services.
    - `mails` - Module to manage the sending of emails.
    - `qr` - Module to manage the QR code creation.
    - `storage` - Module to upload images.
  - `api` - API entities.
    - `utils` - Api utilis.
    - `auth` - Authentication operations.
    - `users` - Users operations.
    - `angels` - Angels operations.
      - This is the entities file structure.
      - `models` - DB models.
      - ***controller.py*** - Bussiness logic of each endpoint.
      - ***schemas.py*** - Data transfer object schemas.
      - ***router.py*** - API endpoints implementation.

## ER Diagram

![imagen](https://user-images.githubusercontent.com/62397465/97359426-5bbe6c80-1862-11eb-85ff-dc41085a330e.png)

## Endpoints

- API docs (by OpenAPI): https://api-mosine.appspot.com/docs
- API dics (by Redoc): https://api-mosine.appspot.com/redoc

- Prefix: `/api`

### Auth

- **Signup**
  - Method: `POST`
  - PATH: `/auth/signup`
  - Action: Create user account (aka guardian)

- **Login**
  - Method: `POST`
  - PATH: `/auth/login`
  - Action: Validate credentials and set cookie session

- **Logout**
  - Method: `POST`
  - PATH: `/auth/logout`
  - Needs Authorization: `True`
  - Action: remove cookie session

- **Email Verification**
  - Method: `POST`
  - PATH: `/auth/verification?email=email@...`
  - Action: Send email with account token verification

- **Recovery Password**
  - Method: `POST`
  - PATH: `/auth/recovery-password?email=email@...`
  - Action: Send email with recovery password token

- **Reset Password**
  - Method: `POST`
  - PATH: `/auth/reset-password`
  - Action: Reset the account credentials (password)


### Users (aka Guardians)

- **Complete Profile**
  - Method: `POST`
  - PATH: `/users`
  - Needs Authorization: `True`
  - Action: Create user profile

- **Retriev Info**
  - Method: `GET`
  - PATH: `/users`
  - Needs Authorization: `True`
  - Action: Return all user info

- **Update Info**
  - Method: `PUT`
  - PATH: `/users`
  - Needs Authorization: `True`
  - Action: Update the user info

- **Delete account**
  - Method: `DELETE`
  - PATH: `/users`
  - Needs Authorization: `True`
  - Action: Delete the user account and all related info

- **Angel profile advise**
  - Method: `POST`
  - PATH: `/users/angel-advise`
  - Action: Send email to user when the angel profile is visited

### Angels

- **Register Angel**
  - Method: `POST`
  - PATH: `/angels`
  - Needs Authorization: `True`
  - Action: Create an Angel profile

- **Retrieve Angel info**
  - Method: `GET`
  - PATH: `/angels/{id}`
  - Action: Return the complete Angel info

- **Update Angel info**
  - Method: `PATCH`
  - PATH: `/angels/{id}`
  - Needs Authorization: `True`
  - Action: Updates Angel info

- **Remove Angel**
  - Method: `DELETE`
  - PATH: `/angels/{id}`
  - Needs Authorization: `True`
  - Action: Remove Angel profile

- **Get Angel QR**
  - Method: `GET`
  - PATH: `/angels/{id}/qr`
  - Needs Authorization: `True`
  - Action: Return QR code

## Authors

- Emanuel Osorio <emanuelosva@gmail.com>
- Jair Águilar <https://github.com/TEGDV>
