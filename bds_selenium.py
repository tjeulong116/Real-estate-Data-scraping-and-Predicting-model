from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import pandas as pd
import time

# Configure driver
website_0 = ""
path = ""
driver_0 = webdriver.Chrome(executable_path=path)
driver_0.maximize_window()
driver_0.get(website_0)

#Pagination
pagination = driver_0.find_element_by_xpath("//div[contains(@class, 're__pagination-group')]")
pages = pagination.find_elements_by_xpath("./a")
current_page = 1
last_page = int(pages[-2].text)
driver_0.quit()

link_list = []

try:
    while current_page <= last_page + 10:
        website = ""
        driver = webdriver.Chrome(executable_path=path)
        driver.maximize_window()
        driver.get(website)

        #Get data
        box = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "product-lists-web")))
        # box = driver.find_element_by_id("product-lists-web")
        products = WebDriverWait(box, 5).until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'js__card-full-web')]/a[@class='js__product-link-for-product-id']")))
        # products = box.find_elements_by_class_name("js__product-link-for-product-id")

        print(len(products))
        for product in products:
            product_id = product.get_attribute("data-product-id")
            title = product.get_attribute("title")
            sublink = product.get_attribute("href")
            link_list.append([product_id, title, sublink])

        driver.quit()
        print(f"Finish page {current_page}")
        current_page = current_page + 1
except Exception as e:
    print(e)
finally:
    df_link_list = pd.DataFrame(link_list, columns=["product_id", "title", "sublink"])
    print(len(df_link_list))
    df_link_list.drop_duplicates(subset="product_id", inplace=True)
    print(len(df_link_list))

    #sort by id //post_date
    df_link_list.sort_values(by="product_id", axis=0, ascending=True, inplace=True, na_position="first")

    #Output data
    time_now = datetime.now().strftime("%Y-%m-%d_%H-%m-%S")
    df_link_list.to_csv(path_or_buf=f"",
                        index=False)
    print("Finished scraping")



