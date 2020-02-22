from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import time
import re

def detail_page_open(browser,id):
    browser.execute_script("window.open()")
    new_window = browser.window_handles
    browser.switch_to.window(new_window[len(new_window)-1])
    browser.get(detail_page_url + id)
    time.sleep(5)

list_page_url = "https://content-tokyo2020.tems-system.com/eguide/jp/AI/list"
detail_page_url = "https://content-tokyo2020.tems-system.com/eguide/jp/AI/details?id="
path = "./ai_expo_list.txt"

browser = webdriver.Chrome(executable_path=r"C:\\App\\chromdriver\\chromedriver.exe")
browser.get(list_page_url)
time.sleep(5)

#val_ids = browser.find_element_by_id("val-id")
val_ids = browser.find_elements(By.CLASS_NAME,"details")

with open(path, mode='w', encoding="UTF-8") as f:
    f.write("企業名,出展ゾーン名,国・地域,出展カテゴリ,対応可能な業種,URL,共同出展社,PR,製品情報\n")
    #c = 0
    for id in val_ids:
        detail_page_open(browser, id.get_attribute("val-id"))
        conpany_name = browser.find_element_by_class_name("company_name").text
        table = browser.find_element_by_class_name("tblfix").find_elements(By.TAG_NAME,"td")
        out = ""
        count = 0
        
        for td in table:
            if len(table) == 6 and count == 5:
                out = out + ","
            text_mod = re.sub(",","，",td.text)
            text_mod = re.sub("\n"," ", text_mod)

            out = out + "," + text_mod
            count += 1
        
        table = browser.find_elements(By.CLASS_NAME, "tbl")
        product_table_td = table[2].find_elements(By.TAG_NAME, "td")

        out = out + ","
        for td in product_table_td:
            out = out + "/" + re.sub("\n", "/", re.sub(",", "，", td.text))

        f.write(re.sub(","," ",conpany_name) + out + "\n")
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
        # c+=1
        # if c==10:
        #     break
