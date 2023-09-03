# from app import db, app, Admins

# # Create an application context
# with app.app_context():
#     # Create an instance of the Admins class
#     info = Admins(username='admin',password='123')

#     # Add the instance to the database session
#     db.session.add(info)
    
#     # Commit the changes to the database
#     db.session.commit()
import datetime
import pytz

def get_current_time():
    egypt_timezone = pytz.timezone('Africa/Cairo')
    current_time = datetime.datetime.now(egypt_timezone)
    current_time = current_time.replace(microsecond=0, tzinfo=None)
    return current_time
print(get_current_time())