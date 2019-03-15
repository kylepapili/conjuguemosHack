import selenium
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

#Prompt User For Ratio
invalidResponse = True
while (invalidResponse):
    correctRatio = input("What score would you like (correct/total)")
    foundDivisor = False
    correctStr = ""
    totalStr = ""
    for c in correctRatio:
        if c == "/":
            foundDivisor = True
        else:
            if foundDivisor:
                totalStr = totalStr + c
            else:
                correctStr = correctStr + c
    if(correctStr == "" or totalStr == ""):
        print("Invalid Response")
    else:
        correctNum = int(correctStr)
        totalNum = int(totalStr)
        if(correctNum < totalNum):
            invalidResponse = False


#Navigate to Page and Login
driver = webdriver.Firefox(executable_path = '/usr/local/bin/geckodriver')
driver.get("https://beta.conjuguemos.com/student/activities")
username = driver.find_element_by_xpath('//*[@id="identity"]')
password = driver.find_element_by_xpath('//*[@id="password"]')
username.send_keys("19_kpapili")
password.send_keys("!UbF$C9Av42Jd5V")
login_button = driver.find_element_by_xpath('//*[@id="login_btn"]')
login_button.click()

#Select Library, preterit tense, regular verbs
driver.find_element_by_xpath('/html/body/div[2]/div[2]/button').click()
driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div/div[1]/ul[2]/li[2]/a').click()
driver.find_element_by_xpath('/html/body/div[4]/div[2]/div[3]/div[8]/div/a').click()
driver.find_element_by_xpath('//*[@id="practice"]').click()
driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div/div').click()

#Change timer to 10 mins
time_box = driver.find_element_by_xpath('/html/body/x-modal[2]/div/input')
time_box.send_keys(Keys.BACK_SPACE, "10")
time.sleep(1)
driver.find_element_by_xpath('/html/body/x-modal[2]/div/div[2]/button').click()

#Start the Practice Session
time.sleep(1)
driver.find_element_by_xpath('//*[@id="start-button"]').click()

#Target Pronoun, Response, and Noun Elements
pronoun_element = driver.find_element_by_xpath('//*[@id="pronoun-input"]')
verb_element = driver.find_element_by_xpath('//*[@id="verb-input"]')
response = driver.find_element_by_xpath('//*[@id="answer-input"]')

#AR and ER Endings
ar_endings = {"yo": "é", "tú": "aste", "él": "ó", "ella": "ó", "usted": "ó", "nosotros": "amos", "vosotros": "asteis", "ellos": "aron", "ellas": "aron", "ustedes": "aron"}
er_endings = {"yo": "í", "tú": "iste", "él": "ió", "ella": "ió", "usted": "ió", "nosotros": "imos", "vosotros": "isteis", "ellos": "ieron", "ellas": "ieron", "ustedes": "ieron"}

#Conjugate Function
def conjugate(pronoun, verb):
    char_array=[]
    for c in verb:
        char_array.append(c)
    verb_type = char_array[len(char_array)-2]
    #Determine the conjugations_dict to reffer to
    if verb_type == "a": #AR Verb
        conjugations_dict = ar_endings
    elif verb_type == "e" or "i": #ER and IR Verbs
        conjugations_dict = er_endings
    else:
        return "error"
    #Check for correct ending
    if pronoun in conjugations_dict.keys():
        correct_ending = conjugations_dict.get(pronoun)
    else:
        #If the pronoun has ' y ' in it
        is_plural_check=[]
        is_plural = False
        for c in pronoun:
            if c == " " or c== "y" :
                is_plural_check.append(c)
            if is_plural_check == [" ", "y", " "]:
                is_plural = True
        if is_plural: #Pronoun is plural
            if "yo" in pronoun:
                correct_ending = conjugations_dict.get("nosotros")
            else:
                correct_ending = conjugations_dict.get("ellos")
        else: #Pronoun is singular
            correct_ending = conjugations_dict.get("él")
    char_array.pop(len(char_array)-2)
    char_array.pop(len(char_array)-1)
    if(len(str(correct_ending)) > 1):
        for c in correct_ending:
            char_array.append(c)
    else:
        char_array.append(correct_ending)
    return ''.join(char_array)

#Correct Loop
for x in range(0,correctNum): 
    pronoun = pronoun_element.get_attribute("innerText")
    verb = verb_element.get_attribute("innerText")
    answer = conjugate(pronoun, verb)
    ActionChains(driver)     .key_down(Keys.COMMAND)     .key_down("a")     .key_up(Keys.COMMAND)     .key_up("a")     .perform()
    response.send_keys(Keys.BACK_SPACE)
    response.send_keys(answer, Keys.RETURN)

#Incorrect Loop
answer = "wrong"
for x in range(0, totalNum-correctNum):
    answer = answer + "1"
    ActionChains(driver)     .key_down(Keys.COMMAND)     .key_down("a")     .key_up(Keys.COMMAND)     .key_up("a")     .perform()
    response.send_keys(Keys.BACK_SPACE)
    response.send_keys(answer, Keys.RETURN)

#Get Seconds function
def get_sec(time_str):
    m, s = time_str.split(':')
    return int(m) * 60 + int(s)

#Wait Until Session Has Ended
timerElement = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div/div')
timeRemaining = timerElement.text
time.sleep(get_sec(timeRemaining)+5)

#Click Record Score When Ready
driver.find_element_by_xpath('//*[@id="scoreVerbModal"]/div/div[3]/button[2]').click()



    

