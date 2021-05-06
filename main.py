import urllib.request
import html5lib
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1080")
options.add_argument("--log-level=3")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options, executable_path="chromedriver.exe")


def validate(myurl):
    try:
        BeautifulSoup(urllib.request.urlopen(myurl), 'html5lib')
        return True
    except urllib.error.HTTPError:
        print('Your username or list name is invalid. Try again.')
        return False
    except UnicodeEncodeError:
        print("Your input has invalid characters. Try again.")
    except Exception as e:
        print(e.__class__, "occurred. Try again")


def listprompt():
    validated = False
    while not validated:
        print('Enter list details to export')
        username = input('Username: ')
        listname = input('Listname: ')
        myurl = 'https://letterboxd.com/{}/list/{}/page/{}/'.format(username, listname, 1)
        validated = validate(myurl)

    soup = BeautifulSoup(urllib.request.urlopen(myurl), 'html5lib')
    print('Exporting {}'.format(soup.title.text[:-12].strip()))
    return {"soup": soup, "username": username, "listname": listname}


def getpagecount(soup):
    if len(soup.find_all("div", attrs={"class": "pagination"})) > 0:
        for a in soup.find_all("div", attrs={"class": "pagination"}):
            return int(a.find_all("a")[-1].text)
    else:
        return 1


def scrollpage():
    for i in range(5):
        time.sleep(0.5)
        driver.execute_script("window.scrollBy(0, 740)")
    time.sleep(0.05)


def getlistmovies(username, listname, pagecount):
    page = 1
    count = 1
    print('Title,Year')
    print(page)
    print(pagecount)
    while page < pagecount + 1:

        myurl = 'https://letterboxd.com/{}/list/{}/page/{}/'.format(username, listname, page)
        driver.get(myurl)
        scrollpage()

        soup = BeautifulSoup(driver.page_source, 'html5lib')
        scripttags = soup.find_all('div')

        for script in scripttags:
            if script.has_attr('data-film-name'):
                print(', '.join([script['data-film-name'], script['data-film-release-year']]))
                count += 1
        page += 1

    driver.quit()
    print("Export completed.")


def main():
    while True:
        inputs = listprompt()
        getlistmovies(inputs["username"], inputs["listname"], getpagecount(inputs["soup"]))


if __name__ == "__main__":
    main()
