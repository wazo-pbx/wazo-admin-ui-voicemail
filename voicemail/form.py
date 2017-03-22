# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_wtf import FlaskForm

from wtforms.fields import SubmitField
from wtforms.fields import TextField
from wtforms.fields import SelectField
from wtforms.fields import BooleanField
from wtforms.fields.html5 import EmailField

from wtforms.validators import InputRequired
from wtforms.validators import Email


class VoicemailForm(FlaskForm):
    name = TextField('Name', [InputRequired()])
    number = TextField('Number', [InputRequired()])
    email = EmailField('Email', validators=[InputRequired(), Email()])
    password = TextField('Password')
    timezone = SelectField('Timezone',
                           validators=[InputRequired()],
                           choices=[
                               ('na-newfoundland', 'America/St_Johns'),
                               ('na-atlantic', 'America/Halifax'),
                               ('na-eastern', 'America/New_York'),
                               ('na-central', 'America/Chicago'),
                               ('na-mountain', 'America/Denver'),
                               ('na-pacific', 'America/Los_Angeles'),
                               ('na-alaska', 'America/Anchorage'),
                               ('eu-fr', 'Europe/Paris')
                           ])
    language = SelectField('Language',
                           validators=[InputRequired()],
                           choices=[
                               ('fr_FR', 'French'),
                               ('fr_CA', 'French Canadian'),
                               ('en_US', 'English'),
                           ])
    users = SelectField('Users', choices=[])
    max_messages = TextField('Maximum messages')
    ask_password = BooleanField('Ask for password')
    attach_audio = BooleanField('Attach audio')
    delete_messages = BooleanField('Delete message after notification')
    enabled = BooleanField('Activated')
    submit = SubmitField('Submit')
