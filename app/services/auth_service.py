from app import db
from app.models import User
from app.utils.db import db_session
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from datetime import datetime

class AuthService:
    @staticmethod
    def register_user(username, email, password):
        try:
            with db_session() as session:
                existing_user = User.query.filter(
                    (User.username == username) | (User.email == email)
                ).first()
                
                if existing_user:
                    if existing_user.username == username:
                        return {'success': False, 'message': 'Username already taken'}, 400
                    else:
                        return {'success': False, 'message': 'Email already registered'}, 400
                
                new_user = User(username=username, email=email)
                new_user.set_password(password)
                
                session.add(new_user)
                session.commit()
                
                return {
                    'success': True,
                    'message': 'User registered successfully',
                    'user_id': new_user.id
                }, 201
        except IntegrityError:
            return {'success': False, 'message': 'Database error occurred'}, 500
        except Exception as e:
            return {'success': False, 'message': str(e)}, 500
    
    @staticmethod
    def login_user(username, password):
        try:
            user = User.query.filter_by(username=username).first()
            
            if not user or not user.check_password(password):
                return {'success': False, 'message': 'Invalid username or password'}, 401
            
            access_token = create_access_token(
                identity=str(user.id)  
            )
          
            return {
                'success': True,
                'message': 'Login successful',
                'access_token': access_token,
                'user_id': user.id,
                'is_admin': user.is_admin
            }, 200
        except Exception as e:
            return {'success': False, 'message': str(e)}, 500