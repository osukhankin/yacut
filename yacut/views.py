from flask import render_template, flash, redirect, url_for

from . import app
from .constants import REDIRECTION_VIEW
from .exceptions import (EmptyApiParams, ShortExist, OriginalIllegal,
                         ShortIllegal, RequiredApiParam, ShortGenerationError)
from .forms import LinkForm
from .models import URLMap

FLASH_ERROR = 'Произошла ошибка - попробуйте позже!'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = LinkForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        return render_template(
            'index.html',
            form=form,
            short=url_for(
                REDIRECTION_VIEW,
                short=URLMap.create(
                    form.original_link.data,
                    form.custom_id.data,
                    validation=False).short,
                _external=True),
        )
    except (
        EmptyApiParams, ShortExist, OriginalIllegal,
        ShortIllegal, RequiredApiParam, ShortGenerationError
    ) as error:
        flash(str(error))
        return render_template('index.html', form=form)


@app.route('/<string:short>')
def redirection_view(short):
    return redirect(URLMap.get_or_404(short).original)
