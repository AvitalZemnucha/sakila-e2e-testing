# pages/actor_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from config_data import UI_BASE_URL, ACTOR_LIST, CREATE_NEW_ACTOR, FIRST_NAME_ID, LAST_NAME_ID, NEW_ACTOR_SUBMIT, \
    EDIT_FIRST_NAME_ID, EDIT_LAST_NAME_ID


class ActorPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        """פותח את דף השחקנים"""
        self.driver.get(UI_BASE_URL)
        return self

    def get_all_actors_elements(self):
        """מחזיר את כל שורות השחקנים בטבלה"""
        self.wait.until(EC.presence_of_element_located((By.XPATH, ACTOR_LIST)))
        return self.driver.find_elements(By.XPATH, ACTOR_LIST)

    def add_actor(self, first_name, last_name):
        """ביצוע תהליך הוספת שחקן חדש והמתנה להופעתו בטבלה"""
        # שמירת כמות השחקנים הנוכחית לפני ההוספה
        initial_count = len(self.get_all_actors_elements())

        self.wait.until(EC.element_to_be_clickable((By.XPATH, CREATE_NEW_ACTOR))).click()

        # מילוי טופס
        self.wait.until(EC.presence_of_element_located((By.ID, FIRST_NAME_ID))).send_keys(first_name)
        self.driver.find_element(By.ID, LAST_NAME_ID).send_keys(last_name)

        # שליחה
        self.driver.find_element(By.XPATH, NEW_ACTOR_SUBMIT).click()

        # --- המתנה חכמה במקום Refresh ---
        # 1. מחכים שמספר השורות בטבלה יגדל ב-1
        self.wait.until(lambda d: len(d.find_elements(By.XPATH, ACTOR_LIST)) == initial_count + 1)

        # 2. מוודאים שהטקסט של השחקן החדש מופיע בשורה האחרונה
        last_row_xpath = f"({ACTOR_LIST})[last()]"
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, last_row_xpath), first_name))

    def update_actor(self, actor_id, new_first, new_last):
        edit_btn_xpath = f"//tr[@id='actor-{actor_id}']//button[contains(text(), 'Edit')]"
        self.wait.until(EC.element_to_be_clickable((By.XPATH, edit_btn_xpath))).click()

        first_input = self.wait.until(EC.presence_of_element_located((By.ID, EDIT_FIRST_NAME_ID)))
        first_input.clear()
        first_input.send_keys(new_first)

        last_input = self.driver.find_element(By.ID, EDIT_LAST_NAME_ID)
        last_input.clear()
        last_input.send_keys(new_last)

        self.driver.find_element(By.XPATH, "//*[@id='edit-form']/button[1]").click()

        # --- תוספת קריטית: המתנה עד שהטקסט החדש יופיע בשורה הספציפית ---
        row_xpath = f"//tr[@id='actor-{actor_id}']"
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, row_xpath), new_first))

    def delete_last_actor(self):
        """מחיקת השחקן האחרון ואימות שהשורה נעלמה"""
        actors = self.get_all_actors_elements()
        initial_count = len(actors)
        last_actor = actors[-1]
        # לחיצה על כפתור מחיקה
        delete_btn = last_actor.find_element(By.XPATH, ".//button[contains(text(), 'Delete')]")
        delete_btn.click()
        # אישור ה-Alert
        self.wait.until(EC.alert_is_present())
        Alert(self.driver).accept()
        # המתנה שהשורה הספציפית תימחק מהדף (Staleness)
        self.wait.until(EC.staleness_of(last_actor))
        # המתנה אופציונלית נוספת: לוודא שמספר השורות בטבלה קטן ב-1
        # זה מונע את הצורך ב-Refresh בתוך הטסט
        self.wait.until(lambda d: len(d.find_elements(By.XPATH, ACTOR_LIST)) == initial_count - 1)
