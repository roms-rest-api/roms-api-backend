[![roms-rest-api](https://i.imgur.com/ju5Lrrs.png)](https://github.com/roms-rest-api)

# roms-api-backend

# Features
- Generates changelogs automatically from device trees in your org
- Create a changelog-page to telegraph
- Upload builds to your GDrive
- Posts automatically builds with changelogs, device name, rom banner, maintainer name and download link in your telegram channel
- Docker support
- Firebase support
---
# How to deploy?
## Installing requirements
- Clone this repo and install requirements:
<div class="termy">

```console
$ git clone https://github.com/roms-rest-api/roms-api-backend

$ cd roms-api-backend

$ python3 -m pip install -r requirements.txt

```
</div>

## Setting up config file
<details>
    <summary><b>Click here for more details</b></summary>

Fill up rest of the fields. Meaning of each fields are described below:
- **devices_org**: This is the name of your github organization.
- **github_token**: This is your github token.
- **drive_id**: This is the folder ID of the Google Drive Folder to where you upload your builds.
- **firebase_cred_file**: This is the path to your firebase credential file.
- **firebase_project_id**: This the id of your firebase project id, check url after you created a project
- **firebase_collection_user**: This is the name of the collection for user authentification.
- **firebase_collection_admin**: This is the name of the collection for admin authentification.
- **firebase_rldb**: This is the url of your firebase realtime database.
- **firebase_rldb_builds_db**: This is the collection name where save informations about builds.
- **rom_name**: This is the name of your rom.
- **author_name**: This is the author name for telegraph posts.
- **rom_pic_url**: This the rom banner url
- **telegram_token**: The telegram bot token that you get from [@BotFather](https://t.me/BotFather)
- **channel_name**:  This is the name of your telegram channel for example @channel123
- **support_group**: This is the support group name for example @DerpFest5T 
- **devices_url**: This is the direct link to your devices.yaml file in your organization
</details>

## Create a firebase instance
- Visit [Firebase Console](https://console.firebase.google.com/)
- Add a project
- Type in a project name
- Create a Firestore Database and choose Productionmode
- Go to Projectsettings and go to service account, then click on Firebase Admin SDK and create your private key (add it later to roms-api-backend as firebase_credentials.json)
- Create a Realtime Database and choose lockmode
- Copy your database url (in config: firebase_rldb)

## Getting Google OAuth API credential file for Google Drive

- Visit the [Google Cloud Console](https://console.developers.google.com/apis/credentials)
- Go to the OAuth Consent tab, fill it, and save.
- Go to the Credentials tab and click Create Credentials -> OAuth Client ID
- Choose Desktop and Create.
- Use the download button to download your credentials.
- Move that file to the root of mirrorbot, and rename it to credentials.json
- Visit [Google API page](https://console.developers.google.com/apis/library)
- Search for Drive and enable it, if it is disabled
- Finally, start roms-api-backend and generate your **token.json** file for Google Drive:

## Deploying
### If you want to deploy it with docker
- Clone [Traefik-Configs](https://github.com/roms-rest-api/traefik-configs) and follow the instructions in readme file

- Build Docker image:
<div class="termy">

```console
$ sudo docker build . -t backend
```
</div>

- Replace your domain name in docker-compose-yml

- Run the image, if you replaced your domain name in docker-compose.yml:
<div class="termy">

```console
$ sudo docker-compose up -d
```
</div>

## Without docker:
<div class="termy">

```console
$ python3 -m uvicorn api:app --reload --host 0.0.0.0 (use gunicorn in production)

```
</div>

## How to upload builds?
This is an example for uploading builds. Replace your values with ones written in caps lock.
<div class="termy">

```console
$  curl -X 'POST'   'https://api.YOUR.DOMAIN/api/upload' \   
                    -H 'accept: application/json' \  
                    -H 'Content-Type: multipart/form-data' \
                    -F 'codename=DEVICENAME' 
                    -F 'version=YOURANDROIDVERSION' \   
                    -F 'username=YOURUSERNAME' \  
                    -F 'file=@PATH/TO/YOUR/BUILD.ZIP;type=application/zip' \
                    -F 'token=YOURTOKEN' \
```
</div>


