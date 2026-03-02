INVALID_ACTOR_DATA = {
    "first_name": "",
    "last_name": "",
    "last_update": "2025-01-01 04:34:33"
}
INVALID_FILM_DATA = {
    "description": 'A Fast+Paced Documentary',
    "release_year": '2025',
    "language_id": '1',
    "rental_duration": '6',
    "rental_rate": '4.99',
    "length": '180',
    "replacement_cost": '19.99',
    "rating": 'PG-13',
    "special_features": 'Deleted Scenes'
}

UI_BASE_URL = "http://127.0.0.1:5000/"
ACTOR_LIST = "//table//tbody//tr"
CREATE_NEW_ACTOR = "//button[contains(text(), 'New')]"
NEW_ACTOR_SUBMIT = "//button[@type='submit']"
FIRST_NAME_ID = "create-firstName"
LAST_NAME_ID = "create-lastName"
EDIT_FIRST_NAME_ID = "edit-firstName"
EDIT_LAST_NAME_ID = "edit-lastName"
UPDATE_BUTTON = "//*[@id='edit-form']/button"
RESUL_TEXT = "//h1"

# API CONST
API_BASE_URL = "http://127.0.0.1:5000/api/"
FILM_API_BASE_URL = "http://127.0.0.1:5000/api/films"
ACTORS_API_URL = "http://127.0.0.1:5000/api/actors"
