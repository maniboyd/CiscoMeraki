from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd



email=input('Please Enter your Email ID \t: ')
password=input('\nPlease Enter your Password to continue \t: ')
url='https://account.meraki.com/secure/login/dashboard_login'




#dashboard_name=''
def process(driver,dashboard_name):
    print(f'processing {dashboard_name}')
    input_text=driver.find_element_by_xpath('//*[@name="magicSearchQuery"]')
    input_text.send_keys(dashboard_name)
    time.sleep(2)
    driver.find_element_by_xpath(f'''//*[@class="magicSearchDropdownSection"]/div/ul/div/li/span[text()="{dashboard_name}"]''').click()
    input_text.send_keys(Keys.ENTER)

    #clicking Air Marshal element
    # air_marshal_url_cur=driver.current_url
    # if(air_marshal_url_cur.__contains__('/usage')):
    #     print(f'Current URL: {air_marshal_url_cur}')
    #     time.sleep(3)
    #     head, sep, tail = air_marshal_url_cur.partition('/usage')
    #     air_marshal_url=head+'/dashboard/air_marshal'
    #     print(f'AirMarshal:{air_marshal_url}')
    #     driver.get(air_marshal_url)
    # else:
    #     print(f'Current URL: {air_marshal_url_cur}')
    #     time.sleep(3)
    #     head, sep, tail = air_marshal_url_cur.partition('/manage')
    #     air_marshal_url=head+'/manage/dashboard/air_marshal'
    #     print(f'AirMarshal:{air_marshal_url}')
    #     driver.get(air_marshal_url)

    #Airmarshal method 2
    time.sleep(2)
    driver.find_element_by_xpath("(//*[text()='Wireless'])[1]/..").click()
    time.sleep(2)
    actions = ActionChains(driver) 
    actions.send_keys(Keys.TAB * 2)
    actions.send_keys(Keys.ENTER)
    actions.perform()
    



    # driver.find_element_by_xpath('//div[@class="menu-item currentTab"]/a').click()
    # driver.find_element_by_xpath('//*[@id="tab_menu_react"]/ul/li[2]/div[2]/ul[1]/li[2]/a/span').click()

    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '(//*[@class="RadioButton__hiddenInput"])[2]')))
    finally: 
        block_radio=driver.find_element_by_xpath('(//*[@class="RadioButton__hiddenInput"])[2]')
        select_check=str(block_radio.is_selected())

        if select_check=='False':
            driver.execute_script("$(arguments[0]).click();", block_radio)
            driver.find_element_by_xpath('//*[@class="SaveChanges__saveBtn btn btn-primary"]').click()
    #         try:
    #             element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '''('//*[@class="SaveChanges SaveChanges--unsavedChanges SaveChanges--floatingBottom"]/button[@type="submit"]''')))
    #         finally:
    #             driver.find_element_by_xpath('//*[@class="SaveChanges SaveChanges--unsavedChanges SaveChanges--floatingBottom"]/button[@type="submit"]').click()
            status= 'Blocked now'
        else:
            status='Already blocked'
        return status
    
def main():
    driver=webdriver.Chrome()
    driver.get(url)
    #login starts here
    driver.find_element_by_id('email').send_keys(email)
    driver.find_element_by_id('password').send_keys(password)
    driver.find_element_by_id('commit').click()
    #login ends here

    #waiting for 2 step authentication code starts here
    wait = WebDriverWait(driver, 30000)
    element = wait.until(EC.visibility_of_element_located((By.XPATH,"//*[(text()='')]")))
    print(element.text)
    #waiting for 2 step authentication code ends here

    #clicking on the org element
    time.sleep(2)
    driver.find_element_by_xpath("//*[(text()='')]").click()
    time.sleep(2)
    # element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@name="magicSearchQuery"]')))
    #clicking on ** element ends here

    network=pd.read_csv("Network.csv")
    values=network['Network Name'].values
    statuses=[]
    for value in values:
        statuses.append(process(driver,value))
    new_df=pd.DataFrame({'Device':values.tolist(),'Status':statuses})
    new_df.to_csv('output.csv')


if __name__=='__main__':
    main()
