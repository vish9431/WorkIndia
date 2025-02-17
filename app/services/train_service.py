from app import db
from app.models import Train, Booking
from app.utils.db import db_session
from sqlalchemy.exc import IntegrityError
from datetime import datetime

class TrainService:
    @staticmethod
    def add_train(data):
        try:
            with db_session() as session:
                existing_train = Train.query.filter_by(train_number=data['train_number']).first()
                if existing_train:
                    return {'success': False, 'message': 'Train with this number already exists'}, 400
                
                new_train = Train(
                    train_number=data['train_number'],
                    name=data['name'],
                    source=data['source'],
                    destination=data['destination'],
                    total_seats=data['total_seats'],
                    departure_time=data['departure_time'],
                    arrival_time=data['arrival_time']
                )
                
                session.add(new_train)
                session.commit()
                
                return {
                    'success': True,
                    'message': 'Train added successfully',
                    'train_id': new_train.id
                }, 201
        except IntegrityError:
            return {'success': False, 'message': 'Database error occurred'}, 500
        except Exception as e:
            return {'success': False, 'message': str(e)}, 500
    
    @staticmethod
    def get_availability(source, destination, date):
        try:
            trains = Train.query.filter_by(source=source, destination=destination).all()
            
            if not trains:
                return {'success': False, 'message': 'No trains available for this route'}, 404
            
            result = []
            for train in trains:
                booked_seats = Booking.query.filter_by(
                    train_id=train.id,
                    booking_date=date,
                    status='CONFIRMED'
                ).count()
                
                available_seats = train.total_seats - booked_seats
                
                result.append({
                    'train_id': train.id,
                    'train_number': train.train_number,
                    'name': train.name,
                    'source': train.source,
                    'destination': train.destination,
                    'departure_time': train.departure_time.strftime('%H:%M'),
                    'arrival_time': train.arrival_time.strftime('%H:%M'),
                    'total_seats': train.total_seats,
                    'available_seats': available_seats
                })
            
            return {
                'success': True,
                'trains': result
            }, 200
        except Exception as e:
            return {'success': False, 'message': str(e)}, 500
    
    @staticmethod
    def update_train_seats(train_id, new_total_seats):
        try:
            with db_session() as session:
                train = Train.query.get(train_id)
                
                if not train:
                    return {'success': False, 'message': 'Train not found'}, 404
                
                booked_seats = db.session.query(db.func.count(Booking.id)).filter_by(
                    train_id=train_id,
                    status='CONFIRMED'
                ).scalar()
                
                if new_total_seats < booked_seats:
                    return {
                        'success': False, 
                        'message': f'Cannot reduce seats below current bookings ({booked_seats})'
                    }, 400
                
                train.total_seats = new_total_seats
                
                return {
                    'success': True,
                    'message': 'Train seats updated successfully',
                    'train_id': train.id,
                    'new_total_seats': new_total_seats
                }, 200
        except Exception as e:
            return {'success': False, 'message': str(e)}, 500