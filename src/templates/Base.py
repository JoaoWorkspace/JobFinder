import os
import uuid
from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4, A3
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Frame, FrameBreak, PageTemplate, Image

def generate_pdf_from_json(output_pdf, data, company_logo=''):

    def halve(number):
        return number/2

    def ensure_directory_exists(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def get_unique_filename(filename):
        directory = os.path.dirname(filename)
        base, ext = os.path.splitext(filename)
        ensure_directory_exists(directory)
        while True:
            try:
                with open(filename, 'x'):
                    return filename
            except (FileExistsError, PermissionError):
                new_guid = uuid.uuid4().hex
                filename = f"{base}_{new_guid}{ext}"

    # Draw the background on the document (including a custom watermark)
    def draw_background(canvas, document):
        canvas.saveState()

        # Draw Grey Rectangle Background on Left Frame
        canvas.setFillColorRGB(0.91, 0.91, 0.91)
        rectangleX = document.leftMargin - docMiddleMargin
        rectangleY = document.bottomMargin
        rectangleWidth =  halve(document.width) + docMiddleMargin
        rectangleHeight = document.height
        canvas.rect(rectangleX, rectangleY, rectangleWidth, rectangleHeight, fill=True, stroke=False)
        
        # Draw White Circular Background to whiten out the Left Frame
        canvas.setFillColorRGB(1, 1, 1)
        circleX = document.leftMargin + halve(halve(document.width))
        circleY = document.height + 200
        circuleRadius = 255
        canvas.circle(circleX, circleY, circuleRadius, fill=True, stroke=False)

        # Draw Company Logo if exists
        if company_logo:
            # Create transparent image with 10% opacity
            transparent_logo_path = create_transparent_image(company_logo, 0.1)  
            watermark = Image(transparent_logo_path)
            img_width = min(watermark.drawWidth, round(halve(frameWidth),0))
            img_height = round(watermark.drawHeight * (img_width / watermark.drawWidth),0)
            img_x = document.width-halve(frameWidth-halve(img_width)-docMiddleMargin)
            img_y = halve(frameWidth)
            canvas.drawImage(transparent_logo_path, img_x, img_y, img_width, img_height, mask='auto')
            # Clean up the temporary file
            os.remove(transparent_logo_path)
            print(f"<- CV GENERATOR ->  Watermark applied for {os.path.split(os.path.splitext(company_logo)[0])[1]}.")

        canvas.restoreState()

    # Create a transparent image with given opacity
    def create_transparent_image(image_path, opacity):
        image = PILImage.open(image_path).convert("RGBA")
        alpha = image.split()[3]
        alpha = alpha.point(lambda p: p * opacity)
        image.putalpha(alpha)
        temp_image_path = f"temp_{os.path.basename(image_path)}"
        image.save(temp_image_path)
        return temp_image_path

    # Custom css styles
    name_style = ParagraphStyle(
        name='NameStyle',
        fontSize=18,
        leading=10,
        spaceAfter=10,
        textColor=colors.HexColor("#333333"),
        fontName='Helvetica-Bold'
    )

    title_style = ParagraphStyle(
        name='TitleStyle',
        fontSize=14,
        leading=18,
        spaceAfter=8,
        textColor=colors.HexColor("#666666"),
        fontName='Helvetica-Bold'
    )

    header_style = ParagraphStyle(
        name='HeaderStyle',
        fontSize=12,
        leading=7,
        spaceAfter=7,
        textColor=colors.HexColor("#00686E"),
        fontName='Helvetica-Bold'
    )

    normal_style = ParagraphStyle(
        name='NormalStyle',
        fontSize=10,
        leading=10,
        spaceAfter=0,
        textColor=colors.HexColor("#333333"),
        fontName='Helvetica'
    )

    bulletpoint_style = ParagraphStyle(
        name='NormalStyle',
        fontSize=9,
        leading=10,
        spaceAfter=10,
        textColor=colors.HexColor("#333333"),
        fontName='Helvetica'
    )

    detail_style = ParagraphStyle(
        name='NormalStyle',
        fontSize=10,
        leading=10,
        spaceAfter=0,
        textColor=colors.HexColor("#333333"),
        fontName='Times-Roman'
    )

    minimal_style = ParagraphStyle(
        name='NormalStyle',
        fontSize=8,
        leading=7,
        spaceAfter=10,
        textColor=colors.HexColor("#333333"),
        fontName='Times-Roman'
    )

    wrapped_header_style = ParagraphStyle(
        name='ButtonStyle',
        fontSize=8,
        textColor=colors.white,
        backColor=colors.HexColor("#00686E"),
        borderPadding=(6, 6),
        borderWidth=1,  
        borderRadius=4,  
        borderColor=colors.black,  
        spaceAfter=5,  
        wordWrap='CJK',  
        fontName='Helvetica-Bold'
    )

    wrapped_blue_style = ParagraphStyle(
        name='ButtonStyle',
        fontSize=8,  # Adjust font size as needed
        textColor=colors.black,  # Adjust text color as needed
        backColor=colors.HexColor("#D6EAF8"),  # Adjust background color as needed
        borderPadding=(6, 6),  # Adjust padding around text
        borderWidth=1,  # Adjust border width
        borderRadius=4,  # Adjust border radius for rounded corners
        borderColor=colors.black,  # Adjust border color as needed
        spaceAfter=5,  # Adjust space after each button
        wordWrap='CJK',  # Enable word wrapping
        fontName='Helvetica-Bold'
    )

    # Generate our output file name and sets it as a SimpleDocTemplate
    output_pdf = get_unique_filename(output_pdf)
    doc = SimpleDocTemplate(output_pdf, pagesize=A3)
    styles = getSampleStyleSheet()

    # Array of PDF Elements that compose the CV
    curriculumVitae = []

    # Create frame for two-column layout
    docMiddleMargin = 6
    frameWidth = halve(doc.width) - docMiddleMargin
    frameLeft = Frame(doc.leftMargin, doc.bottomMargin, frameWidth, doc.height, id='left')
    frameRight = Frame(doc.leftMargin + halve(doc.width) + docMiddleMargin, doc.bottomMargin, frameWidth, doc.height, id='right')
    template = PageTemplate(id='twoColumn', frames=[frameLeft, frameRight], onPage=draw_background)
    doc.addPageTemplates([template])

    # Avatar Section
    profile_image_path = data.get('avatar', '')
    if os.path.exists(profile_image_path):
        avatar = Image(profile_image_path)
        avatar.hAlign = 'CENTER'
        # Adjust image width and height as needed
        img_width = min(avatar.drawWidth, halve(frameWidth))
        img_height = avatar.drawHeight * (img_width / avatar.drawWidth)
        avatar.drawWidth = img_width
        avatar.drawHeight = img_height
        curriculumVitae.append(avatar)
        curriculumVitae.append(Spacer(1, 0.1*inch))

    # Name and Title
    curriculumVitae.append(Paragraph(data.get('name', 'Your Name'), name_style))
    curriculumVitae.append(Paragraph(data.get('title', 'Your Title'), title_style))

    # Contact Information
    contact = data.get('contact', {})
    contact_info = f"<b>Address:</b> {contact.get('address','')}<br/><b>Phone:</b> {contact.get('phone','')}<br/><b>Email:</b> {contact.get('email','')}<br/><b>LinkedIn:</b> {contact.get('linkedin','')}<br/><b>GitHub:</b> {contact.get('github','')}"
    curriculumVitae.append(Paragraph(contact_info, detail_style))

    # About Me Section
    about = data.get('about', [])
    if about:
        curriculumVitae.append(Paragraph(f"<br/>ABOUT ME", header_style))
        about_me = ' '.join(about)
        curriculumVitae.append(Paragraph(about_me, normal_style))

    # Experience Section
    experience = data.get('experience', [])
    if experience:
        curriculumVitae.append(Paragraph(f"<br/>EXPERIENCE", header_style))
        for item in experience:
            experience_story = f"<b>{item.get('title', '')} at {item.get('company', '')}'s</b> {item.get('team','')} Team<br/>"
            curriculumVitae.append(Paragraph(experience_story, detail_style))
            curriculumVitae.append(Paragraph(f"{item.get('date','')}", minimal_style))
            if 'sectors' in item:
                skills = " | ".join(item['sectors'])
                curriculumVitae.append(Paragraph(skills, wrapped_header_style))
            if 'technologies' in item:
                skills = " | ".join(item['technologies'])
                curriculumVitae.append(Paragraph(skills, wrapped_blue_style))
            curriculumVitae.append(Spacer(1, 0.1 * inch))

    # END OF LEFT FRAME / START OF RIGHT FRAME
    curriculumVitae.append(FrameBreak())

    # Education Section
    education = data.get('education', [])
    if education:
        curriculumVitae.append(Paragraph(f"<br/>EDUCATION", header_style))
        edu_content = [f"<b>{edu.get('degree', '')}</b> from {edu.get('institution', '')} <i>({edu.get('date', '')})</i>" for edu in education]
        for degree in edu_content:
            curriculumVitae.append(Paragraph(degree, normal_style))
            curriculumVitae.append(Spacer(1, 0.1 * inch))

    # Certificates Section
    certificates = data.get('certificates', [])
    if certificates:
        curriculumVitae.append(Paragraph("<br/>CERTIFICATES", header_style))
        for certificate in certificates:
            certificate_story = f"<b>{certificate.get('name','Unknown')}</b> by {certificate.get('authority','Unknown')}"           
            curriculumVitae.append(Paragraph(certificate_story, normal_style))
            curriculumVitae.append(Paragraph(f"{certificate.get('date','')}", minimal_style))

    # Projects Section
    projects = data.get('projects', [])
    if projects:
        curriculumVitae.append(Paragraph("<br/>PROJECTS", header_style))
        for project in projects:
            project_story = f"<b>{project.get('title','')}</b><br/>"
            if 'description' in project:
                if isinstance(project['description'], list):
                    description_list = f"<br/> • ".join(project['description'])
                    project_story += f" • {description_list}"
                else:
                    project_story += f" • {project.get('description')}"
            curriculumVitae.append(Paragraph(project_story, bulletpoint_style))

    # Skills Section
    skills = data.get('skills', {})
    if skills:
        curriculumVitae.append(Paragraph("<br/>SKILLS", header_style))
        curriculumVitae.append(Paragraph(f"● = Junior<br/>●● = Intermediate<br/>●●● = Senior<br/>●●●● = Expert<br/>●●●●● = Master", minimal_style))
        for skill_type, type_skills in skills.items():
            skill_type_paragraph = Paragraph(f"{skill_type} Skills", header_style)
            curriculumVitae.append(skill_type_paragraph)
            for skill, level in type_skills.items():
                dots = '●' * level
                skill_paragraph = Paragraph(f"{skill}: {dots}", detail_style)
                curriculumVitae.append(skill_paragraph)
            curriculumVitae.append(Spacer(1, 0.1 * inch))

    # Languages Section
    languages = data.get('languages', {})
    if languages:
        curriculumVitae.append(Paragraph("<br/>LANGUAGES", header_style))
        curriculumVitae.append(Paragraph(f"★ = A1<br/>★★★★★ = C1", minimal_style))
        for language, level in languages.items():
            stars = '★' * level
            language_paragraph = Paragraph(f"{language}: {stars}", detail_style)
            curriculumVitae.append(language_paragraph)
        curriculumVitae.append(Spacer(1, 0.1 * inch))

    doc.build(curriculumVitae)