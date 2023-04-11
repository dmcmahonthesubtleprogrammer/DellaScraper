from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import random
import string
import requests
import tkinter as tk
from tkinter import filedialog
from functools import partial
import os
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
        print("Failed: " + str(e))
    try:
        driver.get(driver.find_element(By.XPATH, "//span[@class='vi-inl-lnk vi-cvip-prel5']").find_element(By.TAG_NAME, "a").get_attribute("href"))
    except Exception as e:
        print("Failed: " + str(e))
    element = None
    try:
        element = driver.find_element(By.XPATH, "//a[@class='vi-image-gallery__enlarge-link']")
    except Exception as e:
        print("Failed: " + str(e))
        element = None
    if element != None:
        try:
            driver.find_element(By.XPATH, "//a[@class='vi-image-gallery__enlarge-link']").click()
        except Exception as e:
            print("Failed: " + str(e))
    else:
        try:
            driver.find_element(By.XPATH, "//div[@class='ux-image-carousel']").click()
        except Exception:
            print("Failed carousel")
        try:
            driver.get(driver.find_element(By.XPATH, "//div[@class='nodestar-item-card-details__image-table']").find_element(By.TAG_NAME, "a").get_attribute("href"))
        except Exception:
            print("Failed href")
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
                                    getImage(folder_path, image.get_attribute("src"))
                                except Exception as e:
                                    print(e)
                        except Exception:
                            print()
                        try:
                            if "s-l1600.png" in image.get_attribute("src"):
                                print(image.get_attribute("src"))
                                try:
                                    getImage(folder_path, image.get_attribute("src"))
                                except Exception:
                                    print(e)
                        except Exception:
                            print()
                        try:
                            if "s-l1600.jpeg" in image.get_attribute("src"):
                                print(image.get_attribute("src"))
                                try:
                                    getImage(folder_path, image.get_attribute("src"))
                                except Exception:
                                    print(e)
                        except Exception:
                            print()
                        try:
                            if "s-l300.jpg" in image.get_attribute("src"):
                                print(image.get_attribute("src"))
                                try:
                                    getImage(folder_path, image.get_attribute("src"))
                                except Exception:
                                    print(e)
                        except Exception:
                            print()
                        try:
                            if "s-l300.jpeg" in image.get_attribute("src"):
                                print(image.get_attribute("src"))
                                try:
                                    getImage(folder_path, image.get_attribute("src"))
                                except Exception:
                                    print(e)
                        except Exception:
                            print()
                        try:
                            if "s-l300.png" in image.get_attribute("src"):
                                print(image.get_attribute("src"))
                                try:
                                    getImage(folder_path, image.get_attribute("src"))
                                except Exception:
                                    print(e)
                        except Exception:
                            print()
    try:
        print(driver.find_element(By.XPATH, "//img[@loading='lazy']").get_attribute("src"))
        getImage(folder_path, driver.find_element(By.XPATH, "//img[@loading='lazy']").get_attribute("src"))
    except Exception as e:
        print("Failed: " + str(e))
def navigateToLink(link):
    global driver
    global image_titles
    global image_description
    global folder_path
    global huburl
    original_nav = False
    driver.get(link)
    print("")
    paragraphs = []
    length = 10
    characters = string.ascii_letters + string.digits
    random_string = "".join(
        random.choice(characters) for i in range(length)
    )
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
        print("Made it past the try block")
        iframe = driver.find_element(By.ID,"desc_ifr").get_attribute("src")
        driver.refresh()
        driver.get(iframe)
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
    ScrollDown()
    getPageButton()
    while pageButton or pageButton == "SinglePage":
        resultsList = []
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
    print("Collecting images from search results, please wait...")
    pagenum = 1
    print("Folder: " + file_path)
    print("URL: " + url.get())
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)
    startingUrl = url.get()
    driver.get(startingUrl)
    handleHoodedChildAtStart()
    PageLoop()
    driver.close()
def validate_fields():
    global folder_path
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
    validate_fields()

"""
def executeScan():
    global label6
    label3.pack_forget()
    label4.pack_forget()
    window.update()
    if (
        file_path is not None
        and file_path != ""
        and url.get() is not None
        and url.get() != ""
    ):
        label6.config(
            text="Collecting images from search results, please wait...", fg="green"
        )
        label6.pack(pady=20)
        window.update()
        pagenum = 1
        print("Folder: " + file_path)
        print("URL: " + url.get())
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        startingUrl = url.get()
        driver.get(startingUrl)
        validPage = False
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
        try:
            pageButton = driver.find_element(
                By.XPATH,
                "//a[@class='pagination__item' and text()='" + str(pagenum) + "']",
            )
        except Exception:
            pageButton = "SinglePage"
        item_titles = []
        item_folders = []
        item_description_folders = []
        item_description = []
        item_description_titles = []
        image_urls = []
        image_titles = []
        link_count = 0
        items = 0
        itemnum = 0
        while pageButton or pageButton == "SinglePage":
            print(
                "<==========================================================================================> "
            )
            print("New Page =============================> " + str(pagenum))
            print(
                "<==========================================================================================> "
            )
            huburl = driver.current_url
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            resultsList = []
            links = []
            try:
                resultsList = driver.find_element(
                    By.XPATH, "//ul[@class='srp-results srp-list clearfix']"
                )
            except Exception:
                resultsList = driver.find_element(
                    By.XPATH, "//ul[@class='srp-results srp-grid clearfix']"
                )
            links = list(set(resultsList.find_elements(By.TAG_NAME, "a")))
            for link in links:
                if (
                    "#UserReviews" not in link.get_attribute("href")
                    and "WatchListAdd?" not in link.get_attribute("href")
                    and "index.html" not in link.get_attribute("href")
                    and "TitleDesc=0&" not in link.get_attribute("href")
                    and "search.srp.node" not in link.get_attribute("href")
                ):
                    picLinks.append(link.get_attribute("href"))
            link_count = 0
            picLinks = list(set(picLinks))
            for link in picLinks:
                link_count = link_count + 1
                print(
                    "Item "
                    + str(link_count)
                    + " out of "
                    + str(len(picLinks))
                    + " is currently being scanned..."
                )
                driver.get(link)
                length = 10
                characters = string.ascii_letters + string.digits
                random_string = "".join(
                    random.choice(characters) for i in range(length)
                )
                nextButton = None
                items = 0
                itemnum = 0
                try:
                    triggermask = driver.find_element(
                        By.XPATH, "//div[@class='ux-image-carousel']"
                    )
                    triggermask.click()
                except Exception:
                    print("couldn't find a triggermask")
                maxview_elements = driver.find_elements(
                    By.XPATH, "//div[@class='vim d-picture-panel-maxview']"
                )
                try:
                    for maxview_element in maxview_elements:
                        buttons = maxview_element.find_elements(By.TAG_NAME, "button")
                        try:
                            for button in buttons:
                                if "carousel-item" in button.get_attribute("class"):
                                    items = items + 1
                        except Exception:
                            print("Couldn't find any carousel-items!")
                        while items > itemnum:
                            print(itemnum)
                            buttons = maxview_element.find_elements(
                                By.TAG_NAME, "button"
                            )
                            for button in buttons:
                                if "btn-next" in button.get_attribute("class"):
                                    itemnum = itemnum + 1
                                    pic_count = pic_count + 1
                                    try:
                                        imgs = driver.find_element(
                                            By.XPATH,
                                            "//div[@class='vim d-picture-panel-maxview']",
                                        ).find_elements(By.TAG_NAME, "img")
                                        imgnum = 0
                                        for img in imgs:
                                            if itemnum - 1 == imgnum:
                                                if (
                                                    "/s-l64.jpg"
                                                    not in img.get_attribute("src")
                                                ):
                                                    print(img.get_attribute("src"))
                                                    image_urls.append(
                                                        img.get_attribute("src")
                                                    )
                                                    print(driver.title)
                                                    image_titles.append(driver.title)
                                                    label5.config(
                                                        text=driver.title, fg="green"
                                                    )
                                                    label5.pack(pady=20)
                                                    label6.config(
                                                        text="Collected "
                                                        + str(len(image_urls))
                                                        + " images so far",
                                                        fg="green",
                                                    )
                                                    label6.pack(pady=20)
                                                    window.update()
                                                    os.makedirs(file_path
                                                                + "/"
                                                                + driver.title
                                                                .replace("?", "")
                                                                .replace("|", "")
                                                                .replace("\\", "")
                                                                .replace("/", "")
                                                                .replace(":", "")
                                                                .replace("<", "")
                                                                .replace(">", "")
                                                                .replace("*", "")
                                                                .replace('"', "")
                                                                + "-folder" + random_string + "/")
                                                    item_description_titles.append(
                                                        driver.title
                                                        .replace("?", "")
                                                        .replace("|", "")
                                                        .replace("\\", "")
                                                        .replace("/", "")
                                                        .replace(":", "")
                                                        .replace("<", "")
                                                        .replace(">", "")
                                                        .replace("*", "")
                                                        .replace('"', "")
                                                        + random_string
                                                    )
                                                    item_description.append(
                                                        "Sample description"
                                                    )
                                                    item_description_folders.append(file_path
                                                                + "/"
                                                                + driver.title
                                                                .replace("?", "")
                                                                .replace("|", "")
                                                                .replace("\\", "")
                                                                .replace("/", "")
                                                                .replace(":", "")
                                                                .replace("<", "")
                                                                .replace(">", "")
                                                                .replace("*", "")
                                                                .replace('"', "")
                                                                + "-folder" + random_string + "/")
                                            imgnum = imgnum + 1
                                    except Exception:
                                        print(
                                            "Couldn't get the max view this way. Have to try another way."
                                        )
                                    button.click()
                    print(items)
                    if items == 0:
                        try:
                            pic_maxviews = driver.find_elements(
                                By.XPATH,
                                "//div[@class='ux-image-carousel-item active image']",
                            )
                            for pic_maxview1 in pic_maxviews:
                                imgmaxes = pic_maxview1.find_elements(
                                    By.TAG_NAME, "img"
                                )
                                for imgmax in imgmaxes:
                                    if "/s-l64.jpg" not in imgmax.get_attribute("src"):
                                        print(imgmax.get_attribute("src"))
                                        image_urls.append(imgmax.get_attribute("src"))
                                        print(driver.title)
                                        image_titles.append(driver.title)
                                        label5.config(text=driver.title, fg="green")
                                        label5.pack(pady=20)
                                        label6.config(
                                            text="Collected "
                                            + str(len(image_urls))
                                            + " images so far",
                                            fg="green",
                                        )
                                        label6.pack(pady=20)
                                        window.update()
                                        item_titles.append(driver.title
                                                           .replace("?", "")
                                                           .replace("|", "")
                                                           .replace("\\", "")
                                                           .replace("/", "")
                                                           .replace(":", "")
                                                           .replace("<", "")
                                                           .replace(">", "")
                                                           .replace("*", "")
                                                           .replace('"', "")
                                                           + "-folder" + random_string)
                                        item_folders.append(file_path
                                                            + "/"
                                                            + driver.title
                                                            .replace("?", "")
                                                            .replace("|", "")
                                                            .replace("\\", "")
                                                            .replace("/", "")
                                                            .replace(":", "")
                                                            .replace("<", "")
                                                            .replace(">", "")
                                                            .replace("*", "")
                                                            .replace('"', "")
                                                            + "-folder" + random_string + "/")
                                        os.makedirs(file_path
                                                    + "/"
                                                    + driver.title
                                                    .replace("?", "")
                                                    .replace("|", "")
                                                    .replace("\\", "")
                                                    .replace("/", "")
                                                    .replace(":", "")
                                                    .replace("<", "")
                                                    .replace(">", "")
                                                    .replace("*", "")
                                                    .replace('"', "")
                                                    + "-folder" + random_string + "/")
                                        try:
                                            item_description_titles.append(
                                                driver.title
                                                .replace("?", "")
                                                .replace("|", "")
                                                .replace("\\", "")
                                                .replace("/", "")
                                                .replace(":", "")
                                                .replace("<", "")
                                                .replace(">", "")
                                                .replace("*", "")
                                                .replace('"', "")
                                                + random_string
                                            )
                                        except Exception:
                                            print("Error with titles")
                                        item_description.append(
                                            "Sample description"
                                        )
                                        item_description_folders.append(file_path
                                                                        + "/"
                                                                        + driver.title
                                                                        .replace("?", "")
                                                                        .replace("|", "")
                                                                        .replace("\\", "")
                                                                        .replace("/", "")
                                                                        .replace(":", "")
                                                                        .replace("<", "")
                                                                        .replace(">", "")
                                                                        .replace("*", "")
                                                                        .replace('"', "")
                                                                        + "-folder" + random_string + "/")
                                print("Got some images another way")
                        except Exception:
                            print("Could not get images")
                except Exception:
                    print("Error: Something went wrong")
                item_titles.append(driver.title
                                   .replace("?", "")
                                   .replace("|", "")
                                   .replace("\\", "")
                                   .replace("/", "")
                                   .replace(":", "")
                                   .replace("<", "")
                                   .replace(">", "")
                                   .replace("*", "")
                                   .replace('"', "")
                                   + "-folder" + random_string)
                item_folders.append(file_path
                                    + "/"
                                    + driver.title
                                    .replace("?", "")
                                    .replace("|", "")
                                    .replace("\\", "")
                                    .replace("/", "")
                                    .replace(":", "")
                                    .replace("<", "")
                                    .replace(">", "")
                                    .replace("*", "")
                                    .replace('"', "")
                                    + "-folder" + random_string + "/")
                driver.back()
                driver.back()
                if driver.current_url == "data:,":
                    try:
                        driver.get(huburl)
                    except Exception:
                        print("")
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
            except Exception:
                print("Error: couldn't go there")
                break
            picLinks = []
        img_count = 0
        label5.config(text="", fg="green")
        label5.pack_forget()
        label6.config(
            text="Saved "
            + str(img_count)
            + " of "
            + str(len(image_urls))
            + " images to "
            + file_path
            + "...",
            fg="green",
        )
        label6.pack(pady=20)
        window.update()
        for image_url in image_urls:
            image_name = ""
            response = requests.get(image_url)
            length = 10
            characters = string.ascii_letters + string.digits
            try:
                random_string = "".join(
                    random.choice(characters) for i in range(length)
                )
                image_name = (
                    image_titles[img_count]
                    .replace(" ", "")
                    .replace("?", "")
                    .replace("|", "")
                    .replace("\\", "")
                    .replace("/", "")
                    .replace(":", "")
                    .replace("<", "")
                    .replace(">", "")
                    .replace("*", "")
                    .replace('"', "")
                    + "-"
                    + random_string
                )
                print("Success!!!")
            except Exception:
                random_string = "".join(
                    random.choice(characters) for i in range(length)
                )
                image_name = random_string
                print("No title...")
            try:
                with open(item_folders[img_count] + image_name + ".jpg", "wb") as f:
                    f.write(response.content)
                f.close()
                img_count = img_count + 1
                label6.config(
                    text="Saved "
                    + str(img_count)
                    + " of "
                    + str(len(image_urls))
                    + " images to "
                    + file_path
                    + "...",
                    fg="green",
                )
                label6.pack(pady=20)
                window.update()
            except Exception:
                print(
                    "Image "
                    + image_titles[img_count]
                    + " failed to save, trying a new convention of naming"
                )
                with open(
                    item_folders[img_count] +
                    + image_titles[img_count]
                    .replace(" ", "")
                    .replace("?", "")
                    .replace("|", "")
                    .replace("\\", "")
                    .replace("/", "")
                    .replace(":", "")
                    .replace("<", "")
                    .replace(">", "")
                    .replace("*", "")
                    .replace('"', "")
                    + str(img_count)
                    + ".jpg",
                    "wb",
                ) as f:
                    f.write(response.content)
                img_count = img_count + 1
                label6.config(
                    text="Saved "
                    + str(img_count)
                    + " of "
                    + str(len(image_urls))
                    + " images to "
                    + file_path
                    + "...",
                    fg="green",
                )
                label6.pack(pady=20)
                window.update()
        descr_counter = 0
        for folder in item_description_folders:
            with open(item_description_folders[descr_counter] + item_description_titles[descr_counter] + ".txt", "w") as f:
                f.write("This is the first line of text.\n")
                f.write("This is the second line of text.\n")
                f.write("This is the third line of text.\n")
            descr_counter = descr_counter + 1
        label6.config(text="All done.", fg="green")
        label6.pack(pady=20)
        window.update()
        time.sleep(3)
        label6.config(text="", fg="green")
        label6.pack_forget()
        window.update()
    else:
        if file_path is None or file_path == "":
            label3.pack(pady=20)
        if url.get() is None or url.get() == "":
            label4.pack(pady=20)
    """


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
button = tk.Button(window, text="Start!", font=("Arial", 14))
button["command"] = partial(collect_photos)
button.pack(pady=10)

window.mainloop()
