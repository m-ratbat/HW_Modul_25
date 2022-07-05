from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from collections import Counter


def test_all_information_about_pets(setup):
    driver = setup
    driver.implicitly_wait(2)
    driver.find_element(By.XPATH, '//*[@id="email"]').send_keys('test@test.test')
    driver.find_element(By.XPATH, '//*[@id="pass"]').send_keys('12345')
    driver.find_element(By.XPATH, 'html/body/div[1]/div[1]/form[1]/div[3]/button[1]').click()

    assert WebDriverWait(driver, 10).until(
        EC.presence_of_element_located([By.CSS_SELECTOR, "html > body > div > div > div:nth-of-type(2)"]))

    driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul[1]/li[1]/a[1]').click()

    assert WebDriverWait(driver, 10).until(
        EC.presence_of_element_located([By.CSS_SELECTOR, "div#all_my_pets > table"]))  # Check that we are on the "my pets" page

    images = driver.find_elements(By.CSS_SELECTOR, 'div th > img')  # Get all photos about pets on the page

    pets_info = driver.find_elements(By.CSS_SELECTOR, 'div td')  # Get all information about pets on the page
    # Sort the information about pets and write it to separate variables
    names = pets_info[::4]
    breeds = pets_info[1::4]
    ages = pets_info[2::4]

    amount = driver.find_elements(By.CSS_SELECTOR, 'html > body > div > div > div')  # Get the profile information and write it to the variable

    pets_with_photo = 0  # Creating a variable for counting the number of pets with photos
    list_names = []  # Creating an empty list in which we'll write the names of all pets
    all_pets = []  # Creating an empty list in which we'll record all the information about each pet

    for i in range(len(names)):
        # Check the number of pets with the photo and record the number in the variable
        if images[i].get_attribute('src') != '':
            pets_with_photo += 1
        assert names[i].text != ''  # check that all pets have a name
        assert breeds[i].text != ''  # Check that all pets have a breed
        assert ages[i].text != ''  # Check that all pets have an age
        list_names.append(names[i].text)
        all_pets.append(names[i].text + breeds[i].text + ages[i].text)

    assert len(Counter(all_pets)) == len(all_pets)  # Check that there are no duplicate pets
    assert len(Counter(list_names)) == len(list_names)  # Check that name of each animal is unique
    assert f"Питомцев: {len(names)}" in amount[0].text  # Check that number of rows in the table corresponds to the number of pets in the user statistics block
    assert pets_with_photo >= len(names) / 2  # Check that at least half of the pets have a photo


