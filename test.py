from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.common.exceptions import NoSuchElementException


class NotFoundException(Exception):
    ...


class InvalidCredentialsException(Exception):
    ...


class D2ruViewsScrapper:
    def __init__(self, username, password):
        self.counter = 0
        self.driver = webdriver.Firefox()
        self.username = username
        self.password = password

    def open_home_page(self):
        self.driver.get("https://dota2.ru/forum")

    def fill_login_fields(self):
        self.driver.find_element_by_id("login_credential_form").send_keys(self.username)
        self.driver.find_element_by_id("login_password_form").send_keys(self.password)

    def press_login_btn(self):
        confirm_login_btn = self.driver.find_element_by_class_name("authorization__btn")
        self.driver.execute_script("arguments[0].click()", confirm_login_btn)

    def validate_login(self):
        try:
            self.driver.find_element_by_class_name("mr6")  # check if "login" button exist on page
            return 403
        except NoSuchElementException:
            return 200

    def login(self):
        self.open_home_page()
        self.fill_login_fields()
        self.press_login_btn()
        sleep(5)
        if self.validate_login() == 403:
            raise InvalidCredentialsException("Invalid credentials")

    def find_user_profile(self, user_to_scrapp):
        self.driver.find_element_by_class_name("header__link-search__button").click()
        search_field = self.driver.find_element_by_class_name(
            "header__item-search__field"
        )
        search_field.send_keys(user_to_scrapp)
        search_field.send_keys(Keys.ENTER)
        sleep(5)
        try:
            return list(
                self.driver.find_elements_by_class_name("forum-theme__top-block")
            )[1].find_element_by_class_name("user-link")
        except NoSuchElementException:
            raise NotFoundException("User not found")

    def check_is_user_page_valid(self, user_to_scrapp):
        username_page = (
            self.driver.find_element_by_class_name("forum-profile__head-title")
                .find_element_by_tag_name("span")
                .text
        )
        if username_page != user_to_scrapp:
            raise NotFoundException("User not found")

    def get_count_of_views(self):
        head_list = self.driver.find_element_by_class_name("forum-profile__head-list")
        views_counter = list(
            head_list.find_elements_by_class_name("forum-profile__head-item")
        )[5].find_element_by_class_name("forum-profile__head-item-text")
        return views_counter.text

    def get_user_profile_views(self, user_to_scrapp):
        if self.counter == 0:
            self.login()
        else:
            self.open_home_page()
        self.counter += 1
        link = self.find_user_profile(user_to_scrapp)
        link.click()
        self.check_is_user_page_valid(user_to_scrapp)
        return int(self.get_count_of_views())

