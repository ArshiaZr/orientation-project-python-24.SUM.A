'''
Flask Application
'''
from flask import Flask, jsonify, request
from models import Experience, Education, Skill
from utils import load_data, save_data, generate_id, correct_spelling

data = load_data('data/data.json')

app = Flask(__name__)

@app.route('/test')
def hello_world():
    '''
    Returns a JSON test message
    '''
    return jsonify({"message": "Hello, World!"})


@app.route('/resume/experience', methods=['GET', 'POST', 'PUT', 'DELETE'])
def experience():
    '''
    Handle experience requests
    '''

    if request.method == "GET":
        index = request.args.get("index")
        # check index is valid number
        if index is not None:
            if not index.isnumeric():
                return jsonify({"error": "Index must be a number"}), 400
            if 0 < int(index) <= len(data["experience"]):
                # ids in data.json are 1 indexed
                return jsonify(data["experience"][int(index)-1]), 200
            return jsonify({"error": 'Index not in range'}), 400

        # if no index, return all experiences
        return jsonify([edu.__dict__ for edu in data['experience']])

    if request.method == "POST":
        required_fields = ['title', 'company', 'start_date', 'end_date', 'description', 'logo']

        if not request.json:
            return jsonify({'error': 'No data provided'}), 400

        missing_fields = [field for field in required_fields if field not in request.json]
        if missing_fields:
            return jsonify({'error': 'Missing required fields'}), 400

        new_id = generate_id(data, 'experience')
        new_experience_data = request.json
        new_experience_data['id'] = new_id
        new_experience = Experience(**new_experience_data)

        data['experience'].append(new_experience)
        save_data('data/data.json', data)

        return jsonify({'id': new_id}), 201
    
    if request.method == "PUT":
        index = request.args.get("index")
        if index is None:
            return jsonify({"error": 'Index not provided'}), 400
        if not index.isnumeric():
            return jsonify({"error": "Index must be a number"}), 400
        
        index = int(index)
        if not (0 < index <= len(data["experience"])):
            return jsonify({"error": 'Index not in range'}), 400
        
        updated_experience_data = request.json
        updated_experience_data['id'] = index
        updated_experience = Experience(**updated_experience_data)
        data["experience"][index - 1] = updated_experience
        save_data('data/data.json', data)
        return jsonify(data["experience"][index - 1]), 200
    
    if request.method == 'DELETE':
        index = request.args.get("index")
        # check index is valid number
        if index is not None:
            if not index.isnumeric():
                return jsonify({"error": "Index must be a number"}), 400
            
            if 0 < int(index) <= len(data["experience"]):
                # ids in data.json are 1 indexed
                data["experience"].pop(int(index)-1)
                save_data('data/data.json', data)
                return jsonify({"message": "Successfully deleted"}), 200

        return jsonify({"error": 'Invalid Index'}), 400

    return jsonify({'error': 'Method not allowed'}), 405


@app.route('/resume/education', methods=['GET', 'POST', 'PUT', 'DELETE'])
def education():
    """
    Handle education requests
    """
    if request.method == 'GET':
        index = request.args.get("index")
        if index is not None: #check if requesting a specific index
            if not index.isnumeric(): #is index a number
                return jsonify("Incorrect index"), 400

            #check if index is inside the bounds of the list
            if int(index) < 0 or int(index) >= len(data.get("skill")):
                return jsonify("Incorrect request, index out of bounds"), 400
            return jsonify(data.get("education")[int(index)]), 200

        return jsonify(data.get("education")), 200 #return the whole list

    if request.method == 'POST':
        required_fields = ['course', 'school', 'start_date', 'end_date', 'grade', 'logo']
        if not request.json:
            return jsonify({'error': 'No data provided'}), 400

        missing_fields = [field for field in required_fields if field not in request.json]
        if missing_fields:
            return jsonify({'error': 'Missing required fields'}), 400

        # If we used database, it will generate the id for us
        new_id = generate_id(data, 'education')

        new_education_data = request.json
        new_education_data['id'] = new_id
        new_education = Education(**new_education_data)

        data['education'].append(new_education)
        save_data('data/data.json', data)

        return jsonify({'id': new_id}), 201
    
    if request.method == 'DELETE':
        index = request.args.get("index")
        # check index is valid number
        if index is not None:
            if not index.isnumeric():
                return jsonify({"error": "Index must be a number"}), 400
            
            if 0 < int(index) <= len(data["education"]):
                # ids in data.json are 1 indexed
                data["education"].pop(int(index)-1)
                save_data('data/data.json', data)
                return jsonify({"message": "Successfully deleted"}), 200

        return jsonify({"error": 'Invalid Index'}), 400
    
    if request.method == "PUT":
        index = request.args.get("index")
        # Check if index is provided and is a number
        if index is None:
            return jsonify({"error": 'Index not provided'}), 400
        if not index.isnumeric():
            return jsonify({"error": "Index must be a number"}), 400
        
        # Check if index is in range
        index = int(index)
        if not 0 < index <= len(data["education"]):
            return jsonify({"error": 'Index not in range'}), 400
        updated_education_data = request.json
        updated_education_data['id'] = index
        updated_education = Education(**updated_education_data)
        data["education"][index - 1] = updated_education
        save_data('data/data.json', data)
        return jsonify(data["education"][index - 1]), 200
    return jsonify({'error': 'Method not allowed'}), 405


@app.route('/resume/skill', methods=['GET', 'POST', 'PUT', 'DELETE'])
def skill():
    '''
    Handles Skill requests
    '''
    if request.method == 'GET':
        index = request.args.get("index")
        if index is not None: #check if requesting a specific index
            if not index.isnumeric(): #is index a number
                return jsonify("Incorrect index"), 400

            #check if index is inside the bounds of the list
            if int(index) < 0 or int(index) >= len(data.get("skill")):
                return jsonify("Incorrect request, index out of bounds"), 400
            return jsonify(data.get("skill")[int(index)]), 200

        return jsonify(data.get("skill")), 200 #return the whole list

    if request.method == 'POST':
        required_fields = ['name', 'proficiency', 'logo']
        if not request.json:
            return jsonify({'error': 'No data provided'}), 400

        missing_fields = [field for field in required_fields if field not in request.json]
        if missing_fields:
            return jsonify({'error': 'Missing required fields'}), 400

        new_id = generate_id(data, 'skill')
        new_skill_data = request.json
        new_skill_data['id'] = new_id
        new_skill = Skill(**new_skill_data)
        data["skill"].append(new_skill)
        save_data('data/data.json', data)

        return jsonify({'id': new_id}), 201

    if request.method == 'DELETE':
        index = request.args.get("index")
        if index is not None: #check if requesting a specific index
            if not index.isnumeric(): #is index a number
                return jsonify("Incorrect index"), 400

            #check if index is inside the bounds of the list
            if int(index) < 0 or int(index) >= len(data.get("skill")):
                return jsonify("Incorrect request, index out of bounds"), 400

            data.get("skill").pop(int(index))
            save_data('data/data.json', data)
            return jsonify({"message": "Successfully deleted"}), 200

        return jsonify({"error": 'Invalid request'}), 400

    if request.method == 'PUT':
        index = request.args.get("index")
        if index is None:
            return jsonify({"error": 'Index not provided'}), 400
        if not index.isnumeric():
            return jsonify({"error": "Index must be a number"}), 400
        
        index = int(index)
        if not 0 < index <= len(data["skill"]):
            return jsonify({"error": 'Index not in range'}), 400
        
        updated_skill_data = request.json
        updated_skill_data['id'] = index
        updated_skill = Skill(**updated_skill_data)
        data["skill"][index] = updated_skill
        save_data('data/data.json', data)
        return jsonify(data["skill"][index]), 200
    return jsonify({})


@app.route('/spelling/correct-spelling', methods=['GET', 'POST'])
def spelling_check():
    '''
    Handles spelling check requests
    '''
    data = request.get_json()
    text = data.get('text', '')
    corrected_text = correct_spelling(text)

    # return the original and corrected text
    return jsonify({"before": text, "after": corrected_text})
