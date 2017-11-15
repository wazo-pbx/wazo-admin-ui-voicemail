# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

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
        users = [user['uuid'] for user in resource['users']]
        resource['user_uuid'] = users
        form = self.form(data=resource)
        return form

    def _populate_form(self, form):
        form.user_uuid.choices = self._build_set_choices_users(form.users)
        form.context.choices = self._build_set_choices_context(form.context)
        return form

    def _build_set_choices_context(self, context):
        if not context.data or context.data == 'None':
            return []
        return [(context.data, context.data)]

    def _build_set_choices_users(self, users):
        results = []
        for user in users:
            if user.lastname.data:
                text = '{} {}'.format(user.firstname.data, user.lastname.data)
            else:
                text = user.firstname.data
            results.append((user.uuid.data, text))
        return results

    def _map_form_to_resources(self, form, form_id=None):
        resource = super(VoicemailView, self)._map_form_to_resources(form, form_id)
        if form.user_uuid.data and form.user_uuid.data != 'None':
            resource['users'] = [{'uuid': form.user_uuid.data}]
        else:
            resource['users'] = []
        return resource

    def _map_resources_to_form_errors(self, form, resources):
        form.populate_errors(resources.get('voicemail', {}))
        return form


class VoicemailDestinationView(LoginRequiredView):

    def list_json(self):
        params = extract_select2_params(request.args)
        voicemails = self.service.list(**params)
        results = [{'id': vm['id'], 'text': vm['name']} for vm in voicemails['items']]
        return jsonify(build_select2_response(results, voicemails['total'], params))
