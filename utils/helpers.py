import pandas as pd
from django.conf import settings

def get_host_name(request):
    if request.is_secure():
        return f'https://{request.get_host()}'
    return f'http://{request.get_host()}'

def write_xlsx_file(file_name, columns, data):
    df = pd.DataFrame(data, columns=columns) 
    excel_file = settings.MEDIA_ROOT / f'downloads/{file_name}'
    df.to_excel(excel_file, index=False)
    return settings.MEDIA_URL + f'downloads/{file_name}'