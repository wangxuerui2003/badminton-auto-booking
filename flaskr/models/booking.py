from flaskr.extensions import db
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class Booking(db.Model):
	id: Mapped[int] = mapped_column(primary_key=True)
	date: Mapped[datetime] = mapped_column(nullable=True)  # no repeat
	day_in_week: Mapped[str] = mapped_column(nullable=True)  # repeat every week
	time_start: Mapped[datetime] = mapped_column(nullable=False)
	time_end: Mapped[datetime] = mapped_column(nullable=False)

	def __repr__(self) -> str:
		return f"Book every {self.day_in_week} from {self.time_start} to {self.time_end}"

