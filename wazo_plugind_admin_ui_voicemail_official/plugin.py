# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_menu.classy import register_flaskview

from wazo_admin_ui.helpers.plugin import create_blueprint
from wazo_admin_ui.helpers.destination import register_destination_form, register_listing_url

from .service import VoicemailService
from .view import VoicemailView, VoicemailDestinationView
from .form import VoicemailDestinationForm

voicemail = create_blueprint('voicemail', __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']

        VoicemailView.service = VoicemailService()
        VoicemailView.register(voicemail, route_base='/voicemails')
        register_flaskview(voicemail, VoicemailView)

        VoicemailDestinationView.service = VoicemailService()
        VoicemailDestinationView.register(voicemail, route_base='/voicemails_listing')

        register_destination_form('voicemail', 'Voicemail', VoicemailDestinationForm)

        register_listing_url('voicemail', 'voicemail.VoicemailDestinationView:list_json')

        core.register_blueprint(voicemail)
