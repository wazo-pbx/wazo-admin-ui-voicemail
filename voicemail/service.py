# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from wazo_admin_ui.helpers.service import BaseConfdService
from wazo_admin_ui.helpers.confd import confd


class VoicemailService(BaseConfdService):

    resource_name = 'voicemail'
    resource_confd = 'voicemails'

    def create(self, resources):
        voicemail = resources.get('voicemail')
        user = voicemail.get('users')

        voicemail = confd.voicemails.create(voicemail)

        if user:
            self.add_voicemail_to_user(voicemail.get('id'), user)

    def update(self, resources):
        voicemail = resources.get('voicemail')
        user = voicemail.get('users')

        if user:
            voicemail_id = voicemail.get('id')
            confd.voicemails.relations(voicemail_id).remove_users()
            self.add_voicemail_to_user(voicemail_id, user)

        confd.voicemails.update(voicemail)

    def delete(self, id):
        voicemail = confd.voicemails.get(id)
        users = voicemail.get('users')

        if users:
            for user in users:
                self.delete_voicemail_to_user(id, user.get('uuid'))

        confd.voicemails.delete(voicemail)

    def get_users(self):
        return confd.users.list()

    def add_voicemail_to_user(self, voicemail_id, user_uuid):
        return confd.voicemails.relations(voicemail_id).add_user(user_uuid)

    def delete_voicemail_to_user(self, voicemail_id, user_uuid):
        return confd.voicemails.relations(voicemail_id).remove_user(user_uuid)
