#!/usr/bin/python2.7

##################################################################################
#-*- coding: utf-8 -*-
# 
# Filename: autoEM.py
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

#builtin library
import sys
import os.path
from optparse import OptionParser, make_option
#self define library

program = sys.argv[0]
LAUNCH_DIR = os.path.dirname(os.path.abspath(sys.path[0]))
# If launched from source directory
if program.startswith('./') or program.startswith('bin/'):
    sys.path.insert(0, LAUNCH_DIR)

from autoEM.misc import *

def version():
	sys.stderr.write(
'%s Ver %s\n\
Copyright (C) 2012 YodaLee\n\
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.\n\
This is free software: you are free to change and redistribute it.\n\
There is NO WARRANTY, to the extent permitted by law.\n\
Written by YodaLee <lc85301@gmail.com>.\n' % (program_name, program_version)
)

def main():
	#"""the main function of autoEM"""
	option_list = [
		make_option('-v', '--version', action='store_true', dest='version',
					default=False, help='show version information')
		]
	parser = OptionParser(usage = 'Usage: autoEM [OPTION...] PAGE...',
						option_list=option_list)
	options, args = parser.parse_args()

	if options.version:
		version()
		sys.exit(0)

	from autoEM.gui import autoEMGui
	autoEMGui()
	sys.exit()
	
if __name__ == '__main__':
	try:
		main()
	except (Exception, KeyboardInterrupt), e:
		if type(e) == KeyboardInterrupt:
			print '\nAborted.'
		else:
			print 'error:', e
