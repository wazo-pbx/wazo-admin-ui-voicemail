# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from flask_menu.classy import classy_menu_item
from marshmallow import fields

from wazo_admin_ui.helpers.classful import BaseView, BaseDestinationView
from wazo_admin_ui.helpers.mallow import BaseSchema, BaseAggregatorSchema, extract_form_fields

from .form import VoicemailForm


class VoicemailSchema(BaseSchema):

    context = fields.String(default='default')

    class Meta:
        fields = extract_form_fields(VoicemailForm)


class AggregatorSchema(BaseAggregatorSchema):
    _main_resource = 'voicemail'

    voicemail = fields.Nested(VoicemailSchema)


class VoicemailView(BaseView):

    form = VoicemailForm
    resource = 'voicemail'
    schema = AggregatorSchema

    @classy_menu_item('.voicemails', 'Voicemails', order=4, icon="envelope")
    def index(self):
        return super(VoicemailView, self).index()

    def _map_resources_to_form(self, resources):
        users = self._get_user(resources['voicemail']['users'])
        return self.form(data=resources['voicemail'], users=users)

    def _get_user(self, users):
        return [user['uuid'] for user in users]


class VoicemailDestinationView(BaseDestinationView):

    def list_json(self):
        params = self._extract_params()
        voicemails = self.service.list(**params)
        results = [{'id': vm['id'], 'text': vm['name']} for vm in voicemails['items']]
        return self._select2_response(results, voicemails['total'], params)
