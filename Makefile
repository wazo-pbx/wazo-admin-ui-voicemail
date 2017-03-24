install:
	python setup.py install
	cp etc/wazo-admin-ui/conf.d/voicemail.yml /etc/wazo-admin-ui/conf.d
	systemctl restart wazo-admin-ui

uninstall:
	pip uninstall wazo-admin-ui-voicemail
	rm /etc/wazo-admin-ui/conf.d/voicemail.yml
	systemctl restart wazo-admin-ui
