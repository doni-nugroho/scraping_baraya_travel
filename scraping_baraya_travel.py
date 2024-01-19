from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
import csv
def scrap():
    link = "https://baraya-travel.com/carabayar"
    # user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36'
    options = webdriver.ChromeOptions()
    options.add_argument("--enable-javascript")
    options.add_argument("--headless")
    # options.add_argument(f'user-agent={user_agent}')
    
    # servis = Service("chromedriver.exe")
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1920, 1080)
    driver.get(link)
    time.sleep(2)
    
    listTipe = driver.find_elements(By.CSS_SELECTOR, "#accordion > .card")
    arr_metode=[]
    
    i = 0
    for itemkartu in listTipe:
        card_header = itemkartu.find_element(By.ID,'heading-'+str(i))
        title_tipe = card_header.find_element(By.TAG_NAME, "button").text
        # print(image)

        card_platforms = itemkartu.find_elements(By.CSS_SELECTOR,'#collapse-'+str(i)+' .card')
        # print(len(card_platforms))
        for card_platform in card_platforms:
            title_platform = card_platform.find_element(By.TAG_NAME, "button")
            image = card_platform.find_element(By.TAG_NAME, "img")
            body = card_platform.find_element(By.CLASS_NAME, "card-body")
            x=[]
            x.append(title_tipe)
            x.append(title_platform.get_attribute("innerHTML").strip())
            x.append(image.get_attribute("src"))
            x.append(body.find_element(By.TAG_NAME,'p').get_attribute("innerHTML").strip())
            x.append(body.find_element(By.TAG_NAME,'ol').get_attribute("innerHTML").strip())
            arr_metode.append(x)

            # Get the image from the URL
            response = requests.get(image.get_attribute("src"))

            # Open the image file for writing
            with open(image.get_attribute("src").split('/')[-1], "wb") as f:

                # Write the image data to the file
                f.write(response.content)
        i=i+1
           
    # print(arr_metode)

    column_names=["category","payment_gateway","image","title","conntent"]
    # Open CSV file for writing
    with open("metode_pembayaran.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        # Write column names
        writer.writerow(column_names)

        # Write data rows
        writer.writerows(arr_metode)
    print("Data exported to metode_pembayaran.csv successfully!")

scrap()