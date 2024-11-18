from celery import shared_task 
import pandas as pd
from io import BytesIO
from .models import UserData
from django.core.mail import send_mail
from django.conf import settings
import sentry_sdk

sentry_sdk.init(
    dsn="https://0ab1dc58df87ac8b44e16e2bf835be1f@o4508296085372928.ingest.us.sentry.io/4508296098021376", 
      
)
@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=5, retry_kwargs={'max_retries': 5})
def process_csv(self,csv_data, user_email):
    """
    Process the uploaded CSV file using Pandas and save data to the database.
    Sends an email notification upon completion.
    """
    try:
        csv_file = BytesIO(csv_data)
        df = pd.read_csv(csv_file)

        required_columns = ['name', 'email', 'age']  
        if not all(column in df.columns for column in required_columns):
            raise ValueError(f"CSV must contain the columns: {', '.join(required_columns)}")


        user_data_entries = [
            UserData(name=row['name'], email=row['email'], age=row['age'])
            for _, row in df.iterrows()
        ]

    
        UserData.objects.bulk_create(user_data_entries)

        # Send completion notification
        send_mail(
            'CSV Processing Complete',
            f'Your CSV file has been processed successfully. {len(user_data_entries)} entries added to the database.',
            settings.EMAIL_HOST_USER,
            [user_email],
            fail_silently=False,
        )
        raise Exception("testing sentry")
        return f"Processed {len(user_data_entries)} entries."
    except Exception as e:
        sentry_sdk.capture_exception(e)
        

@shared_task()
def send_high_priority_email():
    """
    Send high-priority emails to users aged above 18.
    """
    print("Processing high-priority emails...")
    try:
    # Filter users aged greater than 18
        users = UserData.objects.filter(age__gt=18)
        
        for user in users:
            print(f"Sending high-priority email to {user.email , user.age}")
            # send_mail(
            #     'Welcome!',
            #     'You are eligible for our premium services.',
            #     settings.EMAIL_HOST_USER,
            #     [user.email],
            #     fail_silently=False,
            # )

        return f"High-priority emails sent to {len(users)} users."
    except Exception as exc:
        print(f"Error occurred: {exc}. Retrying...")
     


@shared_task 
def send_low_priority_email():
    """
    Send low-priority emails to users aged 18 or below.
    """
    try:
        print("Processing low-priority emails...")
        
        # Filter users aged 18 or below
        users = UserData.objects.filter(age__lte=18)
        
        for user in users:
            print(f"Sending low-priority email to {user.email , user.age}")
            # send_mail(
            #     'Welcome!',
            #     'Explore our services designed for young adults.',
            #     settings.EMAIL_HOST_USER,
            #     [user.email],
            #     fail_silently=False,
            # )
        return f"Low-priority emails sent to {len(users)} users."
    except Exception as e :
        print(e)