#!/usr/bin/python3

'''nut Apport interface

Copyright (C) 2010 Canonical Ltd.
Author: Chuck Short <chuck.short@canonical.com>

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 2 of the License, or (at your
option) any later version.  See http://www.gnu.org/copyleft/gpl.html for
the full text of the license.
'''
from apport.hookutils import *


def add_info(report,ui):

	response = ui.yesno("The contents of your nut configuration files may help developers diagnose your bug more quickly, however, it may contain sensitive information. Do you want to include it in your bug report?")

	if response == None: #use cancelled
		raise StropIteration

	elif response == True:
		attach_file(report, '/etc/nut/ups.conf', 'UpsConf')

	elif response == False:
		ui.information("The contents of your nut configuration files will NOT be included in the bug report")

	report['USBDevices'] = command_output(['lsusb'])
	packages = ['nut', 'nut-client','nut-server', 'nut-cgi', 'nut-snmp', 'nut-hal-drivers', 'nut-xml', 'libupsclient1',
		'libupsclient1-dev', 'python-nut', 'nut-monitor']
	versions = ''
	for package in packages:
		try:
			version = packaging.get_version(package)
		except ValueError:
			version = 'N/A'
		if version is None:
			version = 'N/A'
		versions += '%s %s\n' %(package, version)
	report['NutInstalledVersions'] = versions
	report['KernelVersion'] = command_output(['uname', '-a'])
