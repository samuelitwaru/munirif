FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=munirif.settings

WORKDIR /app

COPY requirements.txt .

RUN python -m venv ../venv
RUN ../venv/bin/pip install --upgrade pip
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

RUN python manage.py migrate  
# RUN python manage.py loaddata groups.json section.json attachment.json department.json faculty.json qualification.json 
CMD ["gunicorn", "munirif.wsgi:application", "--timeout", "120", "--bind", "0.0.0.0:8000"]