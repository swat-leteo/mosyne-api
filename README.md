# Mosyne API

Some description...

## Tech Stack

## Features

## Usage

- Clone this repository:

```bash
git clone git@github.com:swat-leteo/mosyne-api.git
```

- Prepare your computer for dev:
  - Go to `app/prestart.sh` and comment the bash commands.
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
# lintern
source scripts/lint.sh

# code formater
source scripts/format.sh
```

## Project architecture

## ER Diagram

## Endpoints

- API docs (by swagger): https://musyne-api.appspot.com/docs

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
  - Action: remove cookie session

- **Email Verification**
  - Method: `POST`
  - PATH: `/auth/verification/{email}`
  - Action: Send email with account token verification

- **Recovery Password**
  - Method: `POST`
  - PATH: `/auth/recovery-password/{email}`
  - Action: Send email with recovery password token

- **Reset Password**
  - Method: `POST`
  - PATH: `/auth/reset-password`
  - Action: Reset the account credentials (password)


### Users (aka Guardians)

- **Create Profile**
  - Method: `POST`
  - PATH: `/users`
  - Action: Create user profile

- **Retriev Info**
  - Method: `GET`
  - PATH: `/users`
  - Action: Return all user info

- **Update Info**
  - Method: `PATCH`
  - PATH: `/users/{id}`
  - Action: Update the user profile

- **Delete account**
  - Method: `DELETE`
  - PATH: `/users/{id}`
  - Action: Delete the user account and all related info

- **Angel profile advise**
  - Method: `POST`
  - PATH: `/users/angel-advise`
  - Action: Send email to user when the angel profile is visited

### Angels

- **Register Angel**
  - Method: `POST`
  - PATH: `/angels`
  - Action: Create an Angel profile

- **Retrieve Angel info**
  - Method: `GET`
  - PATH: `/angels/{id}`
  - Action: Return the complete Angel info

- **Update Angel info**
  - Method: `PATCH`
  - PATH: `/angels/{id}`
  - Action: Updates Angel info

- **Remove Angel**
  - Method: `DELETE`
  - PATH: `/angels/{id}`
  - Action: Remove Angel profile

- **Get Angel QR**
  - Method: `GET`
  - PATH: `/angels/{id}/qr`
  - Action: Return QR code

## Authors

- Emanuel Osorio <emanuelosva@gmail.com>
- Jair Águilar <>
