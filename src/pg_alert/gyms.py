# flake8: noqa
from .errors import UnsupportedGym


GYM_BOOKING_URLS = {
    'Belmont roped': 'https://app.rockgympro.com/b/widget/?a=offering&offering_guid=b4f9a803f9c54cdc995f3b93200568af&widget_guid=b7c6e7d4c2bd41b1a44990b9a402886c&random=603f0b4f48d5a&iframeid=&mode=p',
    'Belmont bouldering': 'https://app.rockgympro.com/b/widget/?a=offering&offering_guid=680c6293f39a4ba2aad9b34467414790&widget_guid=b7c6e7d4c2bd41b1a44990b9a402886c&random=6041d23ad6fbe&iframeid=&mode=p',
    'Sunnyvale': 'https://app.rockgympro.com/b/widget/?a=offering&offering_guid=29f1b5a8577043f99a2ebf2bca3aa570&random=6041d239991e4&iframeid=&mode=p',
    'Santa Clara': 'https://app.rockgympro.com/b/widget/?a=offering&offering_guid=9f626bb4703e46a8a7b2c7442a4e8e3d&random=6041d26197360&iframeid=&mode=p',
    'San Fransisco': 'https://app.rockgympro.com/b/widget/?a=offering&offering_guid=38c7c0acf0a24626a99dd0765734730b&random=6041d260b75cd&iframeid=&mode=p',
}


def get_gym_url(gym_name):
    if gym_name in GYM_BOOKING_URLS:
        return GYM_BOOKING_URLS[gym_name]
    else:
        raise UnsupportedGym(f"Unknown gym {gym_name}.")
