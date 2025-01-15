from selenium import  webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
import time

option=webdriver.ChromeOptions()
option.add_argument("--headless")
option.add_argument("--no-sandbox")
option.add_argument("--disable-dev-shm-usae")
option.add_argument("--disable-gpu")
driver=webdriver.Chrome(options=option)

url="https://www.getmyuni.com/public-colleges?mode=offline"

Collage_name=[]
City_state=[]
Ownership=[]
Courses_offered=[]
Exams=[]
Fees=[]
Ratings=[]

try:
    driver.get(url)
    time.sleep(5)

    for _ in range(5):
        driver.execute_script("window.scrollBy(0,1000);")
        time.sleep(2)

    soup=BeautifulSoup(driver.page_source,"html.parser")

    collage_list=soup.find_all("div",class_="collage_card_new")

    for collage in collage_list:
        collage_name=collage.find("h2",class_="collage__name").text.strip()if collage.find("h2",class_="collage__name")else "N/A"
        location=collage.find("span",class_="list__style college__location").text.strip()if collage.find("span",class_="list__style college__location")else "N/A"
        ownership=collage.find("span",class_="list__style college__affiliation").text.strip()if collage.find("span",class_="list__style college__affiliation")else "N/A"
        ratings=collage.find("span",class_="college__rating").text.strip()if collage.find("span",class_="college__rating")else "N/A"
        course_fee_div=collage.finnd("div",class_="highlight__div")
        if course_fee_div:
            course_element=course_fee_div.find("span",class_="highlight__value")
            courses=course_element.text.strip()

            exam_element=course_fee_div.find_all_next("div",class_="highlight__div")
            exams=exam_element.text.strip()

            fee_elements=course_fee_div.find_all_next("div",class_="highlight__div")
            fees=fee_elements[1].find("span", class_="highlight__value").text.strip() if len(fee_elements)>2 else "N/A"

        else:
            exams="N/A"
            courses="N/A"
            fees="N/A"

        Collage_name.append(collage_name)
        City_state.append(location)
        Ownership.append(ownership)
        Courses_offered.append(courses)
        Exams.append(exams)
        Fees.append(fees)
        Ratings.append(ratings)

except Exception as e:
    print(f"Error fetching data:{e}")

finally:
    driver.quit()

with open("engineering_universities_public1.csv","w",newline='',encoding='utf-8')as file:
    writer=csv.writer(file)
    writer.writerow(["Collage Name","City & State","Ownership","Courses Offered","Exams","Fees","Ratings"])

    for i in range(len(Collage_name)):
        writer.writerow([
            Collage_name[i],
            City_state[i],
            Ownership[i],
            Courses_offered[i],
            Exams[i],
            Ratings[i]
        ])

print("Data Written to CSV file successfully.")