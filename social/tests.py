from django.test import TestCase, Client
from .models import User, Post, Comment, Friendship
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import pathlib
import os
from selenium.webdriver.common.keys import Keys
import json


# Create your tests here.

# setting up for selenium
def file_uri(filename):
    return pathlib.Path(os.path.abspath(filename)).as_uri()



class ModelTestCase(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(username='test_user', email='test@gmail.com',  password='1234')
        test_user.save()
        post = Post(text='1234', author=test_user)
        post.save()

    def test_user(self):
        '''
        This is dummy test to see if testing can create a database

        '''
        user = User.objects.get(username='test_user')
        self.assertEqual(user.username, 'test_user')

    def test_index(self):
        '''
        This will test if the index page loads
        '''
        c = Client()
        response = c.get('/index')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        '''
        This will test the login function
        '''
        c = Client()
        login = c.login(username='test_user', password='1234')
        self.assertTrue(login)

    def test_fail_login(self):
        '''
        Login with wrong username
        '''
        c = Client()
        login = c.login(username='test_usern', password='12345')

        self.assertFalse(login)

    def test_get_posts(self):
        '''
        Testing if the post XML request answers with 200

        ''' 
        c = Client()
        login = c.login(username='test_user', password='1234')
        self.assertTrue(login)
        response = c.get('/get_posts')
        self.assertEqual(response.status_code, 200)

    def test_get_friends(self):
        '''
        Test if the the friend list will show up
        '''       
        c = Client()
        c.login(username='test_user', password='1234')
        response = c.get('/get_friends')
        self.assertEqual(response.status_code, 200)

    def test_profile(self):
        '''
        Test if you can reach to profile when logged in
        '''
        c = Client()
        c.login(username='test_user', password='1234')
        response = c.get('/profile')
        self.assertEqual(response.status_code, 200)
    
    def test_not_profile(self):
        '''
        Test if you can't reach to profile when not logged in
        '''
        c = Client()
        
        response = c.get('/profile')
        self.assertEqual(response.status_code, 302)

    def test_comments(self):
        '''
        Test if comments are loading
        '''
        c = Client()
        post = Post.objects.get(text='1234')
        c.login(username='test_user', password='1234')
        data = {"post_id": post.id, "text": "1234", "commentator": "test_user"}
        response = c.post("/comment", data, content_type='application/json;charset=UTF-8')
        self.assertEqual(response.status_code, 200)
 
    
class BrowserTestCase(TestCase):
    def test_login_selenium(self):
        # for later username dummyuser2 password dummypassword2
        self.driver = webdriver.Chrome()
        self.driver.get('http://127.0.0.1:8000/')
        self.driver.find_element_by_id('login_username').send_keys('dummyuser')
        self.driver.find_element_by_id('login_password').send_keys('dummy_password' + Keys.ENTER)
        self.driver.implicitly_wait(3)

        # create a new post
        self.driver.find_element_by_id('new_post_text').send_keys('This is a test post')
        self.driver.find_element_by_id('post_new_post_button').click()
        self.driver.implicitly_wait(3)  
       
        # check if the post was created
        self.assertTrue(self.driver.find_element_by_class_name('post'))

        # like and dislike post
        self.driver.find_element_by_class_name('like').click()
        self.driver.find_element_by_class_name('dislike').click()
        
        self.driver.find_element_by_class_name('comment_input').send_keys('This is a comment')
        self.driver.find_element_by_class_name('submit_comment').click()

        # check if comment exists and if the text shows up correctly
        self.driver.implicitly_wait(3) 
        self.assertEqual(self.driver.find_element_by_class_name('comment_text').get_attribute('innerHTML'), 'This is a comment')

        # delete post
        self.driver.find_element_by_class_name('delete_post_button').click()
        self.assertEqual(self.driver.title, 'DBSF | Home')


    # test the friendship functionality
    def test_friendship(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://127.0.0.1:8000/')
        self.driver.find_element_by_id('login_username').send_keys('dummyuser')
        self.driver.find_element_by_id('login_password').send_keys('dummy_password' + Keys.ENTER)
        self.driver.find_element_by_id('search_input').send_keys('dummyuser2' + Keys.ENTER)
        self.driver.find_element_by_link_text('dummyuser2').click()
        self.driver.find_element_by_id('friend_request_button').click()
        self.driver.find_element_by_class_name('logout_a').click()
        self.driver.find_element_by_id('login_username').send_keys('dummyuser2')
        self.driver.find_element_by_id('login_password').send_keys('dummypassword2' + Keys.ENTER)
        self.driver.implicitly_wait(3)
        self.driver.find_element_by_class_name('accept_request_button').click()
        self.driver.refresh()
        self.driver.find_element_by_link_text('dummyuser').click()
        self.driver.find_element_by_id("friend_request_button").click()
        WebDriverWait(self.driver, 10).until(EC.alert_is_present(), 'waited too long')
        alert = self.driver.switch_to.alert
        alert.accept()
        self.assertEqual(self.driver.find_element_by_id("friend_request_button").get_attribute('innerHTML') , '<i class="fa fa-user-plus"> Add</i>')

