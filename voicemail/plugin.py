# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_menu.classy import register_flaskview

from wazo_admin_ui.helpers.plugin import create_blueprint

from .service import VoicemailService
from .view import VoicemailView

voicemail = create_blueprint('voicemail', __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']
        config = dependencies['config']

        VoicemailView.service = VoicemailService(config['confd'])
        VoicemailView.register(voicemail, route_base='/voicemails')
        register_flaskview(voicemail, VoicemailView)

        core.register_blueprint(voicemail)
