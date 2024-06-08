from flaskr.extensions import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from datetime import datetime


class BookingHistory(db.Model):
	__tablename__ = 'booking_history'

	id: Mapped[int] = mapped_column(primary_key=True)
	target_date: Mapped[datetime] = mapped_column(nullable=True)
	booking_id: Mapped[int] = mapped_column(ForeignKey('booking.id'), nullable=False)
	created_at: Mapped[datetime] = mapped_column(default=datetime.now(), nullable=False)
	status: Mapped[str] = mapped_column(nullable=False)
	booking: Mapped['Booking'] = db.relationship('Booking', backref=db.backref('histories', lazy=True))

	def __repr__(self) -> str:
		return f"<BookingHistory {self.id} - At {self.created_at} - Status {self.status}>"
	
	def to_dict(self):
		return {
			"id": self.id,
			"target_date": self.target_date,
			"target_time_from": self.booking.time_from,
			"target_time_to": self.booking.time_to,
			"created_at": self.created_at.strftime("%Y-%m-%d, %H:%M:%S")
		}