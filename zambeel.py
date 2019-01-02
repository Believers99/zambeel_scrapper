from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as exp_cond
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

import time
from collections import namedtuple
from pprint import pprint

from keys import user_id, password

Course = namedtuple('Course', ['name', 'section', 'component', 'timing', 'location', 'instructors', 'dates'])

chrome_options = Options()  
chrome_options.add_argument("--headless") 
driver = webdriver.Chrome(chrome_options=chrome_options)

print('Open Zambeel homepage')
driver.get('https://zambeel.lums.edu.pk/psp/ps/?cmd=login')

elem = driver.find_element_by_name('userid')
elem.clear()
elem.send_keys(user_id)
elem.send_keys(Keys.TAB)

elem = driver.find_element_by_name('pwd')
elem.clear()
elem.send_keys(password)
elem.send_keys(Keys.TAB)

elem = driver.find_element_by_name('Submit')
elem.send_keys(Keys.RETURN)

# TODO: Add proper waiting (until a parricular element loads)
time.sleep(5)
print('Login succesfull')

elem = driver.find_element_by_id('fldra_CO_EMPLOYEE_SELF_SERVICE')
elem.send_keys(Keys.RETURN)
print('Goto Self Service')

# Go to enrollments page
driver.get('https://zambeel.lums.edu.pk/psc/ps/EMPLOYEE/HRMS/s/WEBLIB_PTPP_SC.HOMEPAGE.FieldFormula.IScript_AppHP?scname=CO_EMPLOYEE_SELF_SERVICE&secondary=true&fname=HCCC_ENROLLMENT&pt_fname=HCCC_ENROLLMENT&PortalCacheContent=true&PSCache-Control=role%2cmax-age%3d60&FolderPath=PORTAL_ROOT_OBJECT.CO_EMPLOYEE_SELF_SERVICE.HCCC_ENROLLMENT&IsFolder=true')
print('Goto Enrollment page')

# Go to class schedule
driver.get('https://zambeel.lums.edu.pk/psp/ps/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSR_SSENRL_LIST.GBL?PORTALPARAM_PTCNAV=HC_SSR_SSENRL_LIST&EOPP.SCNode=HRMS&EOPP.SCPortal=EMPLOYEE&EOPP.SCName=CO_EMPLOYEE_SELF_SERVICE&EOPP.SCLabel=Enrollment&EOPP.SCFName=HCCC_ENROLLMENT&EOPP.SCSecondary=true&EOPP.SCPTfname=HCCC_ENROLLMENT&FolderPath=PORTAL_ROOT_OBJECT.CO_EMPLOYEE_SELF_SERVICE.HCCC_ENROLLMENT.HC_SSR_SSENRL_LIST&IsFolder=false')
print('Goto Weekly Schedule')

# TODO: Add proper waiting (until a parricular element loads)
time.sleep(3)

table_frame = driver.find_element_by_id('ptifrmtgtframe')
driver.switch_to_frame(table_frame)
print('Fetch schedule table')

# Grab and parse schedule table
schedule_table = driver.find_element_by_id('ACE_STDNT_ENRL_SSV2$0')

courses = []
course_num = 0
class_comp_num = 0
while True:
    try:
        course_block = schedule_table.find_element_by_id('win0divDERIVED_REGFRM1_DESCR20${}'.format(course_num))
    except NoSuchElementException:
        # All courses have been parsed
        break

    course_name = course_block.find_element_by_class_name('PAGROUPDIVIDER').text
    is_enrolled = course_block.find_element_by_id('STATUS${}'.format(course_num)).text

    row = 1
    while True:
        try:
            class_component = course_block.find_element_by_id('trCLASS_MTG_VW${}_row{}'.format(course_num, row))
        except NoSuchElementException:
            # This course has no other components
            break

        section = class_component.find_element_by_id('MTG_SECTION$span${}'.format(class_comp_num)).text
        component = class_component.find_element_by_id('MTG_COMP${}'.format(class_comp_num)).text
        timing = class_component.find_element_by_id('MTG_SCHED${}'.format(class_comp_num)).text 
        location = class_component.find_element_by_id('MTG_LOC${}'.format(class_comp_num)).text 
        instructors = class_component.find_element_by_id('DERIVED_CLS_DTL_SSR_INSTR_LONG${}'.format(class_comp_num)).text 
        instructors = instructors.replace('\n', '')
        instructors = instructors.replace(',', ';')
        dates = class_component.find_element_by_id('MTG_DATES${}'.format(class_comp_num)).text

        if is_enrolled == 'Enrolled':
            course = Course(course_name, section, component, timing, location, instructors, dates)
            courses.append(course)
        row += 1
        class_comp_num += 1
    print('{} courses gathered'.format(len(courses)))
    course_num += 1

driver.close()

with open('courses.txt', 'w') as f:
    for course in courses:
        f.write('{},{},{},{},{},{},{}\n'.format(course.name, course.section, course.component, course.timing, course.location, course.instructors, course.dates))
