import time
from selenium import webdriver  # 从selenium引入webdriver
import unittest
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from selenium.common.exceptions import WebDriverException
MAX_WAIT=10 
class NewVisitorTest(LiveServerTestCase):  # 把测试写成类，它继承unittest.TestCase
  def setUp(self):  # setUp: 每次测试之前运行的特殊方法，用来启动浏览器
    self.browser = webdriver.Firefox()  # 启动一个selenium webdriver去弹出一个firefox窗口

  def tearDown(self):  # tearDown: 测试之后运行的特殊方法，用来停止浏览器
    self.browser.quit()

    
  def wait_for_row_in_list_table(self,row_text):
        start_time=time.time()
        while True:
              try:
                table=self.browser.find_element_by_id('id_list_table')
                rows=table.find_elements_by_tag_name('tr')
                self.assertIn(row_text,[row.text for row in rows])
                return
              except(AssertionError,WebDriverException)as e:
                if time.time() - start_time>MAX_WAIT:
                      raise e
                time.sleep(0.5)
        
    # table=self.browser.find_element_by_id('id_list_table')
    # rows=table.find_elements_by_tag_name('tr')
    # self.assertIn(row_text,[row.text for row in rows])
      


  def test_can_start_a_list_for_one_user(self):  # 测试的主体是一个名为test_can_start_a_list_and_retrieve_it_later的方法
    # Edith has heard about a cool new online to-do app.
    # She goes to check out its homepage
    self.browser.get(self.live_server_url)  # 用它打开本地网页

    # She notices the page title and header mention to-do lists
    self.assertIn('To-Do', self.browser.title)  # 使用self.assertIn代替断言
    # self.fail('Finish the test!')  # self.fail无论如何都会失败，产生错误信息，此处用于作为完成测试的提醒
    header_text = self.browser.find_element_by_tag_name('h1').text
    self.assertIn('To-Do', header_text)

    # She is invited to enter a to-do item straight away
    inputbox = self.browser.find_element_by_id('id_new_item')
    self.assertEqual(
      inputbox.get_attribute('placeholder'),
      'Enter a to-do item'
    )

    # She types "Buy peacock feathers" into a text box
    # (Edith's hobby is tying fly-fishing lures)
    inputbox.send_keys('Buy peacock feathers')

    # When she hits enter, the page updates, and now the page lists
    # "1: But peacock feathers" as an item in a to-do list
    inputbox.send_keys(Keys.ENTER)
    self.wait_for_row_in_list_table('1:Buy peacock feathers')
    
    # self.assertIn('1:Buy peacock feathers', [row.text for row in rows])
    # self.assertIn('2:Use peacock feathers to make a fly', [row.text for row in rows])

    # There is still a text box inciting her to add another item.
    # She enters "Use peacock feathers to make a fly" (Edith is very methodical)
    inputbox=self.browser.find_element_by_id('id_new_item')
    inputbox.send_keys('Use peacock feathers to make a fly')
    inputbox.send_keys(Keys.ENTER)
    

    # The page updates again, and now shows both items on her list
    self.wait_for_row_in_list_table('1:Buy peacock feathers')
    self.wait_for_row_in_list_table('2:Use peacock feathers to make a fly')
    # self.fail('Finish test')

    # Edith wonders whether the site will remember her list.
    # Then she sees that the site has generated a unique URL for her
    # -- there is some explanatory text to that effect

    # She visits that URL - her to-do list is still there.

    # Satisfied, she goes back to sleep

  def test_multiple_users_can_start_lists_at_different_urls(self):
        self.browser.get(self.live_server_url)
        inputbox=self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1:Buy peacock feathers')
        #She notices that her list has a unique URl
        edith_list_url=self.browser.current_url
        self.assertRegex(edith_list_url,'/list/.+')

        #Now a new user , Francis , comes aloneg to the site
        ##We use a new browser session to make sure that no info
        ##of Edith 's is coming through from cookies etc

        self.browser.quit()
        self.browser=webdriver.Firefox()
        #Francis visit the home page .There is no sign of Edith's
        #list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)


        #Francis starts a nwe list by entering a new item . He
        #is less interesting than Edith
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
       #Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)
        #Again,there is no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)
        #Satisfied, they both go back to sleep

      
      

# if __name__ == '__main__':  # python模拟的程序入口，调用unittest.main方法，它启动unittest测试运行器，将自动在文件中寻找测试类和方法并运行它们
#   unittest.main(warnings='ignore')  # warning='ignore'防止在撰写本文时爆出多余的ResourceWarning信息
