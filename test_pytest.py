'''
Tests in Pytest
'''
from app import app

from models import Skill
from utils import load_data, correct_spelling

data = load_data('data/data.json')

def test_client():
    '''
    Makes a request and checks the message received is the same
    '''
    response = app.test_client().get('/test')
    assert response.status_code == 200
    assert response.json['message'] == "Hello, World!"


def test_experience():
    '''
    Add a new experience and then get all experiences. 
    
    Check that it returns the new experience in that list
    '''
    example_experience = {
        "title": "Software Developer",
        "company": "A Cooler Company",
        "start_date": "October 2022",
        "end_date": "Present",
        "description": "Writing JavaScript Code",
        "logo": "example-logo.png"
    }

    post_response = app.test_client().post('/resume/experience', json=example_experience)
    assert post_response.status_code == 201
    new_experience_id = post_response.json['id']
    
    get_response = app.test_client().get('/resume/experience')
    assert get_response.status_code == 200
    
    found = False
    for experience in get_response.json:
        if experience['id'] == new_experience_id:
            for key, value in example_experience.items():
                assert experience[key] == value
            found = True
            break
        
    assert found, "New experience was not found in the returned list"

def test_delete_experience():
    '''
    Add a new experience and then delete experience by index. 
    
    '''
    prior_experience = app.test_client().get('resume/experience').json
    example_experience = {
        "title": "Software Developer",
        "company": "A Cooler Company",
        "start_date": "October 2022",
        "end_date": "Present",
        "description": "Writing JavaScript Code",
        "logo": "example-logo.png"
    }
    item_id = app.test_client().post('/resume/experience',
                                     json=example_experience).json['id']

    response = app.test_client().delete(f'/resume/experience?index={item_id}')
    assert response.json['message'] == "Successfully deleted"
    assert prior_experience == app.test_client().get('resume/experience').json


def test_education():
    '''
    Add a new education and then get all educations.
    
    Check that the new education is correctly added to the list.
    '''
    example_education = {
        "course": "Engineering",
        "school": "NYU",
        "start_date": "October 2022",
        "end_date": "August 2024",
        "grade": "86%",
        "logo": "example-logo.png"
    }
    post_response = app.test_client().post('/resume/education', json=example_education)
    assert post_response.status_code == 201
    new_education_id = post_response.json['id']

    get_response = app.test_client().get('/resume/education')
    assert get_response.status_code == 200

    found = False
    for education in get_response.json:
        if education['id'] == new_education_id:
            for key, value in example_education.items():
                assert education[key] == value
            found = True
            break
        
    assert found, "New education was not found in the returned list"


def test_delete_education():
    '''
    Add a new education and then delete education by index. 
    
    '''
    prior_education = app.test_client().get('resume/education').json
    example_education = {
        "course": "Engineering",
        "school": "NYU",
        "start_date": "October 2022",
        "end_date": "August 2024",
        "grade": "86%",
        "logo": "example-logo.png"
    }
    item_id = app.test_client().post('/resume/education',
                                     json=example_education).json['id']

    response = app.test_client().delete(f'/resume/education?index={item_id}')
    assert response.json['message'] == "Successfully deleted"
    assert prior_education == app.test_client().get('resume/education').json


def test_post_education_missing_fields():
    """Test POST request to /resume/education with missing fields.
    POST request with missing 'end_date' and 'grade' fields.
    """
    incomplete_education = {
        "course": "Engineering",
        "school": "UBC",
        "start_date": "October 2024",
        "logo": "example-logo.png"
    }
    response = app.test_client().post('/resume/education', json=incomplete_education)
    assert response.status_code == 400
    
def test_post_experience_missing_fields():
    """Test POST request to /resume/experience with missing fields.
    POST request with missing 'company' and 'start_date' fields.
    """
    incomplete_experience = {
        "title": "Software Developer",  
        "description": "Writes code",
    }
    response = app.test_client().post('/resume/experience', json=incomplete_experience)
    assert response.status_code == 400  

def test_skill_indexed_get():
    '''
    Load skill data from data.json
    Check that we can get all skills through indexes
    '''
    index = 0
    for skill in data.get("skill"):
        new_skill = Skill(**app.test_client().get(f'/resume/skill?index={index}').json)
        assert new_skill == skill, f"No skill or incorrect skill found at the index {index}"
        index += 1

def test_skill_get_all():
    '''
    Load skills data from data.json
    Check that the list we get from server is the same as the local list
    '''
    local_skills = data.get("skill")
    skills = app.test_client().get('/resume/skill').json
    for i, skill in enumerate(skills):
        assert local_skills[i] == Skill(**skill)

def test_skill():
    '''
    Add a new skill and then get all skills. 
    
    Check that it returns the new skill in that list
    '''
    example_skill = {
        "name": "JavaScript",
        "proficiency": "2-4 years",
        "logo": "example-logo.png"
    }

    item_id = app.test_client().post('/resume/skill',
                                     json=example_skill).json['id']

    response = app.test_client().get('/resume/skill')
    check_skill = None
    example_skill['id'] = item_id
    for skill in response.json:
        if skill['id'] == item_id:
            check_skill = skill
            break
    assert check_skill == example_skill

def test_delete_skill():
    '''
    Add a new skill.
    Delete the skill.
    Check if it was deleted.
    '''
    skills_before_change = app.test_client().get('/resume/skill').json

    example_skill = {
        "name": "Go",
        "proficiency": "1 year",
        "logo": "example-logo.png"
    }

    item_id = app.test_client().post('/resume/skill',
                                     json=example_skill).json['id']
    delete_response = app.test_client().delete(f'resume/skill?index={item_id}')
    assert delete_response.json["message"] == "Successfully deleted"
    assert skills_before_change == app.test_client().get('/resume/skill').json


def test_correct_spelling():
    '''
    Test the correct_spelling function
    '''
    text = "speling"
    expected_output = "spelling"
    assert correct_spelling(text) == expected_output
    
def test_update_experience():
    '''
    Test the updating functionality of experience
    '''
    # Post a new experience
    example_experience = {
        "title": "Example Developer",
        "company": "Example Company",
        "start_date": "October 2022",
        "end_date": "Present",
        "description": "Writing JavaScript Code",
        "logo": "example-logo.png"
    }

    updated_experience = {
        "title": "Roblox Developer",
        "company": "Roblox",
        "start_date": "2022-01-01",
        "end_date": "2023-01-01",
        "description": "Updated description",
        "logo": "updated-logo-url"
    }

    # Post a new experience
    post_response = app.test_client().post('/resume/experience', json=example_experience)
    assert post_response.status_code == 201
    new_experience_id = post_response.json['id']

    # Update the experience
    update_response = app.test_client().put(f'/resume/experience?index={new_experience_id}', json=updated_experience)
    assert update_response.status_code == 200

    # Check if the experience was updated correctly
    get_response = app.test_client().get('/resume/experience')
    experiences = get_response.json
    found = False

    for experience in experiences:
        if experience['id'] == new_experience_id:
            for key, value in updated_experience.items():
                assert experience[key] == value
            found = True
            break

    assert found, "Updated experience was not found in the returned list"
    
def test_update_education():
    '''
    Test the updating functionality of education
    '''
    # Post a new education
    example_education = {
        "course": "Engineering",
        "school": "NYU",
        "start_date": "October 2022",
        "end_date": "August 2024",
        "grade": "86%",
        "logo": "example-logo.png"
    }

    updated_education = {
        "course": "Computer Science",
        "school": "UBC",
        "start_date": "2022-01-01",
        "end_date": "2023-01-01",
        "grade": "90%",
        "logo": "updated-logo-url"
    }

    # Post a new education
    post_response = app.test_client().post('/resume/education', json=example_education)
    assert post_response.status_code == 201
    new_education_id = post_response.json['id']

    # Update the education
    update_response = app.test_client().put(f'/resume/education?index={new_education_id}',
                                             json=updated_education)
    assert update_response.status_code == 200

    # Check if the education was updated correctly
    get_response = app.test_client().get('/resume/education')
    educations = get_response.json
    found = False

    for education in educations:
        if education['id'] == new_education_id:
            for key, value in updated_education.items():
                assert education[key] == value
            found = True
            break
    assert found, "Updated education was not found in the returned list"

def test_update_skill():
    '''
    Test the updating functionality of skill
    '''
    # Post a new skill
    example_skill = {
        "name": "JavaScript",
        "proficiency": "2-4 years",
        "logo": "example-logo.png"
    }

    updated_skill = {
        "name": "Python",
        "proficiency": "3-5 years",
        "logo": "updated-logo-url"
    }

    # Post a new skill
    post_response = app.test_client().post('/resume/skill', json=example_skill)
    assert post_response.status_code == 201
    new_skill_id = post_response.json['id']

    # Update the skill
    update_response = app.test_client().put(f'/resume/skill?index={new_skill_id}', json=updated_skill)
    assert update_response.status_code == 200

    # Check if the skill was updated correctly
    get_response = app.test_client().get('/resume/skill')
    skills = get_response.json
    found = False

    for skill in skills:
        if skill['id'] == new_skill_id:
            for key, value in updated_skill.items():
                assert skill[key] == value
            found = True
            break
    assert found, "Updated skill was not found in the returned list"