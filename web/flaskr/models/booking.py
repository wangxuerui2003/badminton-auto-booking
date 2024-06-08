from flaskr.extensions import db
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class Booking(db.Model):
	id: Mapped[int] = mapped_column(primary_key=True)
	date: Mapped[datetime] = mapped_column(nullable=True)  # no repeat
	weekday: Mapped[int] = mapped_column(nullable=True)  # 0-6, repeat every week
	time_from: Mapped[int] = mapped_column(nullable=False)  # 7 to 22
	time_to: Mapped[int] = mapped_column(nullable=False)  # 7 to 22

	def __repr__(self) -> str:
		if self.weekday is not None:
			return f"Book every {self.weekday} from {self.time_from} to {self.time_to}"
		return f"Book {self.date.strftime('%Y-%m-%d')} from {self.time_from} to {self.time_to}"
	
	def to_dict(self) -> dict:
		return {
			'id': self.id,
			'date': self.date.strftime('%Y-%m-%d') if self.date else None,
			'weekday': self.weekday,
			'time_from': self.time_from,
			'time_to': self.time_to,
		}
	
	def is_past(self) -> bool:
		if self.date is None:
			return False
		return self.date < datetime.now()
	
	def is_repeated(self) -> bool:
		return self.weekday is not None

	@staticmethod
	def is_ongoing_task_query() -> bool:
		if Booking.date is None:
			return True
		return Booking.date >= datetime.now()

