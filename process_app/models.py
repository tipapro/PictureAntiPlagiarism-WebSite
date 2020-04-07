from django.db import models
# from imgurpython import ImgurClient
#
#
# client_id = '620e8fb724910b6'
# client_secret = '3b5f7575c67d9317c8872e18ef611d5795223c7b'
#
# client = ImgurClient(client_id, client_secret)
#
# # Authorization flow, pin example (see docs for other auth types)
# authorization_url = client.get_auth_url('pin')
#
# # ... redirect user to `authorization_url`, obtain pin (or code or token) ...
# credentials = client.authorize('PIN OBTAINED FROM AUTHORIZATION', 'pin')
# client.set_user_auth(credentials['access_token'], credentials['refresh_token'])


class UploadedImage(models.Model):
    image = models.ImageField(upload_to='MEDIA_ROOT', null=True, blank=True)

