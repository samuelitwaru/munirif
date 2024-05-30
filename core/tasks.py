from background_task import background
from django.contrib.auth.models import User
from core.models import *
from datetime import datetime, timedelta
from django.utils import timezone

@background(schedule=60)
def notify_user(user_id):
    # lookup user by id and send them a message
    user = User.objects.get(pk=user_id)
    user.email_user('Here is a notification', 'You have been notified')

@background
def delete_expired_invitations():
    now = timezone.now()
    lte_date = now - timedelta(7)
    print('lte_date = ', lte_date) 
    scores = Score.objects.filter(created_at__lte=lte_date)
    for score in scores:
        print(score)

@background
def submit_scores():
    now = timezone.now()
    scores = Score.objects.filter(status='ACCEPTED').all()
    for score in scores:
        if now >= score.accepted_at + timedelta(30):
            score.status = 'COMPLETED'
            score.save()
    


