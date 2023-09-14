import random
import re
from datetime import datetime
from urllib.parse import urlparse

from yacut import db
from .constants import (SHORT_SYMBOLS,
                        SHORT_LENGTH_START, NUMBER_OF_ATTEMPTS,
                        SHORT_LENGTH_END, SHORT_PATTERN, ORIGINAL_LENGTH)
from .exceptions import (ShortIllegal, OriginalIllegal, ShortGenerationError,
                         ShortExist)

EMPTY_API_PARAMS = 'Отсутствует тело запроса'
REQUIRED_API_PARAM = '"{}" является обязательным полем!'
SHORT_ILLEGAL = 'Указано недопустимое имя для короткой ссылки'
SHORT_EXIST = 'Имя "{}" уже занято.'
ORIGINAL_ILLEGAL = 'Указана недопустимая оригинальная ссылка'
SHORT_GENERATION_ERROR = 'Произошла ошибка - воспользуйтесь сервисом повторно'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_LENGTH), nullable=False)
    short = db.Column(
        db.String(SHORT_LENGTH_END),
        unique=True,
        nullable=False,
        index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def get_or_404(short):
        return URLMap.query.filter_by(short=short).first_or_404()

    @staticmethod
    def get_unique_short(number_of_attempts):
        for attempt in range(number_of_attempts):
            short = ''.join(
                random.choices(SHORT_SYMBOLS, k=SHORT_LENGTH_START)
            )
            if not URLMap.get(short):
                return short
        raise ShortGenerationError(SHORT_GENERATION_ERROR)

    @staticmethod
    def create(original, short, validation=True):
        if short is None or not short:
            short = URLMap.get_unique_short(NUMBER_OF_ATTEMPTS)
        elif validation:
            if len(short) > SHORT_LENGTH_END:
                raise ShortIllegal(SHORT_ILLEGAL)
            if URLMap.get(short):
                raise ShortExist(SHORT_EXIST.format(short))
            if re.match(SHORT_PATTERN, short) is None:
                raise ShortIllegal(SHORT_ILLEGAL)
        if validation:
            if len(original) > ORIGINAL_LENGTH:
                raise OriginalIllegal(ORIGINAL_ILLEGAL)
            parsed_url = urlparse(original)
            if not (parsed_url.scheme and parsed_url.netloc):
                raise OriginalIllegal(ORIGINAL_ILLEGAL)
        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map
