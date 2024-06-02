from flaskr.extensions import db
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class Booking(db.Model):
	id: Mapped[int] = mapped_column(primary_key=True)
	date: Mapped[datetime] = mapped_column(nullable=True)  # no repeat
	day_in_week: Mapped[int] = mapped_column(nullable=True)  # 0-6, repeat every week
	time_from: Mapped[int] = mapped_column(nullable=False)  # 7 to 22
	time_to: Mapped[int] = mapped_column(nullable=False)  # 7 to 22

	def __repr__(self) -> str:
		if self.day_in_week is not None:
			return f"Book every {self.day_in_week} from {self.time_from} to {self.time_to}"
		return f"Book {self.date.strftime('%Y-%m-%d')} from {self.time_from} to {self.time_to}"
	
	def to_dict(self) -> dict:
		return {
			'id': self.id,
			'date': self.date.strftime('%Y-%m-%d'),
			'day_in_week': self.day_in_week,
			'time_from': self.time_from,
			'time_to': self.time_to,
		}

