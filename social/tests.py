from django.test import TestCase, Client
from .models import User, Post, Comment, Friendship
from selenium import webdriver
import pathlib
import os
from selenium.webdriver.common.keys import Keys


# Create your tests here.

# setting up for selenium
def file_uri(filename):
    return pathlib.Path(os.path.abspath(filename)).as_uri()



class ModelTestCase(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(username='test_user', email='test@gmail.com',  password='1234')
        test_user.save()
        post = Post(pk= 0, text='1234', author=test_user)
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
    
    def test_profile(self):
        '''
        Test if you can't reach to profile when not logged in
        '''
        c = Client()
        
        response = c.get('/profile')
        self.assertEqual(response.status_code, 302)
 
    
class BrowserTestCase(TestCase):
    def test_login_selenium(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://127.0.0.1:8000/')
        self.driver.find_element_by_id('login_username').send_keys('dummyuser')
        self.driver.find_element_by_id('login_password').send_keys('dummy_password' + Keys.ENTER)    
        self.assertEqual(self.driver.title, 'DBSF | Home')



