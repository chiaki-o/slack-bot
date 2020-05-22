import time
import chromedriver_binary
from bs4 import BeautifulSoup
from selenium import webdriver


def scraping():
    startUrl = "https://jp.indeed.com/jobs?q=python&l="
    maxCount = 4
    jobList = []

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    for i in range(0, maxCount):
        if i == 0:
            driver.get(startUrl)
        else:
            currentUrl = driver.current_url
            driver.get(currentUrl)
            html = driver.page_source.encode('utf-8')
            soup = BeautifulSoup(html, "html.parser")
            list = soup.find("td", id="resultsCol").find_all("div", class_="jobsearch-SerpJobCard")
    for job in list:
        jobInfo = []
        jobInfo.append(job.find("span", class_="company").text.replace('\n', ''))
        jobInfo.append(job.find("h2", class_="title").text.replace('\n', ''))
        jobInfo.append(job.find("div", class_="summary").text.replace('\n', ''))
        jobInfo.append("https://jp.indeed.com" + job.find("h2", class_="title").find("a").get("href"))
        jobList.append(jobInfo)

        if soup.find("div", class_="pagination").find_all("span", class_="pn")[-1].find("span", class_="np"):
            if soup.find("div", class_="pagination").find_all("span", class_="pn")[-1].find("span", class_="np").text.split('へ')[0] == "次":
                time.sleep(10)
                driver.find_elements_by_class_name('pn')[-1].click();
    return jobList