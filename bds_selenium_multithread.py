import pandas as pd
from numpy import nan
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor
import time
from tqdm import tqdm

#Configure setting
path = ""

df_links = pd.read_csv(filepath_or_buffer="", header=0)
links_list = df_links.values.tolist()

result = []

def get_a_page(links: list):
    driver_sub = None
    try:
        product_id = str(links[0])
        title = links[1]
        sublink = links[2]

        driver_sub = webdriver.Chrome(executable_path=path)
        driver_sub.maximize_window()
        driver_sub.get(sublink)

        #Get detailed data
        box_sub = WebDriverWait(driver_sub, 10).until(EC.presence_of_element_located((By.ID, "product-detail-web")))
        # box_sub = driver_sub.find_element_by_id("product-detail-web")

        if title is nan:
            title = WebDriverWait(box_sub, 10).until(EC.presence_of_element_located((By.XPATH, "./h1[contains(@class, 'pr-title')]"))).text

        price_per_m2 = ""
        isVerified = False

        try:
            price_per_m2 = WebDriverWait(box_sub, 5).until(EC.presence_of_element_located((By.XPATH, "//span[@class='ext']"))).text
        except:
            print("Not has price_per_m2")

        try:
            WebDriverWait(box_sub, 2).until(EC.presence_of_element_located((By.XPATH, "//i[contains(@class, 'verified-info-click')]")))
            isVerified = True
        except:
            pass

        new_address = box_sub.find_element_by_class_name("re__address-line-1").text
        old_address = box_sub.find_element_by_class_name("re__address-line-2").text
        description = box_sub.find_element_by_xpath(".//div[contains(@class, 're__detail-content')]").text

        price_range = ""
        area = ""
        number_of_bedrooms = ""
        number_of_bathrooms = ""
        number_of_stories = ""
        house_orientation = ""
        balcony_orientation = ""
        front_length = ""
        entrance_road_length = ""
        legal_status = ""
        isFurnished = ""

        detail_items = WebDriverWait(box_sub, 10).until(EC.presence_of_all_elements_located((By.XPATH, ".//div[contains(@class, 'specs-content-item')]")))
        #detail_items = box_sub.find_elements_by_xpath(".//div[contains(@class, 'specs-content-item')]")
        for item in detail_items:
            item_title = item.find_element_by_xpath("./span[contains(@class, 'item-title')]").text
            item_value = item.find_element_by_xpath("./span[contains(@class, 'item-value')]").text

            match item_title:
                case "Khoảng giá":
                    price_range = item_value
                case "Diện tích":
                    area = item_value
                case "Số phòng ngủ":
                    number_of_bedrooms = item_value
                case "Số phòng tắm, vệ sinh":
                    number_of_bathrooms = item_value
                case "Số tầng":
                    number_of_stories = item_value
                case "Hướng nhà":
                    house_orientation = item_value
                case "Hướng ban công":
                    balcony_orientation = item_value
                case "Mặt tiền":
                    front_length = item_value
                case "Đường vào":
                    entrance_road_length = item_value
                case "Pháp lý":
                    legal_status = item_value
                case "Nội thất":
                    isFurnished = item_value
                case _:
                    print("Unknow detailed item")
                    print(sublink)

        short_detail_items = WebDriverWait(box_sub, 10).until(EC.presence_of_all_elements_located((By.XPATH, ".//div[contains(@class, 'js__pr-config-item')]")))
        # short_detail_items = box_sub.find_elements_by_xpath(".//div[contains(@class, 'js__pr-config-item')]")
        post_date = short_detail_items[0].find_element_by_class_name("value").text
        expire_date = short_detail_items[1].find_element_by_class_name("value").text
        post_type = short_detail_items[2].find_element_by_class_name("value").text
        post_id = short_detail_items[3].find_element_by_class_name("value").text
        if post_id != product_id:
            print("Id not match")

        tmp_res_list = [product_id, title, price_range, area, price_per_m2, number_of_bedrooms, number_of_bathrooms,
                             number_of_stories, house_orientation, balcony_orientation, front_length, entrance_road_length,
                             legal_status, isFurnished, new_address, old_address, post_date, expire_date, post_type,
                             isVerified, description, sublink]
        print(tmp_res_list)
        print("---")
        driver_sub.quit()

        return tmp_res_list
    except Exception as e:
        print(e)
    finally:
        if driver_sub:
            driver_sub.quit()

# Start multithread
first_point = 0
last_point = 0


try:
    with ThreadPoolExecutor(max_workers=7) as exe:
        result = list(tqdm(exe.map(get_a_page, links_list), total=len(links_list)))
except Exception as e:
    print(e)
finally:
    #Output to csv
    result = [item for item in result if item is not None]

    df_csv = pd.DataFrame(result, columns=["product_id", "title", "price_range", "area", "price_per_m2", "number_of_bedrooms", "number_of_bathrooms",
        "number_of_stories", "house_orientation", "balcony_orientation", "front_length", "entrance_road_length",
        "legal_status", "isFurnished", "new_address", "old_address", "post_date", "expire_date", "post_type",
        "isVerified", "description", "sublink"])
    df_csv.to_csv(path_or_buf="", index=False)