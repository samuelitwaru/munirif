import pandas as pd
from django.conf import settings
from reportlab.lib import colors 
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, ListFlowable, ListItem, Spacer, HRFlowable, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from bs4 import BeautifulSoup
from core.models import Section


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

def generate_financial_report_pdf(filename, data):
    """
    Generate a PDF financial report with nested expense tables.

    :param filename: Output PDF filename
    :param data: List of project financial dictionaries
    """

    downloads_folder = settings.MEDIA_ROOT / 'downloads'
    downloads_url = '/media/downloads'
    file_path = f'{downloads_folder}/{filename}'

    doc = SimpleDocTemplate(
        file_path, pagesize=A4, 
        rightMargin=20,
        leftMargin=20,
        topMargin=20,
        bottomMargin=20
    )
    elements = []
    styles = getSampleStyleSheet()

    for project in data:
        # === Project Title ===
        elements.append(Paragraph(f"<b>Project:</b> {project['title']}", styles["Heading2"]))
        # elements.append(Spacer(1, 0.2 * inch))

        # === Project Financial Summary Table ===
        summary_data = [
            ["Updated At", project["updated_at"]],
            ["Total Budget", project["total_budget"]],
            ["Budget Allocation", project["budget_allocation"]],
            ["Total Expenditure", project["total_expenditure"]],
            ["Unaccounted", f"{project['unaccounted']:,}"],
        ]

        summary_data = [
            ["Last Updated", "Total Budget", "Budget Expenditure", "Total Expenditure", "Unaccounted"],
            [project["updated_at"], project["total_budget"], project["budget_allocation"], project["total_expenditure"],f"{project['unaccounted']:,}"]
        ]

        summary_table = Table(summary_data, colWidths=[1.5 * inch], hAlign='LEFT')
        summary_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ]))

        elements.append(summary_table)
        elements.append(Spacer(1, 0.3))

        # === Expenses Title ===
        elements.append(Paragraph("<b>Expenses</b>", styles["Heading3"]))
        # elements.append(Spacer(1, 0.15 * inch))

        # === Expenses Nested Table ===
        expenses = project.get("expenses", [])

        expense_data = [[
            "Date", "Expense Category", "Item", "Qty", "Units", "Unit Cost", "Amount", "Remarks"
        ]]

        for exp in expenses:
            expense_data.append([
                exp["date"],
                exp["category"],
                exp["item"],
                exp["quantity"],
                exp["units"],
                f"{exp['unit_cost']:,}",
                f"{exp['amount']:,}",
                exp["remarks"] or "-"
            ])

        if len(expenses) == 0:
            expense_data.append(["No expenses found", "", "", "", "", "", ""])

        expense_table = Table(expense_data, repeatRows=1, hAlign='LEFT')

        if len(expenses) == 0:
            expense_data.append(["No expenses found", "", "", "", "", "", ""])
            expense_table.setStyle(TableStyle([
                ("ALIGN", (0, 1), (-1, -1), "CENTER"),
                ("SPAN", (0, 1), (-1, 1)),
            ]))

        expense_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("ALIGN", (1, 1), (4, -1), "RIGHT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))

        elements.append(expense_table)
        # elements.append(Spacer(1, 0.5 * inch))
        elements.append(
            HRFlowable(
                width="100%",      # or fixed width like 400
                thickness=1,
                color=colors.lightgrey,
                spaceBefore=10,
                spaceAfter=10
            )
        )

    # Build PDF
    doc.build(elements)
    downloads_url = settings.MEDIA_URL + 'downloads'
    return f'{downloads_url}/{filename}'