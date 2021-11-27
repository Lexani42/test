from test import D2ruViewsScrapper

scrapper = D2ruViewsScrapper('login', 'password')


def test_lexani42():
    assert scrapper.get_user_profile_views('lexani42') == 393


def test_test():
    assert scrapper.get_user_profile_views('test') == 27


def test_test_na_dauna():
    assert scrapper.get_user_profile_views('TEST NA DAUNA') == 16


def test_chelik():
    assert scrapper.get_user_profile_views('Chelik') == 30
