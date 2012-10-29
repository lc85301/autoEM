
##################################################################################
#-*- coding: utf-8 -*-
# 
# Filename: gui.py
#
# Copyright (C) 2012 -  You-Tang Lee (YodaLee) <lc85301@gmail.com>
# All Rights reserved.
#
# This file is part of project: autoEM.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
##################################################################################

##############################################
# File: gui.py 
# Description: The GUI interface of autoEM written by pyGTK
##############################################

import pygtk
pygtk.require('2.0')
import gtk

#autoEM package
from autoEM.base import autoEMBase
from autoEM.misc import *

class autoEMGui(autoEMBase):
	"""docstring for ClassName"""
	def update_local(self):
		"""update the  local window"""
	def update_remote(self):
		"""update the check button in remote window"""

	def __init__(self):
		#Info = self.parseRecord()
		for child in super().Info:
			print(child.tag)

		#create window
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_size_request(400,300)
		self.window.set_title(program_name)
		self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
		self.window.set_border_width(10)
		
		##########Widget##########
		#button
		self.upload = gtk.Button('upload')
		self.execute = gtk.Button('run')
		self.download = gtk.Button('download')

		# create tree view
		#model = self.list_model()
		#treeview = gtk.TreeView(model)
		#treeview.set_rules_hint(True)
		#treeview.set_search_column(COLUMN_DESCRIPTION)

		##########Layout##########
		Mainbox = gtk.VBox()
		upbox = gtk.HBox()
		bottombox = gtk.HBox()
		rightbox = gtk.VBox()
		leftbox = gtk.VBox()

		listbox = gtk.ScrolledWindow()
		listbox.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		listbox.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
		#listbox.add(self.treeview)

		bottombox.pack_start(self.upload, False, False, 5)
		bottombox.pack_start(self.execute, False, False, 5)
		bottombox.pack_start(self.download, False, False, 5)

		upbox.pack_start(leftbox, False, False, 5)
		upbox.pack_start(rightbox, False, False, 5)

		Mainbox.pack_start(upbox, False, False, 5)
		Mainbox.pack_start(bottombox, False, False, 5)

		self.window.add(Mainbox)

		#Connect

		#Main
		self.window.show_all()
		gtk.main()

def main():
	"""docstring for main"""
	gtk.main()
		
if __name__ == '__main__':
	try:
		autoEMGui()
		main()
	except (Exception, KeyboardInterrupt), e:
		if type(e) == KeyboardInterrupt:
			print '\nAborted.'
		else:
			print 'error:', e
