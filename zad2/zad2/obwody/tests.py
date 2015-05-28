from django.utils import timezone
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test.utils import setup_test_environment
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

from models import Gmina, Obwod

import time

class SeleniumTests(StaticLiveServerTestCase):
    def setUp(self):
        self.gmina = Gmina.objects.create(
            nazwa='TestGmina'
        )
        self.obwod = Obwod.objects.create(
            nazwa='TestObwod', gmina=self.gmina, karty=10,
            wyborcy=10, aktualizacja=timezone.now()
        )
        self.selenium = webdriver.Firefox()
        self.selenium.maximize_window()
        super(SeleniumTests, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(SeleniumTests, self).tearDown()

    def test_edit_save(self):
        """
        Testing if values actually save
        """
        self.selenium.get(
            '%s%s%d' % (self.live_server_url, "/gminy/", self.gmina.pk)
        )
        editbtn = self.selenium.find_element_by_css_selector("button#edit" + str(self.obwod.pk))
        editbtn.click()
        editfield = self.selenium.find_element_by_css_selector("input#post_karty" + str(self.obwod.pk))
        editfield.clear()
        editfield.send_keys(1337)
        savebtn = self.selenium.find_element_by_css_selector("button#save" + str(self.obwod.pk))
        savebtn.click()
        wait = WebDriverWait(self.selenium, 10)

        self.assertEqual(Obwod.objects.get(pk=self.obwod.pk).karty, 1337)

    def test_simultanous_edit(self):
        """
        There should be an alert when there's a conflic in saving
        """
        driver2 = webdriver.Firefox()
        try:
            self.selenium.get(
                '%s%s%d' % (self.live_server_url, "/gminy/", self.gmina.pk)
            )
            editbtn = self.selenium.find_element_by_css_selector("button#edit" + str(self.obwod.pk))
            editbtn.click()
            editfield = self.selenium.find_element_by_css_selector("input#post_karty" + str(self.obwod.pk))
            editfield.send_keys(10)

            driver2.get(
                '%s%s%d' % (self.live_server_url, "/gminy/", self.gmina.pk)
            )
            editbtn2 = driver2.find_element_by_css_selector("button#edit" + str(self.obwod.pk))
            editbtn2.click()
            editfield2 = driver2.find_element_by_css_selector("input#post_karty" + str(self.obwod.pk))
            editfield2.send_keys(20)
            savebtn2 = driver2.find_element_by_css_selector("button#save" + str(self.obwod.pk))
            savebtn2.click()

            time.sleep(1)

            savebtn = self.selenium.find_element_by_css_selector("button#save" + str(self.obwod.pk))
            savebtn.click()

            wait = WebDriverWait(self.selenium, 10)
            wait.until(expected_conditions.alert_is_present())
            Alert(self.selenium).dismiss()

            elem = self.selenium.find_element_by_css_selector("span#karty" + str(self.obwod.pk))
            elem2 = driver2.find_element_by_css_selector("span#karty" + str(self.obwod.pk))

            self.assertEqual(elem.text, elem2.text)
        finally:
            driver2.quit()
