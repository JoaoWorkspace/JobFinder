import os
import json
import templates.Base as template

def generate_cv_for_companies(data='curriculum.json',pdf_folder='output'):
    if data == 'curriculum.json':
        # Get data from the configuration file
        with open(configuration_file, 'r', encoding='utf-8') as file:
            data = json.load(file)

    # Allowed image extensions
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.pict')

    # Generates one custom PDF for each target company found
    companies = data.get('companies','')
    if companies:
        for company in companies:
            company_logo = company['logo']
            company_logo_path = f"logos/{company_logo}"
            company_name, ext = os.path.splitext(company_logo)
            if os.path.exists(company_logo_path) and ext.lower() in image_extensions:
                output_path = os.path.join(pdf_folder, f"curriculum_{company_name}.pdf")
                template.generate_pdf_from_json(output_path, data, company_logo_path)

    # Generates one final company agnostic curriculum
    template.generate_pdf_from_json(f'{pdf_folder}/curriculum.pdf', data)