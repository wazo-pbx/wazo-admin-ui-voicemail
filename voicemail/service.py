# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from wazo_admin_ui.helpers.service import BaseConfdService


class VoicemailService(BaseConfdService):

    resource = 'voicemail'
    confd_resource = 'voicemails'

    def create(self, resources):
        voicemail = resources.get(self.resource)
        voicemail = self._confd.voicemails.create(voicemail)

        user = resources.get('users')

        if user:
            self.add_voicemail_to_user(user['uuid'], voicemail['id'])

    def update(self, resources):
        voicemail = resources.get(self.resource)
        user = resources.get('users')

        if user:
            self.add_voicemail_to_user(user['uuid'], voicemail['id'])

        self._confd.voicemails.update(resource)

    def get_users(self):
        return self._confd.users.list()

    def add_voicemail_to_user(self, user_uuid, voicemail_id):
        return self._confd.users.relations(user_uuid).add_voicemail(voicemail_id)
