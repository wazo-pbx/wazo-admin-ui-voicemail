# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from flask_menu.classy import classy_menu_item
from marshmallow import fields

from wazo_admin_ui.helpers.classful import BaseView
from wazo_admin_ui.helpers.mallow import BaseSchema, BaseAggregatorSchema, pre_dump

from .form import VoicemailForm


class UserSchema(BaseSchema):

    class Meta:
        fields = ('uuid',)


class VoicemailSchema(BaseSchema):

    class Meta:
        fields = ('name',
                  'number')


class AggregatorSchema(BaseAggregatorSchema):
    _main_resource = 'voicemail'

    voicemail = fields.Nested(VoicemailSchema)
    users = fields.Nested(UserSchema, many=True)

    @pre_dump
    def add_envelope(self, form):
        users = [{'uuid': uuid} for uuid in form.users.data]
        return {'switchboard': form,
                'users': users}


class VoicemailView(BaseView):

    form = VoicemailForm
    resource = 'voicemail'
    schema = AggregatorSchema

    @classy_menu_item('.voicemails', 'Voicemails', order=4, icon="envelope")
    def index(self):
        return super(VoicemailView, self).index()

    def _populate_form(self, form):
        users = self.service.get_users()
        form.users.choices = self._user_list(users['items'])
        return form

    def _map_resources_to_form(self, resources):
        data = self.schema().load(resources).data
        users = self._user_list(resources['voicemail']['users'])
        return self.form(data=resources['voicemail'], users=users)

    def _user_list(self, users):
        return [(user['uuid'], u"{} {}".format(user['firstname'], user['lastname']))
                 for user in users]
