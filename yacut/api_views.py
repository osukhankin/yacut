from flask import jsonify, request, url_for

from . import app
from .constants import REDIRECTION_VIEW
from .error_handlers import InvalidApiData
from .exceptions import (ShortExist, EmptyApiParams, RequiredApiParam,
                         ShortIllegal, OriginalIllegal, ShortGenerationError)
from .models import URLMap

SHORT_NOT_FOUND = 'Указанный id не найден'
SQL_ERROR = 'Произошла ошибка - попробуйте позже!'
EMPTY_API_PARAMS = 'Отсутствует тело запроса'
REQUIRED_API_PARAM = '"{}" является обязательным полем!'
SHORT_EXIST = 'Имя "{}" уже занято.'


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    url_map = URLMap.get(short_id)
    if url_map is None:
        raise InvalidApiData(SHORT_NOT_FOUND.format(short_id), 404)
    return jsonify({'url': url_map.original}), 200


@app.route('/api/id/', methods=['POST'])
def add_short_link():
    data = request.get_json()
    if data is None:
        raise InvalidApiData(EMPTY_API_PARAMS)
    if 'url' not in data:
        raise InvalidApiData(REQUIRED_API_PARAM.format('url'))
    original = data.get('url')
    try:
        return jsonify(
            url=original,
            short_link=url_for(
                REDIRECTION_VIEW,
                short=URLMap.create(original, data.get("custom_id")).short,
                _external=True
            )
        ), 201
    except (
        EmptyApiParams, ShortExist, OriginalIllegal, ShortIllegal,
        RequiredApiParam, ShortGenerationError
    ) as error:
        raise InvalidApiData(str(error))
