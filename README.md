My Blog with Django !

    - a django weblog with new admin pannel
    - recapcha V2 and V3 together
    - maximum try for days in session (activation link and new password)
    - template tags
    - make your own templates (exp : http://www.pylinux.ir)

    base : 
        - internal messaging (writer, staff, superusers) and reply
        - check comment words (profanity)
        - create blog post, edit and publish

    authentication :
        - email base (email instead of username)
        - oauth (google and git hub login)
        - register, activation link and forgot password >> celery email managing 

    home :
        - blog and blog sort 
        - blog sorted by categories
        - tags 

    - Create your own .env file in root dir with parameters :

            SECRET_KEY
            DEBUG
            ALLOWED_HOSTS
            DB_NAME
            DB_USER
            DB_PASSWORD
            DB_HOST
            RECAPTCHA_SECRET_KEY
            RECAPTCHA_SITE_KEY
            RECAPTCHA_SITE_KEY_V2 
            RECAPTCHA_SECRET_KEY_V2
            SOCIAL_AUTH_GITHUB_KEY
            SOCIAL_AUTH_GITHUB_SECRET
            SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
            SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET
            EMAIL_HOST
            EMAIL_PORT
            EMAIL_HOST_USER
            EMAIL_HOST_PASSWORD


    




