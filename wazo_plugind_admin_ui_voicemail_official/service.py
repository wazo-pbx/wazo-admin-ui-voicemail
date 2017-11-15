# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from wazo_admin_ui.helpers.service import BaseConfdService
from wazo_admin_ui.helpers.confd import confd


class VoicemailService(BaseConfdService):

    resource_confd = 'voicemails'

    def create(self, voicemail):
        voicemail = confd.voicemails.create(voicemail)
        for user in voicemail['users']:
            confd.voicemails(voicemail).add_user(user['uuid'])

    def update(self, voicemail):
        confd.voicemails(voicemail).remove_users()
        for user in voicemail['users']:
            confd.voicemails(voicemail).add_user(user['uuid'])

        confd.voicemails.update(voicemail)

    def delete(self, id):
        voicemail = confd.voicemails.get(id)
        for user in voicemail['users']:
            confd.voicemails(voicemail).remove_user(user['uuid'])

        confd.voicemails.delete(voicemail)

    def get_users(self):
        return confd.users.list()
