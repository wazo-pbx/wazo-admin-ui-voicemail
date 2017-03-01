# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from wazo_admin_ui.helpers.service import BaseConfdService


class VoicemailService(BaseConfdService):

    resource = 'voicemail'
    confd_resource = 'voicemails'

    def create(self, resources):
        voicemail = resources.get(self.resource)
        user = voicemail.get('users')

        voicemail = self._confd.voicemails.create(voicemail)

        if user:
            self.add_voicemail_to_user(voicemail.get('id'), user)

    def update(self, resources):
        voicemail = resources.get(self.resource)
        user = voicemail.get('users')

        if user:
            voicemail_id = voicemail.get('id')
            self._confd.voicemails.relations(voicemail_id).remove_users()
            self.add_voicemail_to_user(voicemail_id, user)

        self._confd.voicemails.update(voicemail)

    def delete(self, id):
        voicemail = self._confd.voicemails.get(id)
        users = voicemail.get('users')

        if users:
            for user in users:
                self.delete_voicemail_to_user(id, user.get('uuid'))

        self._confd.voicemails.delete(voicemail)

    def get_users(self):
        return self._confd.users.list()

    def add_voicemail_to_user(self, voicemail_id, user_uuid):
        return self._confd.voicemails.relations(voicemail_id).add_user(user_uuid)

    def delete_voicemail_to_user(self, voicemail_id, user_uuid):
        return self._confd.voicemails.relations(voicemail_id).remove_user(user_uuid)
