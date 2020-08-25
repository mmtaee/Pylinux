from django.conf import settings

# pip install git+https://git@github.com/ping/instagram_private_api.git@1.6.0
# pip install git+https://git@github.com/ping/instagram_private_api_extensions.git@0.3.9
from instagram_private_api import Client, MediaRatios
from instagram_private_api_extensions import media

accounts = {
    # TODO : change usernames in deployment
    'username_1': settings.INSTAGRAM_PASSWORD_1,
    'username_2': settings.INSTAGRAM_PASSWORD_2,
}

def send_to_instagram(instance):
    photo_data, photo_size = media.prepare_image(
        instance.image.path,
        aspect_ratios=MediaRatios.standard
        )
    caption = instance.title.title() + "\n" + f"#{instance.category}"
    for tag in instance.tags.all():
        caption += f" #{tag}"  

    for user, passwd in accounts.items():
        try:
            api = Client(user, passwd)
            api.post_photo(photo_data, photo_size, caption=caption)

        except Exception as error:
            with open ("logs/insta_log.txt" , 'a') as f:
                text = str(error) + "\n"
                f.write(text)
        
