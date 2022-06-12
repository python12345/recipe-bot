from selenium.webdriver.common.keys import Keys
from time import sleep
import json
import sys
import yaml
import xlwt
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import re
import random





def create_original_link(url):
    if url.find(".php") != -1:
        original_link = (
            facebook_https_prefix + facebook_link_body + ((url.split("="))[1])
        )

        if original_link.find("&") != -1:
            original_link = original_link.split("&")[0]

    elif url.find("fnr_t") != -1:
        original_link = (
            facebook_https_prefix
            + facebook_link_body
            + ((url.split("/"))[-1].split("?")[0])
        )
    elif url.find("_tab") != -1:
        original_link = (
            facebook_https_prefix
            + facebook_link_body
            + (url.split("?")[0]).split("/")[-1]
        )
    else:
        original_link = url

    return original_link




def login(email, password):
    """ Logging into our own profile """
    useCookies=True
    try:
        global driver

        options = Options()

        #  Code to disable notifications pop up of Chrome Browser
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--mute-audio")
        # options.add_argument("headless")
        options.add_argument("user-data-dir=selenium") # cookies using
        print("After Options")
        try:

            driver = webdriver.Chrome(
                executable_path=ChromeDriverManager().install(), options=options
            )
        except Exception:
            print("Error loading chrome webdriver " + sys.exc_info()[0])
            exit(1)
        fb_path = facebook_https_prefix + facebook_link_body

        if not isFbLoggedIn():
            try:
                print("Facebook is not logged in")
                print("Facebook logged in is starting")
                # filling the form
                driver.find_element_by_name("email").send_keys(email)
                driver.find_element_by_name("pass").send_keys(password)
                # clicking on login button
                driver.find_element_by_id("loginbutton").click()
            except NoSuchElementException:
                # Facebook new design
                driver.find_element_by_name("login").click()
        else:
            print("Facebook is logged in!")

        driver.get(fb_path)

    except Exception:
        print("There's some error in log in.")
        print(sys.exc_info()[0])
        exit(1)



def scrapeProfile(url):
    driver.get(url)
    sleep(1)

    htmlCodeByPageSource = driver.page_source
    htmlCodeByScript = driver.execute_script("return document.documentElement.outerHTML;")

    try:
        try:
            # Script code
            if htmlCodeByScript != None:
                print("In htmlCodeByScript")
                numberByScript = numberIsExist(htmlCodeByScript)
                siteByScript = siteIsExist(htmlCodeByScript)
                emailByScript = emailIsExist(htmlCodeByScript)
                print("By Script code:\n", "Number : ", numberByScript, "Email : ",
                      emailByScript)  # ,"Site : ",siteByScript
            else:print("htmlCodeByScript is None")
        except Exception as e:
            print(e)

        try:
            # Page source code
            if htmlCodeByPageSource != None:
                print("In htmlCodeByScript")
                numberByPageSource = numberIsExist(htmlCodeByPageSource)
                siteByScriptPageSource = siteIsExist(htmlCodeByPageSource)
                emailByScriptPageSource = emailIsExist(htmlCodeByPageSource)

                print("By Page source code:\n", "Number : ", numberByPageSource, "Email : ",
                      emailByScriptPageSource)  # ,"Site : ",siteByScriptPageSource
            else:print("htmlCodeByPageSource is None")
        except Exception as e:
            print(e)

        print("\n\n\n\n\n\n\n\n")

    except Exception as e:
        print(e)


def createDriver():
    try:
        global driver

        options = Options()

        #  Code to disable notifications pop up of Chrome Browser
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--mute-audio")
        # options.add_argument("headless")
        options.add_argument("user-data-dir=daniel") # cookies using

        try:
            driver = webdriver.Chrome(options=options)

        except Exception:
            print("Error loading chrome webdriver " + str(sys.exc_info()[0]))
            exit(1)

    except Exception as e:
        print(e)
        print("Error createDriver " +str(sys.exc_info()[0]))
        exit(1)

def scrapeGroupPosts(groupUrl):

    driver.get(groupUrl)

    sleep(2)
    scroll(2,driver,selectors,10)
    postsLinkList=list()
    flagClickPosts=False

    # xpathPosts="/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div/div/div/div/div[1]/div[2]/div[2]/div[*]/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div[2]/div/div[2]/span/span/span[2]/span/a"
    # xpathPosts="//*/span[2]/span/a"
    xpathPosts="//*/span[2]/span/a"
    # xpathPosts="/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div/div/div/div/div/div[1]/div/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div[2]/div/div[2]/span/span/span[2]/span/a"

    try:
        postsLinks = driver.find_elements_by_xpath(xpathPosts)
        print("posts len:", len(postsLinks))

        print("posts:")
        i = 0
        for postLink in postsLinks:
            if i == -1:
                try:
                    postLink.click()
                except Exception as e:
                    print("postLink click EXCEPT", e)

            i += 1
            print("posts innerHTML:", postLink.get_attribute('innerHTML'))
            print("posts OuterHTML:", postLink.get_attribute('outerHTML'))
            print("posts.text:", postLink.text)

            # if i == 1:
            #     postsLink1 = driver.find_element_by_xpath(f"//*[contains(text,'{postLink.text}')]")
            #     try:
            #         postsLink1.click()
            #     except Exception as e:
            #         print("postsLink1 click EXCEPT", e)

            attributes = driver.execute_script('if(arguments[0].attributes!==undefined){var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;} else return "No attributes!!!!!!!"',postLink)
            print("posts attributes:", attributes)

            try:
                herf = postLink.get_attribute("href")
                print("post HERF:", herf)
                try:
                    herf = str(herf)[:str(herf).index("?")]
                except:
                    pass

                postsLinkList.append(herf)
            except Exception as e:
                print("STR EXCEPT", e)
            print("\n")

        # Click
        if flagClickPosts:
            try:
                for postLink in postsLinks:
                    print("Scraping profile")
                    postLink.click()
                    print("Clicked profile")
            except Exception:
                print("failed to click on profile")
            return
    except Exception as e:
        print(e)

    return postsLinkList

def randomNumber(): return random.uniform(1,3)

def scrapePost(postUrl):

    ################# Define XPATHS #################
    #"//*[text()='View more comments']"
    # xpathMoreCommentsComments="//*[contains(text(), 'View more comments')]"
    # xpathOpenComment="/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div/div/div/div/div[1]/div[2]/div[1]/div/div[3]/div/div/div/div/div/div/div/div/div[2]/div/div[4]/div/div/div[1]/div/div[1]/div/div[2]"
    #                 "/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[4]/div/div/div/div/div[1]/div[2]/div/div[3]/div/div/div/div/div/div/div/div/div/div[2]/div/div[4]/div/div/div[1]/div/div[1]/div/div[2]/div"
    # xpathOpenComment="//*[@id='mount_0_0']/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[4]/div/div/div/div/div[1]/div[2]/div/div[3]/div/div/div/div/div/div/div/div/div/div[2]/div/div[4]/div/div/div[1]/div/div[1]/div/div[2]/div" # Working

    # "//*[@id="jsc_c_18"]/span"
    # "/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[4]/div/div/div/div/div/div[1]/div/div/div/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div[1]/span/div/a/div/object/a/div/svg/g/image"
    # "/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[4]/div/div/div/div/div/div[1]/div/div/div/div/div/div/div/div/div/div/div[2]/div/div[4]/div/div/div[1]/div/div[1]/div/div[2]/div[1]/div/span"
    xpathOpenComment="//*/div[1]/div[starts-with(@id, 'jsc')]/span"
    # xpathOpenComment="/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div/div/div/div/div/div[1]/div/div/div/div/div/div/div/div/div[2]/div/div[4]/div/div/div/div/div[1]/div/div[2]/div[1]/div/span" # Working
    xpathMoreComments="//span[contains(text(), 'comments')]"

    xpathAllElements = "//*"
    xpathPreviewComments="//*[ends-with(text(), 'comments')]"
    # xpathPreviewComments="//*[@id='mount_0_0']/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div/div/div/div/div/div[1]/div/div/div/div/div/div/div/div/div[2]/div/div[4]/div/div/div[2]/div[2]/div/div[2]"
    "/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[4]/div/div/div/div/div/div[1]/div/div/div/div/div/div/div/div/div/div/div[2]/div/div[4]/div/div/div[2]/div[2]/div/div[2]"
    "/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[4]/div/div/div/div/div/div[1]/div/div/div/div/div/div/div/div/div/div/div[2]/div/div[4]/div/div/div[2]/div[2]/div/div[2]/span/span"
# "//*[@id="mount_0_0"]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[4]/div/div/div/div/div/div[1]/div/div/div/div/div/div/div/div/div/div/div[2]/div/div[4]/div/div/div[2]/div[2]/div/div[2]/span/span"

    xpathMoreComments="//*[@id='mount_0_0']/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div/div[1]/div[4]/div[2]/div[1]/div[2]/span"
    xpathComments="//div[contains(@aria-label,'Comment')]"
    # xpathProfiles="//div//svg//mask//g//*"
    xpathProfiles="//*[@id='mount_0_0']/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div/div/div/div/div/div[1]/div/div/div/div/div/div/div/div/div[2]/div/div[4]/div/div/div[2]/ul/li[*]/div[1]/div/div[1]/span/div/a"
    # xpathProfiles = "//*[@id='mount_0_0']/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div/div[1]/div[4]/ul/li[*]/div[1]/div/div[2]/div/div[1]/div/div[1]/div/div/span/span"
    #"//*[@id='mount_0_0']/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div/div[1]/div[4]/ul/li[5]/div[1]/div/div[2]/div/div[1]/div/div[1]/div/div/span/span"

    xpathCommentsContent = "//*[@id='mount_0_0']/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div/div/div/div/div/div[1]/div/div/div/div/div/div/div/div/div[2]/div/div[4]/div/div/div[2]/ul/li[*]/div[1]/div/div[2]/div/div[1]/div/div[1]/div/div"
############## Post photo xpath working !!!!
    # xpathCommentsContent="//*[@id='mount_0_0']/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div/div[1]/div[4]/ul/li[*]/div[1]/div/div[2]/div/div[1]/div/div[1]/div/div/div/span/div/div"
    # xpathProfiles="//*[@id='mount_0_0']/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div/div[1]/div[4]/ul/li[*]/div[1]/div/div[2]/div/div[1]/div/div[1]/div/div/span/span"



    ################# Define URL #################

    # url="https://www.facebook.com/groups/secrettelaviv"
    url="https://www.facebook.com/groups/secrettelaviv/permalink/10158663282850943//"
    # url="https://www.facebook.com/groups/secrettelaviv/permalink/10158630646610943/"
    # url="https://www.facebook.com/instagram/photos/a.372558296163354/3534592773293208/?type=3&theater"
    # url="https://www.facebook.com/llbean/photos/a.55494987414/10158220276487415/?type=3&theater"
    # url="https://www.facebook.com/Starbucks/photos/a.10150362709023057/10158872299233057"
    # url="https://www.facebook.com/backyard.org.il/posts/673419573345065"
    # xpathComments="//div[@aria-posinset]//div[contains(@aria-label,'Comment by')]//a/span/span[@dir='auto']"

    ################# Define Flags #################
    flagTest=True
    flagAllXpaths=False
    flagGetCommentsContect=False
    flagGetProfilesComments=False
    flagGetMoreViews=False
    flagClickProfile = False
    flagRemove = False
    facebookProfilesLinks=list()
    facebookComments=list()

    numberOfProfileToScrape=10
    try:
        driver.get(postUrl)
        sleep(randomNumber())
        if flagTest:
            html_code = (driver.page_source).encode('utf-8')
            if str(html_code).__contains__("more comments"):
                try:
                    print(str(html_code)[int(str(html_code).index("more comments")-20):20])
                except :
                    print("Failed")
            # print(html_code)
        if flagAllXpaths:
            try:
                allElements = driver.find_elements_by_xpath(xpathAllElements)
                commentsElement= None
                for element in allElements:

                    try:

                        print("allElements:")
                        # if str(element.get_attribute('innerHTML')).__contains__("comments"):
                        #     print("element.innerHTML  CONTAINS!!!!!!!!!!!!!!!!!!!!!!!!!")
                        #     print("allElements innerHTML:",element.get_attribute('innerHTML') )
                        #     commentsElement=element
                        #
                        #     break


                        if str(element.text).__contains__("more comments"):
                            print("element.text CONTAINS!!!!!!!!!!!!!!!!!!!!!!!!!")
                            print("allElements.text:",element.text)
                            commentsElement=element

                            break
                        attributes = driver.execute_script(
                            'if(arguments[0].attributes!==undefined){var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;} else return "No attributes!!!!!!!"',
                            element)
                        # if str(attributes).__contains__("comments"):
                        #     print("element CONTAINS!!!!!!!!!!!!!!!!!!!!!!!!!")
                        #     print("attributes:", attributes)
                        #     commentsElement=element
                        #     break

                    except Exception as e:
                        print("element in all Exception")

                try:
                    commentsElement.click()
                    print("commentsElement clicked")
                except Exception:
                    print("failed to click on commentsElement")
            except Exception as e:
                print("allElementss Exception")



        if flagRemove:
            for i in range(2):
                sleep(randomNumber())
                try:
                    xpathToRemove = "//*[@id='mount_0_0']/div/didrv[1]/div/div[3]/div/div/div[1]/div[2]/div"

                    elementToRemove = driver.find_element_by_xpath(xpathToRemove)
                    driver.execute_script("arguments[0].setAttribute('class','vote-link up voted')", elementToRemove)
                except Exception as e:
                    pass
                try:
                    xpathToRemoveButton = "//*[@id='facebook']/body/div[*]/div[1]/div/div[2]/div/div/div/div[4]/div"
                    elementToRemoveButton = driver.find_element_by_xpath(xpathToRemoveButton)
                    elementToRemoveButton.click()
                except Exception as e:
                    pass

                    print("elementToRemove Exception - Not exist")
                sleep(2)

        if flagGetMoreViews:
            sleep(randomNumber())
            try:
                moreCommentsButton = driver.find_element_by_xpath(xpathPreviewComments)
                try:
                    moreCommentsButton.click()
                    print("moreCommentsButton clicked")
                except Exception:
                    print("failed to click on more comments")
                print("moreCommentsButton:")
                print("innerHTML:", moreCommentsButton.get_attribute('innerHTML'))
                print("moreCommentsButton.text:", moreCommentsButton.text)

                attributes = driver.execute_script(
                    'if(arguments[0].attributes!==undefined){var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;} else return "No attributes!!!!!!!"',
                    moreCommentsButton)
                print("attributes:", attributes)

                print(moreCommentsButton)

            except Exception as e:
                flagMoreViews = False
                print("More Views Buttons is NOT Exist Exception")


            try:
                # Open comments
                openCommentsButton = driver.find_element_by_xpath(xpathOpenComment)

                if openCommentsButton == None:

                    print("open Views Buttons is NOT Exist!")
                else:
                   attributes = driver.execute_script('if(arguments[0].attributes!==undefined){var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;} else return "No attributes!!!!!!!"',openCommentsButton)
                   print("openCommentsButton attributes:", attributes)
                   try:
                       openCommentsButton.click()
                       sleep(randomNumber())
                       print("openCommentsButton clicked")
                   except Exception:
                       print("failed to click on open comments")
                print("Success to click open comments")
            except Exception as e:
                print("openCommentsButton Exception")

            flagMoreViews = True
            countClicks = 0

            while(flagMoreViews):
                if countClicks == 2:
                    break
                moreCommentsButton = None
                try:
                    moreCommentsButton = driver.find_element_by_xpath(xpathPreviewComments)
                    # if moreCommentsButton == None:
                    #     flagMoreViews = False
                    #     print("More Views Buttons is NOT Exist!")
                    #     break
                    try:
                        moreCommentsButton.click()
                        countClicks += 1
                        print("moreCommentsButton clicked")
                    except Exception:
                        print("failed to click on more comments")
                    print("moreCommentsButton:")
                    print("innerHTML:", moreCommentsButton.get_attribute('innerHTML'))
                    print("moreCommentsButton.text:", moreCommentsButton.text)

                    attributes = driver.execute_script('if(arguments[0].attributes!==undefined){var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;} else return "No attributes!!!!!!!"',moreCommentsButton)
                    print("attributes:", attributes)

                    print(moreCommentsButton)

                except Exception as e:
                    flagMoreViews = False
                    print("More Views Buttons is NOT Exist Exception")
                    break
                print("Clicked:",countClicks)
                sleep(randomNumber())
        if flagGetProfilesComments:
            try:
                profiles = driver.find_elements_by_xpath(xpathProfiles)
                print("profiles len:",len(profiles))

                print("profiles:")
                i=0
                for profile in profiles:

                    i+=1
                    print("profiles innerHTML:", profile.get_attribute('innerHTML'))
                    print("profiles.text:", profile.text)

                    attributes = driver.execute_script(
                        'if(arguments[0].attributes!==undefined){var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;} else return "No attributes!!!!!!!"',
                        profile)
                    print("profiles attributes:", attributes)


                    try:
                        herf = profile.get_attribute("href")
                        try:
                            herf=str(herf)[:str(herf).index("?")]
                        except:
                            pass

                        facebookProfilesLinks.append(herf)
                        print("HERF:",herf)
                    except Exception as e:
                        print("STR EXCEPT",e)
                    print("\n")



                # Click
                if flagClickProfile:
                    try:
                        for profile in profiles:
                            print("Scraping profile")
                            profile.click()
                            print("Clicked profile")
                    except Exception:
                        print("failed to click on profile")

            except Exception as e:
                print(e)

        if flagGetCommentsContect:
            comments = driver.find_elements_by_xpath(xpathCommentsContent)
            print("\n\n")
            print("comments:",comments)
            print("comments len:",len(comments))
            i = 1
            for comment in comments:
                try:
                    print("Comment number", i)
                    try:
                        comment.click()
                    except Exception:
                        print("failed to click on comment")
                    # newDriver=comment.send_keys(Keys.COMMAND + 't')
                    attributes = driver.execute_script(
                        'var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;',
                        comment)
                    print("attributes:", attributes)
                    print("Comment innerHTML:", comment.get_attribute('innerHTML'))
                    print("Comment.text:", comment.text)
                    facebookComments.append(comment.text)
                    # sleep(5)
                    # break

                except Exception as e:
                    print(e)
                i += 1
            print(len(comments))
            sleep(randomNumber())
        if len(facebookProfilesLinks) > 0:
            outputExcel("profilesLinks.xls",facebookProfilesLinks,facebookComments,True)
            print("Excel saved!")
    except Exception as e:
        print(e)
        print("Objects Exception")

def scrapePostOld(url):
    driver.get(url)
    sleep(randomNumber())
    try:
        comments = driver.find_elements_by_xpath("//div[@aria-posinset]//div[contains(@aria-label,'Comment by')]//a/span/span[@dir='auto']")
        print(comments)
        print(len(comments))
        i = 1
        for comment in comments:
            try:
                print("Comment number", i)
                # newDriver=comment.send_keys(Keys.COMMAND + 't')
                attributes = driver.execute_script(
                    'var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;',
                    comment)
                print("attributes:", attributes)

                sleep(randomNumber())
                break

            except Exception as e:
                print(e)
            i += 1
        print(len(comments))
        sleep(randomNumber())
    except Exception as e:
        print(e)
        print("Comments Exception")






def scrape_email_phone(url):

    fromSelenium=True
    fromGroup=True

    if fromSelenium:
        with open("info.html", "r") as info:
            infoHtml = info.read()
        with open("credentials.yaml", "r") as ymlfile:
            cfg = yaml.safe_load(stream=ymlfile)
            print(cfg)

        with open("secrets.json", "r") as jsonfile:
            cfg = json.loads(jsonfile.read())
            print(cfg)

        if ("password" not in cfg) or ("email" not in cfg):
            print("Your email or password is missing. Kindly write them in credentials.txt")
            exit(1)

        print("\nStarting Scraping...")
        login(cfg["email"], cfg["password"])
        sleep(randomNumber())
        scrapePost(url)
        sleep(randomNumber())



    if fromSelenium:
        driver.close()
    # # wait some time
    # print(WebDriverWait(driver, 5).until(
    #     EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='FIND US']//following::span[2]"))))

    # address_elements = driver.find_elements_by_xpath(
    #     "//span[text()='FIND US']/../following-sibling::div//button[text()='Get Directions']/../../preceding-sibling::div[1]/div/span")
    # address_elements = driver.find_elements_by_xpath(
    #     "// span[normalize - space() = 'FIND US'] // following::span[2]")

    # for item in address_elements:
    #     print
    #     item.text
def scroll(total_scrolls, driver, selectors, scroll_time):
    global old_height
    current_scrolls = 0

    while True:
        try:
            if current_scrolls == total_scrolls:
                return

            old_height = driver.execute_script("return document.body.scrollHeight")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            WebDriverWait(driver, scroll_time, 0.05).until(
                lambda driver: check_height(driver, selectors, old_height)
            )
            current_scrolls += 1
        except TimeoutException:
            break

    return
def check_height(driver, selectors, old_height):
    new_height = driver.execute_script(selectors.get("height_script"))
    return new_height != old_height

def saveHtmlCodeToFile(htmlCodeByScript,htmlCodeByPageSource):
    # Script code
    f = open("htmls/htmlByScript.html", "a+")
    f.write(htmlCodeByScript)
    f.close()

    # Page source code
    f = open("htmls/htmlByPageSource.html", "a+")
    f.write(htmlCodeByPageSource)
    f.close()

def numberIsExist(string):
    regexp = re.compile(r'\d{3}[-]\d{3}[-]\d{4}')
    if regexp.search(string):
        print ("number matched")
        response=regexp.findall(string)
        print(response)
        return response
    return False

def emailIsExist(string):
    regexp = re.compile("r'[\w\.-]+@[\w\.-]+'")
    print("In emailIsExist")
    stringToFind = '"mailto:'
    try:
        startIndex=string.index(stringToFind)+8
        print("STRING:",str(string[startIndex]))
        if string.__contains__(stringToFind):
            flagQuote = True
            i = 0
            email = ""
            while(flagQuote):
                if i >= 100 :
                    print("email",email)
                    break
                if string[startIndex + i] == '"':
                    print("Found It!")
                    print(email)
                    flagQuote = False
                    break
                else:
                    email += str(string[startIndex + i])
                i+=1
    except Exception as e:
        print("Failed to get mail",e)

    # if regexp.search(string):
    #     print("email matched")
    #     response=regexp.findall(string)
    #     print(response)
    #     return response


    return False

def siteIsExist(string):
    regexp = re.compile(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)')
    if regexp.search(string):
        print ("site matched")
        response=regexp.findall(string)
        # print(response)
        return response
    return False


def getPageHTML():
    try:
        return driver.get_attribute('innerHTML')

    except Exception as e:
        print(e)
        print("Cannot get HTML page")
        return False

def writeToCSV():

    print("NEED TO CHECK IF MAIL IS VALID!!!!!!!!!!")

def isFbLoggedIn():
    driver.get("https://facebook.com")
    if 'Facebook – log in or sign up' in driver.title:
        return False
    else:
        return True


def outputExcel(filename,  list1,list2,append):
    try:
        style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
                             num_format_str='#,##0.00')
        style1 = xlwt.easyxf(num_format_str='D-MMM-YY')

        wb = xlwt.Workbook()
        ws = wb.add_sheet('Profiles Links')
        ws.write(0, 0, datetime.now(), style1)
        ws.write(1, 0, "Profiles links", style1)
        ws.write(2, 0, "Comment", style1)

        i=2

        for value in list1:
            #  Row , Column
            ws.write(i, 2, value, style0)
            i+=1
        i=2
        for value in list2:
            ws.write(i, 3, value, style0)
            i+=1

        wb.save(filename)

    except Exception as e:
        print(e)
        print("Excel exception")

def scrapPostsUrls(postsLinksList):

    try:
        i = 0
        for postLink in postsLinksList:

            print(f"Working on post link number {i}")
            sleep(randomNumber())
            scrapePost(postLink)


            i += 1
    except Exception as e:
        print(e)
        print("scrapPostsUrls exception")

    print("Finish scraping posts urls")

def scrapeProfiles(profiles):

    try:
        for profile in profiles:
            scrapeProfile(profile)
            pass

    except Exception as e:
        print(e)
        print("Excel exception")

if __name__ == "__main__":

    driver = None
    closeDriver = False
    facebook_https_prefix = "https://"
    facebook_link_body = "facebook.com/"
    with open("selectors.json") as a:
        selectors = json.load(a)




    createDriver()
    scrapePost("https://www.facebook.com/groups/129670421052349/permalink/678665106152875/")

    # scrapePost("https://www.facebook.com/groups/secrettelaviv/permalink/10158663282850943//")
    # login("daniel12344321bb@yandex.com","05776672zZ")
    #scraper()
    # scrape_email_phone("https://www.facebook.com/groups/268799249931777/permalink/2393845007427180/")
    # test()
    # scrapePost("")
    # scrapeProfile("https://www.facebook.com/profile.php?id=100004541714251")
    # style="visibility:hidden"

    # postsLinksList = scrapeGroupPosts("https://www.facebook.com/groups/849614141783591/")

    # scrapPostsUrls(postsLinksList)

    print("Finish all scraping!")

    if closeDriver:
        driver.close()
        print("Driver closed")
