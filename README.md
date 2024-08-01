# JobFinder

**JobFinder** is a Python application designed to streamline the process of generating tailored CVs and sending personalized emails to potential employers. It utilizes the Gmail API for sending emails and allows users to configure their application using a `curriculum.json` file.

## Features

- **Customized CV Generation**: Create CV PDFs from a JSON template tailored for different job applications.
- **Personalized Email Sending**: Send emails to companies with customizable intervals and dynamic content.
- **Email Logging**: Log sent emails in a specified sub-folder with timestamped filenames.
- **Dynamic Content Support**: Use placeholders in emails for company-specific details to personalize each message.

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
                "logo": "Accenture.png",
                "email": "example@example.com",
                "position": "Software Engineer"
            }
        ],
        "avatar": "avatar.jpg",
        "name": "Your Name",
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

2. **Avatar Image**: Place an image named `avatar.jpg` or `avatar.png` in the same directory as `curriculum.json` to include your picture in the generated CV.

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
    - Download the `credentials.json` file and place it in the project directory.

### Running the Application

1. **Execute JobFinder**:
    - Run the application by executing `JobFinder.exe`.
    - Choose the desired option:
        1. Generate CVs
        2. Generate emails
        3. Generate both CVs and emails in sequence

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries or issues, please contact [Your Name](mailto:your.email@example.com).
