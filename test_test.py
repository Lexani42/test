from test import D2ruViewsScrapper


def test_scrapper():
    scrapper = D2ruViewsScrapper('login', 'password')
    assert scrapper.get_user_profile_views('lexani42') == 393
    assert scrapper.get_user_profile_views('test') == 27
    assert scrapper.get_user_profile_views('TEST NA DAUNA') == 16
    assert scrapper.get_user_profile_views('Chelik') == 30
