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
import re

file_path = None

def browse_file():
    global file_path
    file_path = filedialog.askdirectory()
    label.config(text=file_path)
    print(file_path)


def executeScan():
    global label6
    label3.pack_forget()
    label4.pack_forget()
    window.update()
    if file_path is not None and file_path != "" and url.get() is not None and url.get() != "":
        label6.config(text="Collecting images from search results, please wait...", fg="green")
        label6.pack(pady=20)
        window.update()
        pagenum = 1
        print("Folder: " + file_path)
        print("URL: " + url.get())
        chrome_options = Options()
        chrome_options.add_argument("--headless")
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
                driver.refresh()
                validPage = False
        try:
            pageButton = driver.find_element(
                By.XPATH, "//a[@class='pagination__item' and text()='" + str(pagenum) + "']"
            )
        except Exception:
            pageButton = "SinglePage"
        image_urls = []
        image_titles = []
        while pageButton or pageButton == "SinglePage":
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
            for link in picLinks:
                driver.get(link)
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
                        for button in buttons:
                            if "carousel-item" in button.get_attribute("class"):
                                items = items + 1
                        while items > itemnum:
                            print(itemnum)
                            buttons = maxview_element.find_elements(By.TAG_NAME, "button")
                            for button in buttons:
                                if "btn-next" in button.get_attribute("class"):
                                    itemnum = itemnum + 1
                                    try:
                                        imgs = driver.find_element(
                                            By.XPATH,
                                            "//div[@class='vim d-picture-panel-maxview']",
                                        ).find_elements(By.TAG_NAME, "img")
                                        imgnum = 0
                                        for img in imgs:
                                            if itemnum - 1 == imgnum:
                                                if "/s-l64.jpg" not in img.get_attribute(
                                                    "src"
                                                ):
                                                    print(img.get_attribute("src"))
                                                    image_urls.append(
                                                        img.get_attribute("src")
                                                    )
                                                    print(driver.title)
                                                    image_titles.append(driver.title)
                                                    label5.config(
                                                        text=driver.title,
                                                        fg="green")
                                                    label5.pack(pady=20)
                                                    label6.config(
                                                        text="Collected " + str(len(image_urls)) + " images so far",
                                                        fg="green")
                                                    label6.pack(pady=20)
                                                    window.update()
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
                                imgmaxes = pic_maxview1.find_elements(By.TAG_NAME, "img")
                                for imgmax in imgmaxes:
                                    if "/s-l64.jpg" not in imgmax.get_attribute("src"):
                                        print(imgmax.get_attribute("src"))
                                        image_urls.append(imgmax.get_attribute("src"))
                                        print(driver.title)
                                        image_titles.append(driver.title)
                                        label5.config(
                                            text=driver.title,
                                            fg="green")
                                        label5.pack(pady=20)
                                        label6.config(
                                            text="Collected " + str(len(image_urls)) + " images so far",
                                            fg="green")
                                        label6.pack(pady=20)
                                        window.update()
                                print("Got some images another way")
                        except Exception:
                            print("Could not get images")
                except Exception:
                    print("Error: Something went wrong")
                driver.back()
                driver.back()
                if driver.current_url == "data:,":
                    try:
                        driver.get(huburl)
                    except Exception:
                        print("")
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
        label5.config(
            text="",
            fg="green")
        label5.pack_forget()
        label6.config(
            text="Saved " + str(img_count) + " of " + str(len(image_urls)) + " images so far",
            fg="green")
        label6.pack(pady=20)
        window.update()
        for image_url in image_urls:
            image_name = ""
            response = requests.get(image_url)
            length = 10
            characters = string.ascii_letters + string.digits
            try:
                random_string = "".join(random.choice(characters) for i in range(length))
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
                random_string = "".join(random.choice(characters) for i in range(length))
                image_name = random_string
                print("No title...")
            try:
                with open(file_path + "/" + image_name + ".jpg", "wb") as f:
                    f.write(response.content)
                img_count = img_count + 1
                label6.config(
                    text="Saved " + str(img_count) + " of " + str(len(image_urls)) + " images so far",
                    fg="green")
                label6.pack(pady=20)
                window.update()
            except Exception:
                print(
                    "Image "
                    + image_titles[img_count]
                    + " failed to save, trying a new convention of naming"
                )
                with open(
                    file_path
                    + "/"
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
                    text="Saved " + img_count + " of " + str(len(image_urls)) + " images to " + file_path + "...",
                    fg="green")
                label6.pack(pady=20)
                window.update()
        label6.config(
            text="All done.",
            fg="green")
        label6.pack(pady=20)
        window.update()
        time.sleep(3)
        label6.config(
            text="",
            fg="green")
        label6.pack_forget()
        window.update()
    else:
        if file_path is None or file_path == "":
            label3.pack(pady=20)
        if url.get() is None or url.get() == "":
            label4.pack(pady=20)

window = tk.Tk()

window.title("Della Scraper")

window.geometry("700x500")
try:
    img = tk.PhotoImage(file="DellaScraperIcon.png")
    window.iconphoto(False,img)
except Exception:
    print("File not found")

label = tk.Label(window, text="Destination Folder", font=("Arial", 16))
label.pack(pady=20)
folder = tk.Button(window, text="Select", command=browse_file)
folder.pack()
label3 = tk.Label(window, text="Make sure to select a destination folder for the files to go into", font=("Arial", 12), fg="red")
label3.pack_forget()
label2 = tk.Label(window, text="Ebay URL", font=("Arial", 16))
label2.pack(pady=20)
label4 = tk.Label(window, text="Make sure to input a ebay url", font=("Arial", 12), fg="red")
label4.pack_forget()
label5 = tk.Label(window, text="Found # images in total", font=("Arial", 12), fg="red")
label5.pack_forget()
label6 = tk.Label(window, text="Saved # out of # images to dest", font=("Arial", 12), fg="red")
label6.pack_forget()
url = tk.Entry(window, highlightthickness=2, highlightbackground="black", width=50)
url.pack()
button = tk.Button(window, text="Start!", font=("Arial", 14))
button["command"] = partial(executeScan)
button.pack(pady=10)

window.mainloop()
