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
import gobject
import socket

#autoEM package
from autoEM.base import autoEMBase
from autoEM.misc import *

(
COLUMN_FIXED,
COLUMN_SIMULATION,
COLUMN_STATUS,
) = range(3)
(
COLUMN_HOST,
COLUMN_USAGE,
) = range(2)

class autoEMGui(autoEMBase):
	"""docstring for ClassName"""
	def __init__(self):
		##########Window##########
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_size_request(500,500)
		self.window.set_resizable(False)
		self.window.set_title(program_name)
		self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
		self.window.set_border_width(10)
		
		##########Widget##########
		#top label
		self.label = gtk.Label('Choose the simulation you want to run.')
		#button
		self.upload = gtk.Button('upload')
		self.execute = gtk.Button('run')
		self.download = gtk.Button('download')
		self.add = gtk.Button('add')
		self.remove = gtk.Button('remove')
		self.about = gtk.Button('About')
		#file scroll window
		self.sw_file = gtk.ScrolledWindow()
		self.sw_file.set_size_request(200, 400)
		self.sw_file.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		self.sw_file.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		#file listview
		self.file_listbox = gtk.ListStore(
			gobject.TYPE_BOOLEAN,
			gobject.TYPE_STRING,
			gobject.TYPE_STRING)
		#file treeview
		self.treeview_file = gtk.TreeView(self.file_listbox)
		self.treeview_file.set_rules_hint(True)
		self.add_column_file(self.treeview_file)

		#host scroll window
		self.sw_host = gtk.ScrolledWindow()
		self.sw_host.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		self.sw_host.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		#host listview
		self.host_listbox = gtk.ListStore(
			gobject.TYPE_STRING,
			gobject.TYPE_STRING)
			
		#host treeview
		self.treeview_host = gtk.TreeView(self.host_listbox)
		self.treeview_host.set_rules_hint(True)
		self.host_selection = self.treeview_host.get_selection()
		self.host_selection.set_mode(gtk.SELECTION_SINGLE)
		self.add_column_host(self.treeview_host)

		##########Layout##########
		Mainbox = gtk.VBox()
		file_bottombox = gtk.HBox()
		host_bottombox = gtk.HBox()
		table = gtk.Table(rows = 2, columns = 2, homogeneous=False)

		##pack two scroll window		
		self.sw_file.add(self.treeview_file)
		self.sw_host.add(self.treeview_host)

		#file_bottombox
		file_bottombox.pack_start(self.upload, False, False, 5)
		file_bottombox.pack_start(self.execute, False, False, 5)
		file_bottombox.pack_start(self.download, False, False, 5)
		#host_bottombox
		host_bottombox.pack_start(self.add, False, False, 5)
		host_bottombox.pack_start(self.remove, False, False, 5)
		host_bottombox.pack_end(self.about, False, False, 5)
		#table pack
		table.attach(self.sw_file, 0, 1, 0, 1, yoptions=gtk.EXPAND|gtk.FILL)
		table.attach(self.sw_host, 1, 2, 0, 1, yoptions=gtk.EXPAND|gtk.FILL)
		table.attach(file_bottombox, 0, 1, 1, 2)
		table.attach(host_bottombox, 1, 2, 1, 2)

		Mainbox.pack_start(self.label, False, False, 5)
		Mainbox.pack_start(table, False, False, 5)

		self.window.add(Mainbox)

		#Connect
		#gobject.timeout_add(5000, self.update_usage)
		self.gui_update_workstation()
		self.gui_update_file()
		self.update_usage()
		self.add.connect('clicked', self.gui_add_workstation)
		self.remove.connect('clicked', self.gui_remove_workstation)
		self.about.connect('clicked', self.about_dialog)
		self.window.connect("destroy", gtk.main_quit)

		#Main
		self.window.show_all()
		self.gui_ask_info()
		gtk.main()

	def gui_update_file(self):
		self.file_listbox.clear()
		for item in self.list_file():
			iter = self.file_listbox.append()
			self.file_listbox.set(iter,
				COLUMN_FIXED, False,
				COLUMN_SIMULATION, item,
				COLUMN_STATUS, '')

	def gui_update_workstation(self):
		self.host_listbox.clear()
		for item in self.list_host():
			iter = self.host_listbox.append()
			self.host_listbox.set(iter,
				COLUMN_HOST, item,
				COLUMN_USAGE, '')
	
	def gui_ask_info(self):
		askinfo = gtk.MessageDialog(None, 0, gtk.MESSAGE_QUESTION, gtk.BUTTONS_OK_CANCEL, "Input your username and password")
		action_area = askinfo.get_content_area()
		nameentry = gtk.Entry()
		passentry = gtk.Entry()
		passentry.set_visibility(False)
		action_area.pack_start(nameentry)
		action_area.pack_start(passentry)
		askinfo.show_all()
		response = askinfo.run()
		if response == gtk.RESPONSE_OK:
			self.set_info(nameentry.get_text(), passentry.get_text())
		elif response == gtk.RESPONSE_CANCEL:
			pass

		askinfo.destroy()

	def gui_remove_workstation(self, button):
		"""show warning, call remove_workstation, update liststore"""
		model, iter = self.host_selection.get_selected()
		if iter is not None:
			deletehost = gtk.MessageDialog(None, 0, gtk.MESSAGE_QUESTION, gtk.BUTTONS_OK_CANCEL, "Are you sure you want to delete this host")
			deletehost.show_all()
			response = deletehost.run()
			if response == gtk.RESPONSE_OK:
				self.remove_workstation(model.get_value(iter,0))
				self.gui_update_workstation()
			deletehost.destroy()

	def gui_add_workstation(self, button):
		"""show pop out, get host and call add_workstaion, update liststore"""
		askhost = gtk.MessageDialog(None, 0, gtk.MESSAGE_QUESTION, gtk.BUTTONS_OK_CANCEL, "Input the host IP")
		action_area = askhost.get_content_area()
		entry = gtk.Entry()
		action_area.pack_start(entry)
		askhost.show_all()
		response = askhost.run()
		if response == gtk.RESPONSE_OK:
			#press ok, test host ip validation
			text = entry.get_text()
			try:
				socket.inet_aton(text)
				self.add_workstaion(text)
				self.gui_update_workstation()
			except socket.error:
				warning = gtk.MessageDialog(None, 0, gtk.MESSAGE_WARNING, gtk.BUTTONS_OK, "invalid IP")
				warning.show_all()
				warning.run()
				warning.destroy()
		askhost.destroy()

	def about_dialog(self, button):
		"""about this program"""
		about = gtk.AboutDialog()
		about.set_position(gtk.WIN_POS_CENTER)
		about.set_name(program_name)
		about.set_version(program_version)
		about.set_comments('Manage EM works Easily\n')
		about.set_license('''
			This program is free software; you can redistribute it and/or modify
			it under the terms of the GNU General Public License as published by
			the Free Software Foundation; either version 2 of the License, or
			(at your option) any later version.
			
			This program is distributed in the hope that it will be useful,
			but WITHOUT ANY WARRANTY; without even the implied warranty of
			MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
			GNU General Public License for more details.
			
			You should have received a copy of the GNU General Public License
			along with this program; if not, write to the Free Software Foundation,
			Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
			''')
		about.set_copyright('Copyright 2012 Lee You-Tang (YodaLee)')
		about.set_website('https://github.com/lc85301/autoEM')
		about.set_website_label('autoEM at GitHub')
		about.set_authors(['Lee You-Tang (YodaLee) <lc85301@gmail.com>'])
		about.set_translator_credits('Lee You-Tang (YodaLee)' '<lc85301@gmail.com>')
		about.set_logo(gtk.gdk.pixbuf_new_from_file_at_size(program_logo, 96,96))
		about.connect('response', lambda x, y, z: about.destroy(), True)
		about.show_all()

	def add_column_file(self, treeview):
		"""add default column in treeview"""
		model = treeview.get_model()
		# column for fixed toggles
		renderer = gtk.CellRendererToggle()
		renderer.connect('toggled', self.fixed_toggled, model)
		column = gtk.TreeViewColumn('Fixed', renderer, active=COLUMN_FIXED)
		# set this column to a fixed sizing(of 50 pixels)
		column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
		column.set_fixed_width(50)
		treeview.append_column(column)
		# column for simulation name
		column = gtk.TreeViewColumn('Simulation', gtk.CellRendererText(), text=COLUMN_SIMULATION)
		treeview.append_column(column)
		# column for simulation status
		column = gtk.TreeViewColumn('Status', gtk.CellRendererText(), text=COLUMN_STATUS)
		treeview.append_column(column)

	def add_column_host(self, treeview):
		"""add default column in treeview"""
		model = treeview.get_model()
		# column for simulation name
		column = gtk.TreeViewColumn('Workstation Host', gtk.CellRendererText(), text=COLUMN_HOST)
		treeview.append_column(column)
		# column for simulation status
		column = gtk.TreeViewColumn('Usage', gtk.CellRendererText(), text=COLUMN_USAGE)
		treeview.append_column(column)

	def fixed_toggled(self, cell, path, model):
		# get toggled iter
		iter = model.get_iter((int(path),))
		fixed = model.get_value(iter, COLUMN_FIXED)
		# do something with the value
		fixed = not fixed
		# set new value
		model.set(iter, COLUMN_FIXED, fixed)

	def update_usage(self):
		host_list = self.list_host()
		status = self.get_usage()
		for item in range(len(host_list)):
			self.host_listbox[item][COLUMN_USAGE] = 'XD'

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
