from bs4 import BeautifulSoup
import urllib2  # WEBREQUEST
import re  # REGEX
from decimal import Decimal 
import time
import subprocess
import datetime
import calendar
from decimal import *
from dateutil.relativedelta import *

class Room:
    def __init__(self, hotel, room, price):
        self.hotel = hotel
        self.room = room
        self.price = price

##########################
#### RiverTide Suites ####
##########################

# Use regular expressions to find the hotel prices here because all of the rooms/rates are stored in the html ##
def getRiverTideKingRate(month1, day1, year1, month2, day2, year2):
    print("\n--- RiverTide Suites ---\n")
    websiteContent = urllib2.urlopen("https://gds.secure-res.com/gc/rez.aspx?locale=en-US&arrive="
                                      + month1 + "/" + day1 + "/" + year1 + "&depart=" + month2 + "/"
                                       + day2 + "/" + year2 + "&adult=1&child=0&group=&Hotel=18238&start=availresults&__utma=3002675.1792862537.1405573478.1405573478.1406086943.2&__utmb=3002675.1.10.1406086943&__utmc=3002675&__utmx=-&__utmz=3002675.1406086943.2.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)&__utmv=-&__utmk=99437724")
    websiteCode = websiteContent.read()
    pricesArrayText = re.findall("var\sprices\s=\snew\sArray[^;]*", websiteCode, re.DOTALL)
    pricesArray = re.findall('\'(.*?)\'', pricesArrayText[0], re.DOTALL)
    
    roomsText = re.findall("var\sroomNamesNoDupes\s=\snew\sArray[^;]*", websiteCode, re.DOTALL)
    roomIdsText = re.findall("var\sroomIdsWithDupes\s=\snew\sArray[^;]*", websiteCode, re.DOTALL)
    roomsArray = re.findall('\'(.*?)\'', roomsText[0], re.DOTALL)
    roomIdsArray = re.findall('\'(.*?)\'', roomIdsText[0], re.DOTALL)
    
    for room in roomsArray:
        print(room)
    
    ## CALCULATE THE RATE FOR A KING ROOM
    kingRoomPrices = []
    index = 0
    for room in roomIdsArray:
        if room == "1RIV":
            kingRoomPrices.append(pricesArray[index])
        elif room == "1RIVH":
            kingRoomPrices.append(pricesArray[index])
        elif room == "1MTN":
            kingRoomPrices.append(pricesArray[index])
        index += 1
        
    totalCost = 0
    for stringPrice in kingRoomPrices:
        totalCost += Decimal(stringPrice)
    kingPrice = 0
    kingPrice = totalCost / len(kingRoomPrices)
    room = Room("rivertide", "king", kingPrice)
    return room

###########################
#### City Center Motel ####
###########################
def getCityCenterMotelRates(month1, day1, year1):
    print("\n--- City Center Motel ---\n")
    roomsArray = []
    kingRoomPrices = []
    loaded = False
    while loaded == False:
        try:   
            browser.get("https://www.bookonthenet.net/west/premium/eresmain.aspx?id=WaRdGJ%2fSYdTmbsQGrTycC%2bkCq7GDGhlJOA3%2bPHMPDAE%3d&arrival_date=" + year1 + "-" + month1 + "-" + day1 + "&stay_nights=1&adults=1&children=0#/rates")
            checkForAlertWindow(browser)
                
            time.sleep(2) 
                              
            for test in browser.find_elements_by_xpath("//div[@class='twelve columns']/span[@class='lblAverageRate']"):
                pricesArray.append(test.text)
            for test2 in browser.find_elements_by_xpath("//span[@class='twelve columns lblRoomType']"):
                roomsArray.append(test2.text)
            loaded = True
        except Exception as e:
            continue
     
    # CALCULATE THE RATE FOR A KING ROOM
    index = 0
    for room in roomsArray:
        print(room + ": $" + pricesArray[index])
        if room == "KING":
            kingRoomPrices.append(pricesArray[index])
        elif room == "KING BED UPSTAIRS":
            kingRoomPrices.append(pricesArray[index])
        index += 1
      
    totalCost = 0
    for stringPrice in kingRoomPrices:
        totalCost += Decimal(stringPrice)
          
    kingPrice = 0
    kingPrice = totalCost / len(kingRoomPrices)
    return(Room("City Center Motel", "king", kingPrice))

    # print(roomsArray)
    # print(roomIdsArray)

##########################################
#### holiday inn express hotel suites ####
##########################################
def getHolidayInnRates(month1, day1, year1, month2, day2, year2):
    print("\n--- holiday inn express hotel suites ---\n")  
    
    roomsArray = []
    
    browser.get("https://www.ihg.com/holidayinnexpress/hotels/us/en/reservation/book?qAdlt=1&qBrs=6c.hi.ex.sb.ul.ic.cp.cw.in.vn.rc.cv.rs.ma.tc&qChld=0&qCiD=" + day1 + "&qCiMy=" + month1 + year1 + "&qCoD=" + day2 + "&qCoMy=" + month2 + year2 + "&qDest=Seaside+OR%2C+UNITED+STATES&qGRM=0&qHtlC=ssdor&qPSt=0&qRRSrt=rt&qRef=df&qRms=1&qRpn=1&qRpp=10&qRtP=6CBARC&qSHp=1&qSlH=SSDOR&qSmP=3&qSrt=sDD&qWch=0&srb_u=1&method=redirect&modifySearch=bookhotel_ssdor")
    checkForAlertWindow(browser)
    for test in browser.find_elements_by_xpath("//span[@class='lowestRate rateSection']"):#/div[@class='headerWrapper']/div"):
        index = 0
        split = test.text.split(" ")
        for word in split:
            if "$" in word:
                pricesArray.append(split[index + 1])
                break
            index += 1
         
    totalCost = 0
    numRoomsFound = 0
    pricesIndex = 0
    for test in browser.find_elements_by_xpath("//span[@class='roomTypeDesc']"):#/div[@class='headerWrapper']/div"):
        roomsArray.append(test.text)
        index = 0
        split = test.text.split(" ")
        for word in split:
            if "KING" in split:
                if "BED" in split:
                    totalCost += Decimal(pricesArray[pricesIndex])
                    numRoomsFound += 1
                    break
            else:
                break
            index += 1
        pricesIndex += 1
        
    index = 0
    for room in roomsArray:
        print(room + ": $" + pricesArray[index])
        index += 1
                    
    #         loaded = True
    #     except Exception as e:
    #         print(e)
    #         continue
        
    # CALCULATE THE RATE FOR A KING ROOM
    kingPrice = 0
    kingPrice = totalCost / numRoomsFound
    return Room("Holiday Inn", "king", kingPrice)

##############################
#### River Inn at Seaside ####
##############################
def getRiverInnRates(month1, day1, year1):
    print("\n--- River Inn at Seaside ---\n")
    roomsArray = []
    pricesArray = []
    kingRoomPrices = []
    
#     loaded = False
#     while loaded == False:
    try:
        browser.get("https://www.bookonthenet.net/west/premium/eresmain.aspx?id=uAaftFpgyLJCC3VBBQSeTef4SKIGR6LNvU37oFXPqEk%3d&arrival_date=" + year1 + "-" + month1 + "-" + day1 +"&stay_nights=1&adults=1&children=0#/rates")
        checkForAlertWindow(browser)
              
        for test in browser.find_elements_by_xpath("//div[@class='twelve columns']/span[@class='lblAverageRate']"):
            pricesArray.append(test.text)
                       
        for test2 in browser.find_elements_by_xpath("//div[@class='row rates']/div[@class='six columns mobile-four']/div[@class='row']/span[@class='twelve columns lblRoomType']"):
            roomsArray.append(test2.text)
        loaded = True
    except Exception as e:
        #continue
        x = 1
        
    # CALCULATE THE RATE FOR A KING ROOM
    index = 0
    for room in roomsArray:
        print(room + ": $" + pricesArray[index])
        if "KING" in room:
            kingRoomPrices.append(pricesArray[index])
        index += 1
      
    totalCost = 0
    for stringPrice in kingRoomPrices:
        totalCost += Decimal(stringPrice)
          
    kingPrice = 0
    kingPrice = totalCost / len(kingRoomPrices)
    return(Room("River Inn At Seaside", "king", kingPrice))

########################
#### Shilo Inn East ####
########################
def getShiloInnEastRates(month1, day1, year1, month2, day2, year2):
    print("\n--- Shilo Inn East ---\n")
    roomsArray = []
    pricesArray = []
    kingRoomPrices = []
       
    ## Note: needs to be in maximized (possibly desktop mode?) in order for
    ##       this to work. if in samller window, the elements change (possibly
    ##       switches to mobile or something?)
        
#     loaded = False
#     while loaded == False:
#         try:

    browser.get("https://be.shiloinns.com/?hotelCode=4242&numAdults=1&numChildren=0&promoCode=&checkInDate=" + month1 + "%2F" + day1 + "%2F" + year1 + "&checkOutDate=" + month2 + "%2F" + day2 + "%2F" + year2 + "&matchingQualifier=alt&currentPage=respMain&style=res&page=avail&restrictToCategory=RACK&NewReservation=avail")
    checkForAlertWindow(browser)
        
    for test in browser.find_elements_by_xpath("//div[@class='room']/div[@class='item hidden-xs']/div[@class='head']/div[@class='name']"):
        roomsArray.append(test.text)
                      
    for test in browser.find_elements_by_xpath("//div[@class='rate']/form/input[@name='totalPrice']"):
        pricesArray.append(test.get_attribute('value'))
    loaded = True
#         except Exception as e:
#             continue

    # CALCULATE THE RATE FOR A KING ROOM
    index = 0
    for room in roomsArray:
        print(room + ": $" + pricesArray[index])
        if "KING" in room:
            kingRoomPrices.append(pricesArray[index])
        index += 1
        
    if len(kingRoomPrices) == 0:
        return(Room("Shilo Inn East", "king", 0))
      
    totalCost = 0
    for stringPrice in kingRoomPrices:
        totalCost += Decimal(stringPrice)
          
    kingPrice = 0
    kingPrice = totalCost / len(kingRoomPrices)
    return(Room("Shilo Inn East", "king", kingPrice))

#################
#### Motel 6 ####
#################
def getMotel6Rates(month1, day1, year1, month2, day2, year2):
    print("\n--- Motel 6 ---\n")
    roomsArray = []
    pricesArray = []
    kingRoomPrices = []
    
    month1 = "2"
    day1 = "12"
    year1 = "2015"
    month2 = "2"
    day2 = "13"
    year2 = "2015"
    
    loaded = False
    while loaded == False:
        try:
            browser.get("http://www.motel6.com/ms/check-availability.do?property=4062&VID=&numberOfAdults=1&arrivalDate=" + year1 + "-" + month1 + "-" + day1 + "&departureDate=" + year2 + "-" + month2 + "-" + day2 + "&corporatePlusNumber=&travelAgentNumber=&BTR=/G6Maps/M6ProximityResults.aspx?searchtype=C")
            checkForAlertWindow(browser)
            
            browser.find_element_by_xpath("//input[@name='submit']").click()
            for test in browser.find_elements_by_xpath("//span[@class='pdetails']"):
                 roomsArray.append(test.text)
            for test in browser.find_elements_by_xpath("//b[@class='blue']"):
                index = 0
                split = test.text.split(" ")
                for word in split:
                    if "$" in word:
                        pricesArray.append(split[index].replace("$", ""))
                        break
                    index += 1
            loaded = True
        except Exception as e:
            continue
    
    # CALCULATE THE RATE FOR A KING ROOM
    index = 0
    for room in roomsArray:
        if room.strip() == "":
            continue
        else:
            print(room + ": $" + pricesArray[index])
            if "KING" in room:
                kingRoomPrices.append(pricesArray[index])
            index += 1
      
    totalCost = 0
    for stringPrice in kingRoomPrices:
        totalCost += Decimal(stringPrice)
          
    kingPrice = 0
    kingPrice = totalCost / len(kingRoomPrices)
    return(Room("Motel 6", "king", kingPrice))

#################################
#### GuestHouse Inn & Suites ####
#################################
def getGuestHouseInnRates(month1, day1, year1):  
    print("\n--- GuestHouse Inn & Suites ---\n")
    roomsArray = []
    pricesArray = []
    kingRoomPrices = []
        
    loaded = False
    while loaded == False:
        try:
            browser.get("https://res.travlynx.com/bbe/page2.aspx?langId=1&pcode=GOSESD&checkin=" + month1 + "%2F" + day1 + "%2F" + year1 + "&nights=1&checkout=" + month2 + "%2F" + day2 + "%2F" + year2 + "&adults=1&rooms=1&children=&bed=&nosmoking=&promo=&group=&iata=&corp=&rate=&ratecat=1&timestamp=&loyalty=")
            checkForAlertWindow(browser)
            
            for test in browser.find_elements_by_xpath("//h2[@class='roomtypename']/a"):
                 roomsArray.append(test.text)
            for test in browser.find_elements_by_xpath("//td[@class='currency']/a"):
                 pricesArray.append(test.text)
            loaded = True
        except Exception as e:
            continue
    
    # CALCULATE THE RATE FOR A KING ROOM
    index = 0
    for room in roomsArray:
        print(room + ": " + pricesArray[index])
        if "KING" in room:
            kingRoomPrices.append(pricesArray[index])
        index += 1
      
    totalCost = 0
    for stringPrice in kingRoomPrices:
        totalCost += Decimal(stringPrice)
          
    kingPrice = 0
    if len(kingRoomPrices) > 0:
        kingPrice = totalCost / len(kingRoomPrices)
        
    return(Room("Guest House Inn", "king", kingPrice))

##############################
#### Shilo Inn Oceanfront ####
##############################
def getShiloInnOceanfrontRates(month1, day1, year1, month2, day2, year2):
    print("\n--- Shilo Inn Oceanfront ---\n")
    roomsArray = []
    pricesArray = []
    kingRoomPrices = []
    
    try:
        browser.get("https://be.shiloinns.com/?checkInDate=" + month1 + "/" + day1 + "/" + year1 + "&checkOutDate=" + month2 + "/" + day2 + "/" + year2 + "&numAdults=1&numChildren=0&promoCode=&restrictToCategory=RACK&style=res&hotelCode=4243&page=avail")
        checkForAlertWindow(browser)
        
        for test in browser.find_elements_by_xpath("//div[@class='room']/div[@class='item hidden-xs']/div[@class='head']/div[@class='name']"):
             roomsArray.append(test.text)
        for test in browser.find_elements_by_xpath("//div[@class='rate']/form/input[@name='totalPrice']"):
             pricesArray.append(test.get_attribute('value'))
    except Exception as e:
        x = 1

    # CALCULATE THE RATE FOR A KING ROOM
    index = 0
    for room in roomsArray:
        print(room + ": $" + pricesArray[index])
        if "KING" in room:
            kingRoomPrices.append(pricesArray[index])
        index += 1
    
    totalCost = 0
    for stringPrice in kingRoomPrices:
        totalCost += Decimal(stringPrice)
    
    kingPrice = 0
    if len(kingRoomPrices) > 0:
        kingPrice = totalCost / len(kingRoomPrices)
        
    return(Room("Shilo Inn Ocean Front", "king", kingPrice))

#######################################
### Best Western Ocean View Resort ####
#######################################
def getBestWesternOceanViewRates(day1):
    print("\n--- Best Western Ocean View Resort ---\n")
    roomsArray = []
    pricesArray = []
    kingRoomPrices = []
          
    browser.get("http://book.bestwestern.com/bestwestern/selectHotel.do#")
    checkForAlertWindow(browser)
    
    destination = browser.find_element_by_xpath("//input[@name='hotelLocation']")
    destination.send_keys("Seaside, Oregon, United States")
    time.sleep(2)
    destination.send_keys(Keys.RETURN)
                 
    browser.find_element_by_xpath("//input[@name='arrDate']").click()
    calendars = browser.find_elements_by_xpath("//table[@class='ui-datepicker-calendar']")
       
    rows = calendars[1].find_elements_by_tag_name("tr")
    i = 1;
    for row in rows:
        if(i == 7):
            break
        numberedDaysInWeek = rows[i].find_elements_by_tag_name("td")
        i += 1
        for numberedDay in numberedDaysInWeek:
            if(numberedDay.text == day1):
                numberedDay.find_element_by_tag_name("a").click()
                break
            else:
                continue
            break
        else:
            continue
        break
                
    browser.implicitly_wait(20)
    buttonDiv = browser.find_element_by_xpath("//div[@class='buttons clearfix']")
    buttons = buttonDiv.find_elements_by_tag_name("a")
    buttons[1].click()
    buttons = browser.find_elements_by_xpath("//div[@class='sideBar']/div[@class='section']/a[@class='button']")
    buttons[0].click()
                 
    browser.implicitly_wait(20)
    rowLinks = browser.find_elements_by_xpath("//table[@class='inner']/tbody/tr/td[@class='description']/a[@class='forwardLink']")
    for link in rowLinks:
        roomsArray.append(link.text)
    prices = browser.find_elements_by_xpath("//td[@class='rate selectRoomRestictionMessage']/strong/span[@class='currencyRateDisplay']")
    for price in prices:
        pricesArray.append(price.text)

    # CALCULATE THE RATE FOR A KING ROOM
    index = 0
    for room in roomsArray:
        if room.strip() == "":
            continue
        else:
            print(room + ": $" + pricesArray[index])
            if "Queen" in room:
                kingRoomPrices.append(pricesArray[index])
            index += 2
    
    totalCost = 0
    for stringPrice in kingRoomPrices:
        totalCost += Decimal(stringPrice)
    
    kingPrice = 0
    if len(kingRoomPrices) > 0:
        kingPrice = totalCost / len(kingRoomPrices)
        
    return(Room("Best Western Ocean View Resort", "king", kingPrice))

###########################################################
#### Comfort Inn & Suites by Seaside Convention Center ####
###########################################################
def getComfortInnConventionCenterRates(day1):
    print("\n Comfort Inn & Suites by Seaside Convention Center ---\n")
    roomsArray = []
    pricesArray = []
    kingRoomPrices = []
    
    loaded = False
    while loaded == False:
        try:
            browser.get("http://www.comfortinn.com/hotel-seaside-oregon-OR421")
            checkForAlertWindow(browser)
            
            browser.find_element_by_xpath("//input[@name='arrivalDate']").click()
            time.sleep(2)
            fromCalendar = browser.find_elements_by_xpath("//table[@class='ui-datepicker-calendar']")
            rows = fromCalendar[0].find_elements_by_tag_name("tr")
            i = 1;
            for row in rows:
                if(i == 7):
                    break
                numberedDaysInWeek = rows[i].find_elements_by_tag_name("td")
                i += 1
                for numberedDay in numberedDaysInWeek:
                    if(numberedDay.text == day1):
                         numberedDay.find_element_by_tag_name("a").click()
                         break
                    else:
                         continue
                    break
                else:
                    continue
                break

            browser.find_element_by_xpath("//button[@name='find']").click()
            time.sleep(2)
            rooms = browser.find_elements_by_xpath("//div[@class='h4 rsm-room-nonsmoking']")
            for room in rooms:
                roomsArray.append(room.text)
            prices = browser.find_elements_by_xpath("//div[@class='mod-rsm-rates-room-rate']/div[@class='amount']")
            for price in prices:
                pricesArray.append(price.text)
            loaded = True
        except Exception as e:
            continue
        
    # CALCULATE THE RATE FOR A KING ROOM
    index = 0
    for room in roomsArray:
        print(room + ": " + pricesArray[index])
        if "King" in room:
            kingRoomPrices.append(pricesArray[index])
        index += 1
    
    totalCost = 0
    index = 0
    for stringPrice in kingRoomPrices:
        stringPriceBeforeDecimal = stringPrice[1:-6]
        stringPriceAfterDecimal = stringPrice[-6:-4]
        totalCost += Decimal(stringPriceBeforeDecimal + "." + stringPriceAfterDecimal)
    
    kingPrice = 0
    if len(kingRoomPrices) > 0:
        kingPrice = totalCost / len(kingRoomPrices)
        
    return(Room("Comfort Inn And Suites", "king", kingPrice))

#### HELPER FUNCTION TO DELETE ANY ERROR MESSAGES THAT POP UP ####
def checkForAlertWindow(browser):
    try:
        alert = browser.switch_to_alert()
        alert.accept()
        
    except Exception as e:
        x = 1
    return

# # ### Booking.com ####
# #   
# print("\n\n\n\n--- Booking ---\n\n")
#    
# browser.get("http://www.booking.com/searchresults.html?src=index&nflt=&ss_raw=seaside+&from_autocomplete=1&error_url=http%3A%2F%2Fwww.booking.com%2Findex.en-us.html%3Faid%3D337733%3Bsid%3Db698d280c4f42bc2672b035e51f569b4%3Bdcid%3D4%3B&aid=337733&dcid=4&sid=b698d280c4f42bc2672b035e51f569b4&si=ai%2Cco%2Cci%2Cre%2Cdi&ss=Seaside%2C+Oregon%2C+USA&checkin_monthday=25&checkin_year_month=2014-11&checkout_monthday=26&checkout_year_month=2014-11&interval_of_time=any&flex_checkin_year_month=any&no_rooms=1&group_adults=1&group_children=0&dest_type=city&dest_id=20105036&ac_pageview_id=e8f2106e931800ff&ac_position=0&ac_langcode=en&ac_suggestion_list_length=5")
# time.sleep(1)
#    
# hotelWindow = webdriver.Chrome("/usr/local/bin/chromedriver")
# hotelWindow.implicitly_wait(5)
#    
# hotellinks = browser.find_elements_by_xpath("//div[@class='sr_item_content']/h3/a")
# for hotellink in hotellinks:
#     print("\n\n--- " + hotellink.text + " ---\n\n")
#     url = hotellink.get_attribute("href")
#     hotelWindow.get(url)
#     time.sleep(2)
#     try:
#         rooms = hotelWindow.find_elements_by_xpath("//a[@class='jqrt togglelink']")
#         for room in rooms:
#             print(room.text)
#     except:
#         pass
#     try:
#         prices = hotelWindow.find_elements_by_xpath("//strong[@class=' b-tooltip-with-price-breakdown-tracker rooms-table-room-price']")
#         for price in prices:
#             print(price.text)
#     except:
#         pass 
    
# ### Priceline ####
#   
# print("\n\n\n\n--- Priceline ---\n\n")
#   
# browser.get("http://www.priceline.com")
# browser.find_element_by_xpath("//input[@name='cityName']").send_keys('Seaside, OR')
#    
# calendarLink = browser.find_element_by_xpath("//input[@name='checkInDate']").click()
# fromCalendar = browser.find_element_by_xpath("//table[@class='ui-datepicker-calendar']")
# print(fromCalendar)
# # fromCalendar.click()
# time.sleep(1)
# rows = fromCalendar.find_elements_by_tag_name("tr")
# i = 1;
# for row in rows:
#     if(i == 7):
#         break
#     days = rows[i].find_elements_by_tag_name("td")
#     i += 1
#     for day in days:
#         if(day.text == "29"):
#              day.find_element_by_tag_name("a").click()
#              break
#         else:
#              continue
#         break
#     else:
#         continue
#     break
#    
# calendarLink = browser.find_element_by_xpath("//input[@name='checkOutDate']")
# fromCalendar = browser.find_element_by_xpath("//table[@class='ui-datepicker-calendar']")
# print(fromCalendar)
# rows = fromCalendar.find_elements_by_tag_name("tr")
# i = 1;
# for row in rows:
#     if(i == 7):
#         break
#     days = rows[i].find_elements_by_tag_name("td")
#     i += 1
#     for day in days:
#         if(day.text == "30"):
#              time.sleep(2)
#              day.find_element_by_tag_name("a").click()
#              time.sleep(2)
#              break
#         else:
#              continue
#         break
#     else:
#         continue
#     break
#    
# hotelWindow = webdriver.Chrome("/usr/local/bin/chromedriver")
# hotelWindow.implicitly_wait(10)
#    
# browser.find_element_by_xpath("//button[@id='hotel-btn-submit-retl']").click()
# chooseButtons = browser.find_elements_by_xpath("//button[@class='listitem_choose']")
# print(len(chooseButtons))
# for chooseButton in chooseButtons:
#     url = chooseButton.get_attribute('listitemexiturl')
#     fullUrl = 'http://www.priceline.com' + url
#     print(fullUrl)
#     hotelWindow.get(fullUrl)
#     hotelName = hotelWindow.find_element_by_xpath("//a[@class='gaHtlEvntTrk']")
#     print("\n\n--- " + hotelName.text + " ---\n\n")
#     rooms = hotelWindow.find_elements_by_xpath("//span[@class='rateInfoDesc']")
#     for room in rooms:
#         print(room.text)
#     rates = hotelWindow.find_elements_by_xpath("//span[@class='rs_Display_rate_dollars']")
#     for rate in rates:
#         print(rate.text)
# #      
# # #### Hotels.com ####
#   
# print("\n\n\n\n--- Hotels.com ---\n\n")
#   
# browser.get("http://www.hotels.com/search.do?current-location=&arrivalDate=11%2F25%2F14&departureDate=11%2F26%2F14&searchParams.rooms.compact_occupancy_dropdown=compact_occupancy_1_1&rooms=1&searchParams.rooms%5B0%5D.numberOfAdults=1&children%5B0%5D=0&srsReport=HomePage%7CAutoS%7Ccity%7Cseaside+or%7C6%7C3%7C0%7C6%7C1%7C15%7C1483629&pageName=HomePage&searchParams.landmark=&resolvedLocation=CITY%3A1483629%3APROVIDED%3APROVIDED")
# time.sleep(2)
#    
# hotelLinks = browser.find_elements_by_xpath("//a[@class='cta cta-hotel-select']")
# print(len(hotelLinks))
# for hotelLink in hotelLinks:
#     url = hotelLink.get_attribute("href")
#     hotelWindow.get(url)
#     hotelName = hotelWindow.find_element_by_xpath("//h1[@class='fn org']")
#     print("\n\n--- " + hotelName.text + " ---\n\n")
#     rooms = hotelWindow.find_elements_by_xpath("//td[@class='room-type']/h3")
#     for room in rooms:
#         print(room.text)
#     rates = hotelWindow.find_elements_by_xpath("//span[@class='current-price']/strong")
#     for rate in rates:
#         print(rate.text)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
browser = webdriver.Chrome("/Users/kevinquiring/Downloads/chromedriver 5")
browser.implicitly_wait(60)

roomsArray = []
pricesArray = []
totalCost = 0

### GET TODAYS DATE AND DO SEARCHES BASED ON IT ###

todaysDate = datetime.date.today()
date1 = todaysDate + datetime.timedelta(days=81)
date2 = todaysDate + datetime.timedelta(days=82)
day1 = str(date1.day)
month1 = str(date1.month)
year1 = str(date1.year)
day2 = str(date2.day)
month2 = str(date2.month)
year2 = str(date2.year)

prevMonth1 = str((date1 - relativedelta(months=1)).month)
prevMonth2 = str((date2 - relativedelta(months=1)).month)
prevYear1 = str((date1 - relativedelta(years=1)).year)
prevYear2 = str((date2 - relativedelta(years=1)).year)

# daysInMonth = calendar.monthrange(year, month)[1]
# print(day)
# print(month)
# print(year)
# print(daysInMonth)
# useNextMonth = False
# if(day == daysInMonth):
#     useNextMonth = True

allRooms = []
allRooms.append(getRiverTideKingRate(month1, day1, year1, month2, day2, year2))
allRooms.append(getCityCenterMotelRates(month1, day1, year1))
allRooms.append(getHolidayInnRates(prevMonth1, day1, year1, prevMonth2, day2, year2))
allRooms.append(getRiverInnRates(month1, day1, year1))
allRooms.append(getShiloInnEastRates(month1, day1, year1, month2, day2, year2)) # BROWSER WINDOW HAS TO BE MAXIMIZED
allRooms.append(getMotel6Rates(month1, day1, year1, month2, day2, year2))   # CAN ONLY DO UP TO 30 DAY ONLINE LOOKUPS, DATES CURRENTLY IN FUNCTION
allRooms.append(getGuestHouseInnRates(month1, day1, year1))
allRooms.append(getShiloInnOceanfrontRates(month1, day1, year1, month2, day2, year2))
allRooms.append(getBestWesternOceanViewRates("3")) # NEED TO MAKE SURE THE DATE FOUND IS ENABLED OR FIND ELEMENT HANGS (EX: IF THE DAY 30 IS IN THE CALENDAR VIEW FROM THE PREV MONTH)
allRooms.append(getComfortInnConventionCenterRates("15"))

print("\n\n--- AVERAGE RATES FOR 'KING-LIKE' ROOMS FROM EACH HOTEL ---\n")

for room in allRooms:
    print(room.hotel + ": King Room = $" + str(room.price))

browser.delete_all_cookies()
browser.quit()
