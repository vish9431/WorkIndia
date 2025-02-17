from app import create_app, db
from app.models import User

def init_db():
    app = create_app()
    with app.app_context():
        db.create_all()
        
        admin = User.query.filter_by(is_admin=True).first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@example.com',
                is_admin=True
            )
            admin.set_password('admin123') 
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully.")
        else:
            print("Admin user already exists.")
        
        print("Database initialized successfully.")

if __name__ == '__main__':
    init_db()