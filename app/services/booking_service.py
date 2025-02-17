from app import db
from app.models import Train, Booking
from app.utils.db import db_session
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from sqlalchemy import and_, func, text

class BookingService:
    @staticmethod
    def book_seat(user_id, train_id, source, destination, booking_date, number_of_seats):
        try:
            with db_session() as session:
                train = Train.query.get(train_id)
                if not train:
                    return {'success': False, 'message': 'Train not found'}, 404
                
                if train.source != source or train.destination != destination:
                    return {'success': False, 'message': 'Invalid source or destination for this train'}, 400
                
                session.execute(text(f"SELECT * FROM trains WHERE id = :train_id FOR UPDATE"), {'train_id': train_id})
                
                booked_seats = Booking.query.filter(
                    and_(
                        Booking.train_id == train_id,
                        Booking.booking_date == booking_date,
                        Booking.status == 'CONFIRMED'
                    )
                ).count()
                
                available_seats = train.total_seats - booked_seats
                if available_seats < number_of_seats:
                    return {
                        'success': False,
                        'message': f'Not enough seats available. Only {available_seats} seats left',
                        'available_seats': available_seats
                    }, 400
                
                bookings = []
                for i in range(number_of_seats):
                    last_seat = Booking.query.filter(
                        and_(
                            Booking.train_id == train_id,
                            Booking.booking_date == booking_date
                        )
                    ).order_by(Booking.seat_number.desc()).first()
                    
                    next_seat = 1 if not last_seat else last_seat.seat_number + 1
                    
                    booking = Booking(
                        user_id=user_id,
                        train_id=train_id,
                        source=source,
                        destination=destination,
                        seat_number=next_seat,
                        booking_date=booking_date,
                        status='CONFIRMED'
                    )
                    session.add(booking)
                    bookings.append(booking)
                
                session.flush()
                
                booking_ids = [b.booking_id for b in bookings]
                
                return {
                    'success': True,
                    'message': f'Successfully booked {number_of_seats} seats',
                    'booking_ids': booking_ids,
                    'train_number': train.train_number,
                    'train_name': train.name,
                    'source': source,
                    'destination': destination,
                    'booking_date': booking_date.strftime('%Y-%m-%d'),
                    'seat_numbers': [b.seat_number for b in bookings]
                }, 201
        except IntegrityError:
            return {'success': False, 'message': 'Database error occurred'}, 500
        except Exception as e:
            return {'success': False, 'message': str(e)}, 500
    
    @staticmethod
    def get_booking_details(booking_id, user_id):
        try:
            booking = Booking.query.filter_by(booking_id=booking_id).first()
            
            if not booking:
                return {'success': False, 'message': 'Booking not found'}, 404
            
            # if booking.user_id != user_id:
            #     return {'success': False, 'message': 'Unauthorized to view this booking'}, 403
            
            train = Train.query.get(booking.train_id)
            
            return {
                'success': True,
                'booking_id': booking.booking_id,
                'train_number': train.train_number,
                'train_name': train.name,
                'source': booking.source,
                'destination': booking.destination,
                'seat_number': booking.seat_number,
                'booking_date': booking.booking_date.strftime('%Y-%m-%d'),
                'status': booking.status,
                'created_at': booking.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }, 200
        except Exception as e:
            return {'success': False, 'message': str(e)}, 500
    
    @staticmethod
    def get_user_bookings(user_id):
        try:
            bookings = Booking.query.filter_by(user_id=user_id).all()
            
            if not bookings:
                return {'success': True, 'message': 'No bookings found', 'bookings': []}, 200
            
            result = []
            for booking in bookings:
                train = Train.query.get(booking.train_id)
                
                result.append({
                    'booking_id': booking.booking_id,
                    'train_number': train.train_number,
                    'train_name': train.name,
                    'source': booking.source,
                    'destination': booking.destination,
                    'seat_number': booking.seat_number,
                    'booking_date': booking.booking_date.strftime('%Y-%m-%d'),
                    'status': booking.status,
                    'created_at': booking.created_at.strftime('%Y-%m-%d %H:%M:%S')
                })
            
            return {
                'success': True,
                'bookings': result
            }, 200
        except Exception as e:
            return {'success': False, 'message': str(e)}, 500