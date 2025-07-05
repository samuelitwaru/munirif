import pandas as pd
from django.conf import settings
from reportlab.pdfgen import canvas 
from reportlab.pdfbase.ttfonts import TTFont 
from reportlab.pdfbase import pdfmetrics 
from reportlab.lib import colors 
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, ListFlowable, ListItem, Spacer, HRFlowable, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
import os
from bs4 import BeautifulSoup
from core.models import Section
import locale

def comma_separator(num):
    return "{:,}".format(num)



def clean_and_convert_html(html_content):
    html_content = clean_html(html_content)
    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    soup = BeautifulSoup(html_content, 'lxml')
    flowables = []
    # Iterate over the HTML elements
    if str(soup).strip():
        for element in soup.body:
            if element.name == 'p':
                flowables.append(Paragraph(str(element), styleN))
                flowables.append(Spacer(1, 12))
            elif element.name == 'ul':
                list_items = []
                for li in element.find_all('li'):
                    list_items.append(ListItem(Paragraph(str(li), styleN)))
                flowables.append(ListFlowable(list_items, bulletType='bullet'))
                flowables.append(Spacer(1, 12))

    return flowables

def clean_html(html_content):
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'lxml')
    # List of supported tags
    supported_tags = ['b', 'i', 'u', 'font', 'p', 'br', 'span', 'ul', 'li']
    # Remove unsupported tags while keeping their content
    for tag in soup.find_all(True):
        if tag.name not in supported_tags:
            tag.unwrap()
    # Remove all attributes
    for tag in soup.find_all(True):
        tag.attrs = {}

    # Return the cleaned HTML content
    return str(soup)


def get_host_name(request):
    if request.is_secure():
        return f'https://{request.get_host()}'
    return f'http://{request.get_host()}'

def write_xlsx_file(file_name, columns, data):
    df = pd.DataFrame(data, columns=columns) 
    excel_file = settings.MEDIA_ROOT / f'downloads/{file_name}'
    df.to_excel(excel_file, index=False)
    return settings.MEDIA_URL + f'downloads/{file_name}'


def write_proposal_pdf(file_name, proposal):
    downloads_folder = settings.MEDIA_ROOT / 'downloads'
    downloads_url = '/media/downloads'
    file_path = f'{downloads_folder}/{file_name}'

    # Create a PDF document
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    styleH1 = styles['Heading1']
    styleH2 = styles['Heading2']
    styleH3 = styles['Heading3']
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), 'gray'),
        ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, 'black'),
        ('BOX', (0, 0), (-1, -1), 0.25, 'black'),
    ])

    title_style = ParagraphStyle(
        'centered',
        parent=styles['Heading1'],
        alignment=1,  # 0=left, 1=center, 2=right
    )

    theme_style = ParagraphStyle(
        'centered',
        parent=styles['Heading2'],
        alignment=1,  # 0=left, 1=center, 2=right
    )
    line = HRFlowable(width="100%", thickness=1, lineCap='round', color="black")
    story.append(Paragraph('Title', title_style))
    story.append(Paragraph(f'{proposal.title}', title_style))
    story.append(line)
    story.append(Paragraph('Theme', theme_style))
    story.append(Paragraph(f'{proposal.theme}', theme_style))

    for section in Section.objects.all():
        story.append(Paragraph(f'<h3>{section.title}</h3><br/>', styleH3))
        if section.name == 'team':
            data = [['Full Name', 'Email', 'Telephone', 'Role']]
            for team in proposal.team_set.all():
                data.append([team.full_name, team.email, team.telephone, team.role])
            table = Table(data)
            table.setStyle(table_style)
            story.append(table)
        elif section.name == 'summary_budget':
            data = [['Item', 'Quantity', 'Units', 'Unit Cost', 'Total Cost']]
            total = 0
            for budg in proposal.budget_set.all():
                budg_total = budg.total_cost*budg.quantity
                data.append([budg.item, budg.quantity, budg.units, comma_separator(budg.total_cost), comma_separator(budg_total)])
                total += budg_total
            data.append(['Total', '','','', comma_separator(total)])
            table = Table(data)
            table.setStyle(table_style)
            story.append(table)
        else:
            flowables = clean_and_convert_html(getattr(proposal, section.name, '') or '')
            # story.append(Paragraph(content , styleN))
            story += flowables

    doc.build(story)
    return f'{downloads_url}/{file_name}'

