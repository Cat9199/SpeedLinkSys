from app import db, app, Dprice

# Create an application context
with app.app_context():
    # Create an instance of the Admins class
    info = Dprice(sid=1)

    # Add the instance to the database session
    db.session.add(info)
    
    # Commit the changes to the database
    db.session.commit()
