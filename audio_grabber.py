import selenium.common.exceptions
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import requests


def download_audio(url, output_path, name):
    # Send a GET request to download the file
    response = requests.get(url)
    trueOutputPath = output_path + name + ".mp3"

    # Check if the request was successful
    if response.status_code == 200:
        # Save the content of the response (M4A file) to a local file
        with open(trueOutputPath, "wb") as file:
            file.write(response.content)
        print("✅ File downloaded successfully: \"" + name + "\".\n")
    else:
        print("❌ Error: Failed to download \"" + name + "\".\n")


def fetch_audio(string, outputPath, name):
    print("✅ Attempting to fetch audio: " + string[:40] + " ...")

    myUrl = "https://acapela-box.com/AcaBox/index.php"
    caps = DesiredCapabilities.CHROME
    caps['goog:loggingPrefs'] = {'performance': 'ALL'}

    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": "../audiofiles/"}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options, keep_alive=True)

    driver.get(myUrl)

    element = driver.find_element(By.ID, "acaboxText")

    wait = WebDriverWait(driver, timeout=2)
    wait.until(lambda d: element.is_displayed())
    element.send_keys(string)

    try:
        voiceSelector = driver.find_element(By.ID, "acaboxvoice_cb_title")
        while voiceSelector.text != "Will (FromAfar)":
            driver.find_element(By.ID, "acaboxvoice_div").click()
            element.send_keys('will (from' + Keys.ENTER)
    except selenium.common.exceptions.StaleElementReferenceException:
        voiceSelector = driver.find_element(By.ID, "acaboxvoice_cb_title")
        while voiceSelector.text != "Will (FromAfar)":
            driver.find_element(By.ID, "acaboxvoice_div").click()
            element.send_keys('will (from' + Keys.ENTER)

    driver.find_element(By.ID, "TOSAccepted").click()

    element = driver.find_element(By.ID, "acaboxText")

    while element.text is None:
        element = driver.find_element(By.ID, "acaboxText")
        element.send_keys(string)
        test = driver.find_element(By.ID, "acaboxText")
        print(test.text)
        print(element.text)
    element = driver.find_element(By.ID, "acaboxText").send_keys(string)
    driver.find_element(By.ID, value="listen_button").click()

    try:
        wait = WebDriverWait(driver, timeout=20)
        seekBar = driver.find_element(By.CLASS_NAME, "jp-seek-bar")
        wait.until(lambda d: seekBar.value_of_css_property('width') != "0px")
    except TimeoutException:
        print("❌ Error: TimeoutException\n")

    try:
        perf = driver.get_log('performance')
        perfString = str(perf)
        urlIndex = perfString.find("https://vaasbox.acapela-box.com/MESSAGES/")
        urlString = ""
        i = urlIndex
        while perfString[i + 1] != "}":
            urlString = urlString + perfString[i]
            i += 1
        download_audio(urlString, outputPath, name)
    except requests.exceptions.InvalidSchema:
        print("❌ Error: InvalidSchema: Attempted download failed. Possibly needed more time.\n")
        return 1
    return 0
