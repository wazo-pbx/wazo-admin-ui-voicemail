# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from wtforms.fields import (FieldList,
                            FormField,
                            HiddenField,
                            SubmitField,
                            StringField,
                            SelectField,
                            BooleanField)
from wtforms.fields.html5 import EmailField, IntegerField

from wtforms.validators import InputRequired, Length, NumberRange, Regexp

from wazo_admin_ui.helpers.destination import DestinationHiddenField
from wazo_admin_ui.helpers.form import BaseForm


class UserForm(BaseForm):
    uuid = HiddenField()
    firstname = HiddenField()
    lastname = HiddenField()


class VoicemailForm(BaseForm):
    name = StringField('Name', [InputRequired(), Length(max=80)])
    context = SelectField('Context', [InputRequired()], choices=[])
    number = StringField('Number', [InputRequired(), Length(max=40), Regexp(r'^[0-9]+$')])
    email = EmailField('Email', validators=[Length(max=80)])
    password = StringField('Password', [Length(max=80), Regexp(r'^[0-9]+$')], render_kw={'type': 'password',
                                                                                         'data_toggle': 'password'})
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
    users = FieldList(FormField(UserForm))
    user_uuid = SelectField('Users', choices=[])
    max_messages = IntegerField('Maximum messages', [NumberRange(min=0)])
    ask_password = BooleanField('Ask for password')
    attach_audio = BooleanField('Attach audio')
    delete_messages = BooleanField('Delete message after notification')
    enabled = BooleanField('Activated')
    submit = SubmitField('Submit')


class VoicemailDestinationForm(BaseForm):
    set_value_template = '{voicemail_name}'

    voicemail_id = SelectField('Voicemail', [InputRequired()], choices=[])
    greeting = SelectField('Greeting', choices=[('busy', 'Busy'), ('unavailable', 'Unavailable')])
    skip_instructions = BooleanField('Skip instructions')
    voicemail_name = DestinationHiddenField()