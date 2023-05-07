from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import random
import math
import string
import requests
import tkinter as tk
from tkinter import filedialog
from functools import partial
import os
import asyncio
import signal
import re

file_path = None
validPage = False
chrome_options = Options()
driver = None
startingUrl = ""
pagenum = 1
pageButton = None
links = []
resultsList = []
huburl = ""
nextButton = None
items = 0
itemnum = 0
image_urls = []
pic_count = 0
imgnum = 0
images = []
image_titles = []
image_description = []
image_folder_directories = []
image_directories = []
folder_path = ""
startingPage = 1
onAPage = False
sellerName = ""
picLinks = []
def browse_file():
    global file_path
    file_path = filedialog.askdirectory()
    label.config(text=file_path)
    print(file_path)
def getResultsList():
    global resultsList
    global driver
    try:
        resultsList = driver.find_element(
            By.XPATH, "//ul[@class='srp-results srp-list clearfix']"
        )
    except Exception:
        resultsList = driver.find_element(
            By.XPATH, "//ul[@class='srp-results srp-grid clearfix']"
        )
def getItems(maxElement,directory):
    global items
    global itemnum
    global pic_count
    global images
    global driver
    global file_path
    global image_urls
    global image_folder_directories
    global image_directories
    global folder_path
    length = 10
    characters = string.ascii_letters + string.digits
    random_string_image = ""
    while items > itemnum:
        print(itemnum)
        buttons = maxElement.find_elements(
            By.TAG_NAME, "button"
        )
        for button in buttons:
            if "btn-next" in button.get_attribute("class"):
                button.click()
                images = driver.find_element(
                    By.XPATH,
                    "//div[@class='vim d-picture-panel-maxview']",
                ).find_elements(By.TAG_NAME, "img")
                itemnum = itemnum + 1
                for image in images:
                    if items == itemnum:
                        if "/s-l64.jpg" not in str(image.get_attribute("src")):
                            random_string_image = "".join(
                                random.choice(characters) for i in range(length)
                            )
                            image_directories.append(directory + random_string_image + "-" + driver.title.replace("?","")
                                    .replace("|", "")
                                    .replace("\\", "")
                                    .replace("/", "")
                                    .replace(":", "")
                                    .replace("<", "")
                                    .replace(">", "")
                                    .replace("*", "")
                                    .replace('"', "")
                                    .replace(" ", "") + ".jpg")
                            image_urls.append(image.get_attribute("src"))
                            print(directory + random_string_image + "-" + driver.title.replace("?", "")
                                  .replace("|", "")
                                  .replace("\\", "")
                                  .replace("/", "")
                                  .replace(":", "")
                                  .replace("<", "")
                                  .replace(">", "")
                                  .replace("*", "")
                                  .replace('"', "") + ".jpg")
                            print(image.get_attribute("src"))
def getImage(folder,href):
    global image_urls
    global image_directories
    length = 10
    characters = string.ascii_letters + string.digits
    random_string = "".join(
        random.choice(characters) for i in range(length)
    )
    image_directories.append(folder + random_string + "-" + driver.title.replace("?", "")
                             .replace("|", "")
                             .replace("\\", "")
                             .replace("/", "")
                             .replace(":", "")
                             .replace("<", "")
                             .replace(">", "")
                             .replace("*", "")
                             .replace('"', "")
                             .replace(" ", "") + ".jpg")
    image_urls.append(href)
async def itemTimer():
    global onAPage
    global huburl
    print("Timer started")
    time.sleep(30)
    print("The timer has ended")
    if onAPage:
        print("If item isn't finished, returning to main page")
        while driver.current_url != huburl:
            driver.get(huburl)
            onAPage = False
async def itemTimerRunFunction():
    task = asyncio.create_task(itemTimer())
    print("Code below the timer")
    print("End of code")
def getAllPicButtons():
    global nextButton
    global items
    global itemnum
    global driver
    global image_urls
    global image_directories
    global file_path
    global image_folder_directories
    global folder_path
    nextButton = None
    items = 0
    itemnum = 0
    original_link_clicked = False
    try:
        driver.get(driver.find_element(By.XPATH, "//span[@class='vi-inl-lnk vi-original-listing']").find_element(By.TAG_NAME, "a").get_attribute("href"))
    except Exception as e:
        print("")
        try:
            driver.get(driver.find_element(By.XPATH, "//span[@class='vi-inl-lnk vi-cvip-prel5']").find_element(By.TAG_NAME,
                                                                                                           "a").get_attribute(
            "href"))
        except Exception:
            print("")
            try:
                driver.get(
                    driver.find_element(By.XPATH, "//div[@class='ux-image-carousel']").find_element(By.TAG_NAME,
                                                                                                            "a").get_attribute(
                        "href"))
            except Exception:
                print("")
    """
    try:
        driver.get(driver.find_element(By.XPATH, "//span[@class='vi-inl-lnk vi-cvip-prel5']").find_element(By.TAG_NAME, "a").get_attribute("href"))
    except Exception as e:
        print("")
    """
    element = None
    try:
        element = driver.find_element(By.XPATH, "//a[@class='vi-image-gallery__enlarge-link']")
    except Exception as e:
        print("")
        element = None
    if element != None:
        try:
            driver.find_element(By.XPATH, "//a[@class='vi-image-gallery__enlarge-link']").click()
            #driver.back()
        except Exception as e:
            print("Couldn't click and stuck")
            #driver.back()
    else:
        try:
            driver.find_element(By.XPATH, "//div[@class='ux-image-carousel']").click()
        except Exception:
            print("")
        try:
            driver.get(driver.find_element(By.XPATH, "//div[@class='nodestar-item-card-details__image-table']").find_element(By.TAG_NAME, "a").get_attribute("href"))
        except Exception:
            print("")
        print(driver.find_elements(By.TAG_NAME, "img"))
        print(len(driver.find_elements(By.XPATH, "//button[@class='ux-image-filmstrip-carousel-item image']")))
        if len(driver.find_elements(By.XPATH, "//button[@class='ux-image-filmstrip-carousel-item image']")) == 0:
            print()
        else:
            for i, button in enumerate(driver.find_elements(By.XPATH, "//button[@class='ux-image-filmstrip-carousel-item image']")):
                print("Index: " + str(i))
                print("Length: " + str(len(driver.find_elements(By.XPATH, "//button[@class='ux-image-filmstrip-carousel-item image']"))-1))
                try:
                    button.click()
                except Exception:
                    print("Failed to click button")
                if i == len(driver.find_elements(By.XPATH, "//button[@class='ux-image-filmstrip-carousel-item image']"))-1:
                    for img, image in enumerate(driver.find_elements(By.TAG_NAME, "img")):
                        try:
                            if "s-l1600.jpg" in image.get_attribute("src"):
                                print(image.get_attribute("src"))
                                try:
                                    print("")
                                    getImage(folder_path, image.get_attribute("src"))
                                    print("")
                                except Exception as e:
                                    print("")
                        except Exception:
                            print("")
                        try:
                            if "s-l1600.png" in image.get_attribute("src"):
                                print(image.get_attribute("src"))
                                try:
                                    getImage(folder_path, image.get_attribute("src"))
                                except Exception:
                                    print("")
                        except Exception:
                            print()
                        try:
                            if "s-l1600.jpeg" in image.get_attribute("src"):
                                print(image.get_attribute("src"))
                                try:
                                    getImage(folder_path, image.get_attribute("src"))
                                except Exception:
                                    print("")
                        except Exception:
                            print()
                        try:
                            if "s-l300.jpg" in image.get_attribute("src"):
                                print(image.get_attribute("src"))
                                try:
                                    getImage(folder_path, image.get_attribute("src"))
                                except Exception:
                                    print("")
                        except Exception:
                            print()
                        try:
                            if "s-l300.jpeg" in image.get_attribute("src"):
                                print(image.get_attribute("src"))
                                try:
                                    getImage(folder_path, image.get_attribute("src"))
                                except Exception:
                                    print("")
                        except Exception:
                            print()
                        try:
                            if "s-l300.png" in image.get_attribute("src"):
                                print(image.get_attribute("src"))
                                try:
                                    getImage(folder_path, image.get_attribute("src"))
                                except Exception:
                                    print("")
                        except Exception:
                            print()
    try:
        print(driver.find_element(By.XPATH, "//img[@loading='lazy']").get_attribute("src"))
        getImage(folder_path, driver.find_element(By.XPATH, "//img[@loading='lazy']").get_attribute("src"))
    except Exception as e:
        print("Failed: " + "")
def timeout_handler(signum, frame):
    raise TimeoutException()
def navigateToLink(link):
    global driver
    global image_titles
    global image_description
    global folder_path
    global huburl
    global onAPage
    global sellerName
    original_nav = False
    driver.get(link)
    onAPage = True
    print("")
    paragraphs = []
    length = 10
    characters = string.ascii_letters + string.digits
    random_string = "".join(
        random.choice(characters) for i in range(length)
    )
    sellerElement = None
    try:
        sellerElement = driver.find_element(By.XPATH, '//span[@class="mbg-nw"]')
    except Exception:
        print()
    pageSeller = ""
    try:
        pageSeller = sellerElement.text
    except Exception:
        print()
    if sellerName == pageSeller or sellerName == "":
        folder_path = (file_path + "/" + driver.title.replace("?", "")
                   .replace("|", "")
                   .replace("\\", "")
                   .replace("/", "")
                   .replace(":", "")
                   .replace("<", "")
                   .replace(">", "")
                   .replace("*", "")
                   .replace('"', "") + "-folder-" + random_string + "/")
        image_folder_directories.append(folder_path)
        image_titles.append(driver.title)
        print(driver.title)
        print(folder_path)
        paragraph = []
        paragraphsHtml = []
        try:
            driver.refresh()
            driver.get(driver.find_element(By.ID,"desc_ifr").get_attribute("src"))
            try:
                paragraphsHtml = driver.find_element(By.TAG_NAME,"body").get_attribute("innerHTML")
                image_description.append(paragraphsHtml)
            except Exception:
                print("Paragraphs not found")
            driver.back()
        except Exception:
            print("Description not found")
            paragraphsHtml = ["<p> No description found for this item </p>"]
            image_description.append(paragraphsHtml)
        print("Gonna run pics now")
        getAllPicButtons()
        driver.back()
    while driver.current_url != huburl:
        driver.get(huburl)
        onAPage = False
    print("Made it back")

def LinkLoop():
    global picLinks
    global folder_path
    global pagenum
    picLinks = list(set(picLinks))
    picLinkCount = 0
    label6.config(text=str(picLinkCount) + " of " + str(len(picLinks)) + " items scanned on page " + str(pagenum),
                  fg="green")
    label6.pack()
    window.update()
    for link in picLinks:
        navigateToLink(link)
        picLinkCount = picLinkCount + 1
        label6.config(text=str(picLinkCount) + " of " + str(len(picLinks)) + " items scanned on page " + str(pagenum), fg="green")
        label6.pack()
        window.update()
    label6.forget()
    window.update()
def getLinks():
    global links
    global picLinks
    global resultsList
    links = list(set(resultsList.find_elements(By.TAG_NAME, "a")))
    for link in links:
        if (
                "#UserReviews" not in link.get_attribute("href")
                and "WatchListAdd?" not in link.get_attribute("href")
                and "index.html" not in link.get_attribute("href")
                and "TitleDesc=0&" not in link.get_attribute("href")
                and "search.srp.node" not in link.get_attribute("href")
                and "sch" not in link.get_attribute("href")
                and "SellLikeItem" not in link.get_attribute("href")
        ):
            picLinks.append(link.get_attribute("href"))
def ScrollDown():
    global new_height
    global last_height
    global driver
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
def searchPage():
    global huburl
    global links
    global resultsList
    global driver
    global image_urls
    global image_description
    global image_folder_directories
    global image_titles
    global image_directories
    global folder_path
    global picLinks
    huburl = driver.current_url
    ScrollDown()
    getResultsList()
    getLinks()
    LinkLoop()
    for i, title in enumerate(image_titles):
        try:
            os.makedirs(image_folder_directories[i])
        except Exception:
            print("Failed to create folder or folder already exists.")
        try:
            with open(image_folder_directories[i] + title.replace("?", "")
                    .replace("|", "")
                    .replace("\\", "")
                    .replace("/", "")
                    .replace(":", "")
                    .replace("<", "")
                    .replace(">", "")
                    .replace("*", "")
                    .replace('"', "") + ".html", "w", encoding="utf-8") as f:
                f.write(str(image_description[i]) + "\n")
        except Exception:
            print("Failed to create description file")
    label5.pack()
    label5.config(text="", fg="green")
    window.update()
    print(len(image_urls))
    for i, image in enumerate(image_urls):
        print("File directory: " + image_directories[i])
        try:
            response = requests.get(image)
            with open(image_directories[i], "wb") as f:
                f.write(response.content)
            label5.config(text="Copied " + str(i + 1) + " of " + str(len(image_urls)) + " images.", fg="green")
            window.update()
        except Exception:
            print("Cannot create file or file already exists")
    label5.forget()
    window.update()
    image_titles = []
    image_description = []
    image_urls = []
    image_directories = []
    image_folder_directories = []
def getPageButton():
    global pagenum
    global pageButton
    try:
        pageButton = driver.find_element(
            By.XPATH,
            "//a[@class='pagination__item' and text()='" + str(pagenum) + "']",
        )
    except Exception:
        pageButton = "SinglePage"
def PageLoop():
    global pageButton
    global pagenum
    global driver
    global resultsList
    global folder_path
    global huburl
    global picLinks
    ScrollDown()
    getPageButton()
    while pageButton or pageButton == "SinglePage":
        resultsList = []
        try:
            if pagenum >= int(startingPage.get()):
                try:
                    if pagenum <= int(endingPage.get()):
                        searchPage()
                except Exception:
                    print("No ending page.")
                    searchPage()
        except Exception:
            print("No page number found.")
            searchPage()
        pagenum = pagenum + 1
        try:
            pageButton = driver.find_element(
                By.XPATH,
                "//a[@class='pagination__item' and text()='" + str(pagenum) + "']",
            )
        except Exception:
            print("Error: couldn't get that")
            pageButton = None
        try:
            driver.get(pageButton.get_attribute("href"))
            huburl = driver.current_url
        except Exception:
            print("Error: couldn't go there")
            break
def handleHoodedChildAtStart():
    global startingUrl
    global driver
    global validPage
    global huburl
    global last_height
    global resultsList
    global picLinks
    global pageButton
    while not validPage:
        validPage = True
        try:
            huburl = startingUrl
            last_height = driver.execute_script("return document.body.scrollHeight")
            try:
                resultsList = driver.find_element(
                    By.XPATH, "//ul[@class='srp-results srp-list clearfix']"
                )
            except Exception:
                resultsList = driver.find_element(
                    By.XPATH, "//ul[@class='srp-results srp-grid clearfix']"
                )
            picLinks = []
            pageButton = None
        except Exception:
            print("Hooded child. Refreshing...")
            driver.get("https://www.ebay.com/")
            driver.get(startingUrl)
            driver.refresh()
            validPage = False
def commence_search():
    global startingUrl
    global chrome_options
    global driver
    global pagenum
    global url
    global file_path
    global folder_path
    global sellerName
    global picLinks
    print("Collecting images from search results, please wait...")
    pagenum = 1
    print("Folder: " + file_path)
    print("URL: " + url.get())
    chrome_options = Options()
    #pchrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    startingUrl = url.get()
    driver.get(startingUrl)
    handleHoodedChildAtStart()
    try:
        element = driver.find_element(By.XPATH,'//div[@class="str-seller-card__store-name"]')
        sellerName = element.text
    except Exception:
        print()
    PageLoop()
    driver.close()
def validate_fields():
    global folder_path
    global picLinks
    if (
            file_path is None
            or file_path == ""
    ):
        print("No path")
    if (
            url.get() is None
            or url.get() == ""
    ):
        print("No url")
    if (
            file_path is not None
            and file_path != ""
            and url.get() is not None
            and url.get() != ""
    ):
        print("Valid")
        commence_search()
def collect_photos():
    global folder_path
    global picLinks
    validate_fields()

window = tk.Tk()

window.title("Della Scraper")

window.geometry("700x500")
try:
    img = tk.PhotoImage(file="DellaScraperIcon.png")
    window.iconphoto(False, img)
except Exception:
    print("File not found")

label = tk.Label(window, text="Destination Folder", font=("Arial", 16))
label.pack(pady=20)
folder = tk.Button(window, text="Select", command=browse_file)
folder.pack()
label3 = tk.Label(
    window,
    text="Make sure to select a destination folder for the files to go into",
    font=("Arial", 12),
    fg="red",
)
label3.pack_forget()
label2 = tk.Label(window, text="Ebay URL", font=("Arial", 16))
label2.pack(pady=20)
label4 = tk.Label(
    window, text="Make sure to input a ebay url", font=("Arial", 12), fg="red"
)
label4.pack_forget()
label5 = tk.Label(window, text="Found # images in total", font=("Arial", 12), fg="red")
label5.pack_forget()
label6 = tk.Label(
    window, text="Saved # out of # images to dest", font=("Arial", 12), fg="red"
)
label6.pack_forget()
url = tk.Entry(window, highlightthickness=2, highlightbackground="black", width=50)
url.pack()
pageLabel = tk.Label(
    window, text="Starting page", font=("Arial", 12)
)
pageLabel.pack()
startingPage = tk.Entry(window, highlightthickness=2, highlightbackground="black", width=15)
startingPage.pack()
endPageLabel = tk.Label(
    window, text="Ending page", font=("Arial", 12)
)
endPageLabel.pack()
endingPage = tk.Entry(window, highlightthickness=2, highlightbackground="black", width=15)
endingPage.pack()
button = tk.Button(window, text="Start!", font=("Arial", 14))
button["command"] = partial(collect_photos)
button.pack(pady=10)

window.mainloop()
