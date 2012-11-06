##################################################################################
#-*- coding: utf-8 -*-
# 
# Filename: misc.py
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

import sys
import platform
import collections

#os Information
running_os = platform.system()

#Program Information
program_name = 'autoEM'
program_version = '0.1.0'

if running_os == "Windows":
	program_logo = 'autoEM.png'

#configure file storage
config_file = "example.xml"

#Info type
Info = collections.namedtuple("Info", "username, hostname, password, port")

