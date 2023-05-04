# DRF social media API

You can create user profile with picture, 
bio and other details. Users can create posts, add hashtags to posts and follow other users.

Security is assured by use of JWT tokens authentication.

Comprehensive documentation.

## Installation

Python must be installed before the next steps:

```shell
git clone https://github.com/ada-krav/DRF_social_media_API.git
cd DRF_social_media_API
python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)
pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

