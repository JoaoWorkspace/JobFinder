import os
import sys
import json
import jsonschema

from jsonschema import validate

from Utils import get_integer_input
from GenerateCV import generate_cv_for_companies
from GenerateEmail import send_cv_email_to_companies

def load_data(json_file):
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as error:
        print(f"<- MAIN -> Error: {error}")
        sys.exit()

def validate_data(data):
    schema = {
        "type": "object",
        "properties": {
            "minimumInterval": {"type": "integer"},
            "maximumInterval": {"type": "integer"},
            "message": {
                "type": "object",
                "properties": {
                    "opening": {"type": "array", "items": {"type": "string"}},
                    "constant": {"type": "array", "items": {"type": "string"}},
                    "variable": {"type": "array", "items": {"type": "string"}},
                    "ending": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["opening", "constant", "variable", "ending"]
            },
            "companies": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "logo": {"type": "string"},
                        "email": {"type": "string", "format": "email"},
                        "position": {"type": "string"}
                    },
                    "required": ["logo", "email", "position"]
                }
            },
            "avatar": {"type": "string"},
            "name": {"type": "string"},
            "title": {"type": "string"},
            "about": {"type": "array", "items": {"type": "string"}},
            "contact": {
                "type": "object",
                "properties": {
                    "address": {"type": "string"},
                    "phone": {"type": "string"},
                    "email": {"type": "string", "format": "email"},
                    "linkedin": {"type": "string", "format": "uri"},
                    "github": {"type": "string", "format": "uri"}
                },
                "required": ["address", "phone", "email", "linkedin", "github"]
            },
            "experience": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "team": {"type": "string"},
                        "company": {"type": "string"},
                        "date": {"type": "string"},
                        "sectors": {"type": "array", "items": {"type": "string"}},
                        "technologies": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["title", "team", "company", "date", "sectors", "technologies"]
                }
            },
            "education": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "degree": {"type": "string"},
                        "institution": {"type": "string"},
                        "date": {"type": "string"}
                    },
                    "required": ["degree", "institution", "date"]
                }
            },
            "certificates": {
                "type": "array", 
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "authority": {"type": "string"},
                        "date": {"type": "string"}
                    },
                    "required": ["name", "authority", "date"]
                }
            },
            "projects": {
                "type": "array", 
                "items": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "description": {
                            "oneOf": [
                                {   
                                    "type": "string"
                                },
                                {
                                    "type": "array",
                                    "items": {"type": "string"}
                                }
                            ]
                        }
                    },
                    "required": ["title", "description"]
                }
            },
            "skills": {
                "type": "object",
                "properties": {
                    "Technical": {
                        "type": "object",
                        "additionalProperties": {
                            "type": "integer"
                        }
                    },
                    "Leadership and Management": {
                        "type": "object",
                        "additionalProperties": {
                            "type": "integer"
                        }
                    },
                    "Soft": {
                        "type": "object",
                        "additionalProperties": {
                            "type": "integer"
                        }
                    }
                }
            },
            "languages": {
                "type": "object",
                "additionalProperties": {
                    "type": "integer"
                }
            }
        },
        "required": ["message", "companies", "avatar", "name", "title", "about", "contact"]
    }
    try:
        validate(instance=data, schema=schema)
        print("<- MAIN -> Data is valid.")
    except jsonschema.exceptions.ValidationError as error:
        print(f"<- MAIN -> Data validation error: {error.message}")
        sys.exit()

def main():
    pdf_folder = 'output'
    data = load_data('curriculum.json')
    print(f"<- MAIN -> Analyzing your 'curriculum.json' data...")
    validate_data(data)
    
    print(f"<- MAIN -> Welcome to JobFinder {data['name']}! Type the corresponding number in order to select an option.\n<- MAIN -> How may I assist you?");
    print("\t[1] Generate Curriculum Vitae PDF Documents")
    print("\t[2] Send Curriculum Vitae email to all target companies")
    print("\t[3] All of the above")
    choice = get_integer_input("Your choice: ")

    if choice==1 or choice == 3:
        print("<- MAIN -> Generating CVs...")
        generate_cv_for_companies(data, pdf_folder)
        print("<- MAIN -> Finished generating CVs!")
    if choice == 2 or choice == 3:
        print("<- MAIN -> Sending emails...")
        send_cv_email_to_companies(data, pdf_folder)
        print("<- MAIN -> Finished processing emails!")
    if choice not in [1,2,3]:
        print(f"<- FINISHED -> {data['name']}, you do not know how to read. Please do so before attempting to find a job. Aborting...")
        
    print("<- FINISHED -> Thank you for using JobFinder!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n<- FINISHED -> Process interrupted by the user. Thank you for using JobFinder!")
        sys.exit()
    finally:
        os.system('pause')