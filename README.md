

# JobFinder <img src="https://github.com/user-attachments/assets/c7f2cf41-a7f9-40e2-a975-b311c0d160c3" width="100">

**JobFinder** is a sophisticated Python application designed to streamline the creation of tailored CVs and the dispatch of personalized emails to potential employers. Utilizing the Gmail API for email delivery, JobFinder allows users to configure their application via a `curriculum.json` file, ensuring a highly customizable and efficient job application process.
<img src="https://github.com/user-attachments/assets/f3b67c42-90f0-4446-afa5-e88e8f98491d" width = 800>

*Sample obtained with `curriculum.json` provided and the base template*
## Features

- **Customized CV Generation**: Automatically create CV PDFs from a JSON template tailored for different job applications.
- **File Management**: CV generation will not overwrite existing files. Instead, it will append a GUID to the filenames to preserve multiple versions.
- **Personalized Email Dispatch**: Send customized emails to potential employers with configurable intervals and dynamic content.
- **Email Logging**: Maintain a log of sent emails in a specified sub-folder with timestamped filenames.
- **Dynamic Content Support**: Use placeholders in emails to personalize each message for specific companies.
- **Modular Template System**: Easily create and use custom templates for CV generation by defining a `generate_pdf_from_json` function.
- **Schema Validation**: Validate `curriculum.json` using a predefined schema to ensure data integrity and consistency.

## Usage

### Configuration

1. **`curriculum.json`**: This file contains the necessary information to generate your CV and send emails. Below is a sample schema:

    ```json
    {
        "minimumInterval": 30,
        "maximumInterval": 45,
        "message": {
            "opening": [
                "<p>Greetings {company} Team,</p>"
            ],
            "constant": [
                "<p>Noticed you have a vacancy for {position}.<br><b>DISCLAIMER:</b> I am available to work after 17pm[UTC] and before 9am[UTC] exclusively at the moment.</p>"
            ],
            "variable": [
                "<p>I believe my skills and experiences align well with {company}’s needs, and I am eager to contribute to your team.</p>"
            ],
            "ending": [
                "<p>I left my CV in attachment for your review. I look forward to the opportunity to discuss my qualifications further.</p>",
                "<p>Best regards,<br>{name}</p>"
            ]
        },
        "companies": [
            {
                "logo": "GitHub.png",
                "email": "example@example.com",
                "position": "Software Architect"
            }
        ],
        "avatar": "avatar.jpg",
        "name": "John Doe",
        "title": "Your Title",
        "about": [
            "Brief description about yourself."
        ],
        "contact": {
            "address": "Your Address",
            "phone": "Your Phone Number",
            "email": "your.email@example.com",
            "linkedin": "https://linkedin.com/in/yourprofile",
            "github": "https://github.com/yourprofile"
        }
    }
    ```

2. **Avatar Image**:
    - The avatar image can be named anything and placed in any directory, as long as the correct path is specified in `curriculum.json`.
    - **Supported Formats**: When using the Image class in ReportLab's `reportlab.platypus` module, the following image formats are supported:
        - **JPEG/JPG**: Ideal for photographic images.
        - **PNG**: Supports transparency and is lossless.
        - **GIF**: Primarily for simple graphics and animations.
        - **BMP**: Generally uncompressed.
        - **TIFF/TIF**: Often used for high-quality images.
        - **PICT**: Macintosh Picture format, though less common.

3. **Company Information**:
    - **Logo**: The company logo is mandatory. It must be placed in the `logos` sub-folder of your executable. The filename of the logo image is used to parse the company's name (e.g., `Accenture.png` will be associated with the company name "Accenture").
    - **Email**: The email address is required as it serves as the target recipient for the application email. 
    - **Position**: The position you're applying for is mandatory. It is used both in the body of the email and in the email subject line to tailor the message to the specific job opening.

4. **Introductory Information**:
   - All three of these are required in order to function: [Name, Title, About]
     
5. **Contact Information**: 
    - **Address**: Your address.
    - **Phone**: Your phone number.
    - **Email**: Your email address.
    - **Linkedin**: LinkedIn profile URL.
    - **Github**: GitHub profile URL.
   
6. **Experience Information**: Array of experience objects
    - **Title**: Job title.
    - **Team**: Team name.
    - **Company**: Company name.
    - **Date**: Employment date.
    - **Sectors**: Array of sectors worked in.
    - **Technologies**: Array of technologies used.

7. **Education**: Array of education objects
    - **Degree**: Degree name.
    - **Institution**: Institution name.
    - **Date**: Graduation date.

8. **Certificates**: Array of certificate objects
    - **Name**: Certificate name.
    - **Authority**: Issuing authority.
    - **Date**: Certification date.

9. **Projects**: Array of project objects
    - **Title**: Project title.
    - **Description**: Array of strings or a single string describing the project.

10. **Skills**: Object containing skill ratings:
    - **Technical**: Sub-object with various technical skills.
    - **Leadership and Management**: Sub-object with leadership and management skills.
    - **Soft**: Sub-object with soft skills.

11. **Languages**: Object with language proficiency levels.

**Pro Tip**: *Guiding yourself with the sampled `curriculum.json` will facilitate.*

## Template Customization

1. **Create a Custom Template:** Define a `generate_pdf_from_json` function in your custom template.
2. **Update the Import:** Change the import statement in `GenerateCV.py` to use your custom template:
    ```python
    import templates.Base as template  # Original import
    import templates.MyCustom as template  # Custom template import
    ```
3. **Run `MakeExecutable.ps1`:** It will automatically recompile your python scripts and remake `JobFinder.exe`.

### CV Generation Process

- **Multiple Versions**: Every time the CV Generator runs, it creates both a tailored CV for each company listed in curriculum.json and a default CV without a custom watermark. Files are saved with a GUID suffix to prevent overwriting existing files, allowing multiple versions to coexist.
- **Multiple Versions**: Each time the CV Generator runs, it will create both a customized CV for each company listed in `curriculum.json` and a default CV without a custom watermark. Existing files are not overwritten; instead, a GUID is suffixed to the filename, allowing multiple versions of your CV to coexist.
- **File Naming**: Generated CVs will have filenames in the format `curriculum_companyName_GUID.pdf`.

### Email Sending Process

- **Latest Files**: When sending emails, the code will select the latest files generated for each company.
- **Email Attachments**: When sending emails, the most recent CV files are used. Although the filenames may include a GUID (e.g., `curriculum_companyName_GUID.pdf`), the attachment in the email is named without the GUID (e.g., `curriculum_companyName.pdf`).

### Setup Google Cloud Console for Gmail API

1. **Create a New Project**:
    - Navigate to the [Google Cloud Console](https://console.cloud.google.com/).
    - Create a new project.

2. **Enable Gmail API**:
    - Go to the "API & Services" dashboard.
    - Click on "Enable APIs and Services" and search for "Gmail API".
    - Enable the Gmail API for your project.

3. **Create Credentials**:
    - Go to "Credentials" and click "Create Credentials".
    - Select "OAuth 2.0 Client IDs" and configure the consent screen.
  
4. **Set the OAuth Scope**:
    - When configuring OAuth consent, ensure that the scope `/auth/gmail.modify` is included. This scope allows the application to read and modify Gmail messages and labels, which is necessary for sending and managing emails.

5. **Download and Place `credentials.json`**:
    - Download the `credentials.json` file from the [Google Cloud Console](https://console.cloud.google.com/).
    - Place the `credentials.json` file in the same directory as the executable (e.g., `JobFinder.exe`). This ensures the application can access the necessary credentials for authentication with the Gmail API.

### Running the Application

- **Execute JobFinder**:
    - Run the application by executing `JobFinder.exe`.
    - Choose the desired option:
        - [1] **Generate CVs**
        - [2] **Generate emails**
        - [3] **Generate both CVs and emails in sequence**
     
### I/O Behavior and Error Handling
When running the application, you may encounter specific behaviors and error messages. Here is an example output of a successful e-mail process run:
```plaintext
<- MAIN -> Analyzing your 'curriculum.json' data...
<- MAIN -> Data is valid.
<- MAIN -> Welcome to JobFinder John Doe! Type the corresponding number in order to select an option.
<- MAIN -> How may I assist you?
        [1] Generate Curriculum Vitae PDF Documents
        [2] Send Curriculum Vitae email to all target companies
        [3] All of the above
Your choice: 2
<- MAIN -> Sending emails...
<- EMAIL GENERATOR -> ERROR: Interval Minimum of 0 minutes is lower than 30 minutes!
<- EMAIL GENERATOR -> Applying default values instead...
<- EMAIL GENERATOR -> ERROR: Interval Maximum of 0 minutes is lower than 30 minutes!
<- EMAIL GENERATOR -> Applying default values instead...
<- EMAIL GENERATOR -> Interval set to 30 - 60 minutes
<- EMAIL GENERATOR -> Do you wish to use your.email@gmail.com as your sender email?
        [1] Yes
        [2] No
Your choice: 1
<- EMAIL GENERATOR -> GMail detected. Attempting to authenticate and send emails through GMail API...
<- EMAIL GENERATOR -> Successfully authenticated GMail! Sending...
<- EMAIL GENERATOR -> Company: GitHub, Position: Software Architect, BaseCV: output\curriculum_GitHub.pdf
<- EMAIL GENERATOR -> Most recent company CV found: output\curriculum_curriculum_GitHub_04537dcefa814746aeda65497e17614e.pdf
<- EMAIL GENERATOR -> Email body:
    <html>
    <body>
        <p>Greetings GitHub Team,</p>
        <p>Noticed you have a vacancy for Software Architect.<br><b>DISCLAIMER:</b> I am available to work after 17pm[UTC] and before 9am[UTC] exclusively at the moment.</p>
        <p>My background has prepared me well to contribute to GitHub.</p>
        <p>I left my CV in attachment for your review. I look forward to the opportunity to discuss my qualifications further.</p><p>Best regards,<br>John Doe</p>
    </body>
    </html>

<- EMAIL GENERATOR -> Email sent to example@example.com
<- EMAIL GENERATOR -> Waiting 46 minutes before sending the next email.

<- FINISHED -> Process interrupted by the user. Exiting...
Press any key to continue . . .
```
*Note: I interrupt the process with Ctrl+C after the first e-mail is sent in the example.* 
## License

This project is licensed under the GNU General Public License - see the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries or issues, please contact [JoaoWorkspace](mailto:joao.workspace@gmail.com).
