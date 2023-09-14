from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import (DataRequired, Length, ValidationError, Regexp,
                                Optional)

from .constants import (SHORT_LENGTH_END, ORIGINAL_LENGTH, SHORT_PATTERN)
from .models import URLMap

ORIGINAL_TEXT = 'Длинная ссылка'
ORIGINAL_MESSAGE = 'Обязательное поле'
SHORT_TEXT = 'Ваш вариант короткой ссылки'
SHORT_LENGTH_MESSAGE = 'Длина короткой ссылки до {} символов'
ORIGINAL_LENGTH_MESSAGE = 'Длина оригинальной ссылки до {} символов'
SUBMIT_MESSAGE = 'Добавить'
SHORT_ILLEGAL = 'Указано недопустимое имя для короткой ссылки'
SHORT_EXIST = 'Имя {} уже занято!'


class LinkForm(FlaskForm):
    original_link = StringField(
        ORIGINAL_TEXT,
        validators=[
            Length(
                max=ORIGINAL_LENGTH,
                message=ORIGINAL_LENGTH_MESSAGE.format(ORIGINAL_LENGTH)
            ),
            DataRequired(message=ORIGINAL_MESSAGE)
        ]
    )
    custom_id = StringField(
        SHORT_TEXT,
        validators=[
            Length(
                max=SHORT_LENGTH_END,
                message=SHORT_LENGTH_MESSAGE.format(SHORT_LENGTH_END)
            ),
            Regexp(
                SHORT_PATTERN,
                message=SHORT_ILLEGAL
            ),
            Optional(strip_whitespace=True)
        ]
    )
    submit = SubmitField(SUBMIT_MESSAGE)

    def validate_custom_id(form, field):
        if URLMap.get(field.data):
            raise ValidationError(SHORT_EXIST.format(field.data))
        return field.data
