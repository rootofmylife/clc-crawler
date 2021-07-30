from selenium import webdriver
import time

opts = webdriver.FirefoxOptions()
opts.headless = True

driver = webdriver.Firefox(options=opts)
driver.get("https://batdongsan.com.vn/nha-dat-ban")
time.sleep(2)

links = driver.find_elements_by_css_selector('.wrap-plink')
titles = [el.get_attribute("href") for el in links]
print(titles)

driver.close()