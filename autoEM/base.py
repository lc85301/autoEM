#!/usr/bin/python2.7

##################################################################################
#-*- coding: utf-8 -*-
# 
# Filename: base.py
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

#predefine library
import os
import getpass
import traceback
import collections
import xml.etree.ElementTree as ET
#third part library
import paramiko
#self define library
from autoEM.misc import *

class autoEMBase:
	"""docstring for autoEMBase"""
	def __init__():
		pass

	##################Record related function##################
	Tree = ET.parse('example.xml')
	Info = Tree.getroot()
	def refreshRecord(self):
		Tree.write('example.xml')

	def add_workstaion(self, host):
		"""add a workstation record to xml"""
		ET.subelement

	
	def list_host(self):
		"""return the list with all host in record"""
		hostlist = []
		for host in self.Info.find('Servers').findall('Host'):
			hostlist.append(host.text)
		return hostlist

	def list_file(self):
		"""check the file in local directory and list all the .son files"""
		path = os.getcwd()
		listing = os.listdir(path)
		filelist = []
		for infile in listing:
			if infile.endswith(".son"):
				filelist.append(infile)
		return filelist

	##################Paramiko(SSH) related function##################
	def exec_remote_command(command, info):
		"""execute the command on the remote maching,
		return the stdout and stderr"""
		#setup log file
		#info = get_user_info()
		try:
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(info.hostname, username=info.username, password = info.password)
			stdin, stdout, stderr = ssh.exec_command(command)
			return stdout, stderr
		except exception, e:
			print '*** Caught exception %s: %s ***' % (e.__class__, e)
			traceback.print_exc()
		finally:
			ssh.close()
			sys.exit(1)

	def download_file(filename, info):
		"""download file to workstation"""
		#info = get_user_info()
		t = paramiko.Transport((info.hostname,info.port))
		t.connect(username=info.username, password=info.password, hostkey=info.hostkey)
		sftp = paramiko.SFTPClient.from_transport(t)
		sftp.get("autoEM/"+filename, filename)
		sftp.close()
		t.close()

	def upload_file(filename, info):
		"""upload file to workstation"""
		#info = get_user_info()
		t = paramiko.Transport((info.hostname,info.port))
		t.connect(username=info.username, password=info.password, hostkey=info.hostkey)
		sftp = paramiko.SFTPClient.from_transport(t)
		sftp.put(filename, "autoEM/" + filename)
		sftp.close()
		t.close()

	def check_usage(self, hostlist):
		for host in list_host():
			print host

	def get_usage():
		"""check the status of workstation loading"""
		command = 'uptime'
		stdout, stderr = exec_remote_command(command)
		print(stdout.readline())

		command = 'free'
		stdout, stderr = exec_remote_command(command)
		print(stdout.readline())

	def run(filename):
		"""run em simulation"""
		command = 'source ~/.bashrc; nohup em ~/autoEM/%s </dev/null >em.log 2>&1 &' % filename
		stdout, stderr = exec_remote_command(command)
		stdout.readline()
		stderr.readline()



#sftp = paramiko.SFTPClient.from_transport(t)
#try:
#	sftp.mkdir("autoEM")
#except IOError:
#	print '(autoEM folder already exists)'
#sftp.put(filename, filename)

		#def get_user_info():
		#"""get username and password"""
		## get hostname
		#hostname = ''
		#username = ''
		#password = ''
		#port = 22
		#hostname = raw_input('Hostname: ')
		#if len(hostname) == 0:
		#	print '*** Hostname required. ***'
		#	sys.exit(1)
		#if hostname.find('@') >= 0 :
		#	username, hostname = hostname.split('@')
		#if hostname.find(':') >= 0:
		#	hostname, portstr = hostname.split(':')
		#	port = int(portstr)
		### get username
		#if username == '':
		#	default_username = getpass.getuser()
		#	username = raw_input('Username [%s]: ' % default_username)
		#	if len(username) == 0:
		#		username = default_username
		#password = getpass.getpass('Password for %s@%s: ' % (username, hostname))

		## get host key, if we know one
		#hostkeytype = None
		#hostkey = None
		#try:
		#	host_keys = paramiko.util.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
		#except IOError:
		#	try:
		#		# try ~/ssh/ too, because windows can't have a folder named ~/.ssh/
		#		host_keys = paramiko.util.load_host_keys(os.path.expanduser('~/ssh/known_hosts'))
		#	except IOError:
		#		print '*** Unable to open host keys file ***'
		#		host_keys = {}
		#if host_keys.has_key(hostname):
		#	hostkeytype = host_keys[hostname].keys()[0]
		#	hostkey = host_keys[hostname][hostkeytype]
		#	print 'Using host key of type %s' % hostkeytype

#	Info = collections.namedtuple("Info", "username, hostname, password, port, hostkeytype, hostkey")
#	return Info(username, hostname, password, port, hostkeytype, hostkey)
