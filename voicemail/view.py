# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from flask import jsonify, request
from flask_menu.classy import classy_menu_item

from wazo_admin_ui.helpers.classful import BaseView, LoginRequiredView
from wazo_admin_ui.helpers.classful import extract_select2_params, build_select2_response

from .form import VoicemailForm


class VoicemailView(BaseView):

    form = VoicemailForm
    resource = 'voicemail'

    @classy_menu_item('.voicemails', 'Voicemails', order=4, icon="envelope")
    def index(self):
        return super(VoicemailView, self).index()

    def _map_resources_to_form(self, resource):
        users = self._get_user(resource['users'])
        form = self.form(data=resource, users=users)
        form.users.choices = self._build_setted_choices(resource['users'])
        return form

    def _get_user(self, users):
        return [user['uuid'] for user in users]

    def _build_setted_choices(self, users):
        results = []
        for user in users:
            if user.get('lastname'):
                text = '{} {}'.format(user.get('firstname'), user['lastname'])
            else:
                text = user.get('firstname')
            results.append((user['uuid'], text))
        return results

    def _map_resources_to_form_errors(self, form, resources):
        form.populate_errors(resources.get('voicemail', {}))
        return form


class VoicemailDestinationView(LoginRequiredView):

    def list_json(self):
        params = extract_select2_params(request.args)
        voicemails = self.service.list(**params)
        results = [{'id': vm['id'], 'text': vm['name']} for vm in voicemails['items']]
        return jsonify(build_select2_response(results, voicemails['total'], params))
