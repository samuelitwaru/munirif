from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_html_email(request, subject, recipient_list, html_template, context):
    # Load the HTML template
    context['request'] = request
    html_message = render_to_string(html_template, context)
    if isinstance(recipient_list, list):
        recipient_list.append('gms@muni.ac.ug')
    # Create a plain text version of the HTML email
    plain_message = strip_tags(html_message)

    # Send the email
    print('sending', recipient_list)
    res = send_mail(
        subject,
        plain_message,
        'samuelitwaru@gmail.com',  # Sender's email
        recipient_list,
        html_message=html_message,  # HTML content of the email
        fail_silently=False,
    )
    print(res)