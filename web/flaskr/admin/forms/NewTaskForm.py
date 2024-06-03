from flask import abort
from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, ValidationError


def weekday_to_int(weekday_str: str):
    if weekday_str is None:
        return None
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_int = weekdays.index(weekday_str)
    return weekday_int

class NewTaskForm(FlaskForm):
    date = DateField('Date (YYYY-MM-DD)', format='%Y-%m-%d')
    weekday = SelectField('Weekday', choices=[('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'), ('thursday', 'Thursday'), ('friday', 'Friday'), ('saturday', 'Saturday'), ('sunday', 'Sunday')])
    time_from = IntegerField('Time From (07-21)', validators=[DataRequired()])
    time_to = IntegerField('Time To (08-22)', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate(self, *args, **kwargs):
        super().validate(*args, **kwargs)
        
        date = self.date.data
        weekday = self.weekday.data
        time_from = self.time_from.data
        time_to = self.time_to.data

        if date and weekday:
            abort(422, description="Please input only date or only weekday.")

        if not date and not weekday:
            abort(422, description="Please input one of date or weekday.")

        if not (7 <= time_from <= 21):
            abort(422, description="Time From must be between 07 and 21.")

        if not (8 <= time_to <= 22):
            abort(422, description="Time To must be between 08 and 22.")

        if time_to - time_from > 2 or time_to - time_from < 1:
            abort(422, description="Invalid time_from and time_to combination.")

        self.weekday.data = weekday_to_int(self.weekday.data)

        return True
