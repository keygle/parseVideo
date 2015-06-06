# -*- coding: utf-8 -*-
# error.py, part for parse_video : a fork from parseVideo. 
# error: o/lieying_plugin/error: errors definition for lieying_plugin. 
# version 0.0.3.0 test201506070244
# author sceext <sceext@foxmail.com> 2009EisF2015, 2015.06. 
# copyright 2015 sceext
#
# This is FREE SOFTWARE, released under GNU GPLv3+ 
# please see README.md and LICENSE for more information. 
#
#    parse_video : a fork from parseVideo. 
#    Copyright (C) 2015 sceext <sceext@foxmail.com> 
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

# import

# class for errors

# parse_video lieying_plugin base error
class ParseVideoLieyingPluginError(Exception):
    pass

class BError(ParseVideoLieyingPluginError):	# base error
    pass

class NotSupportURLError(BError):
    pass

class ParseError(BError):
    pass

class UnknowError(BError):
    pass

class MsgError(BError):
    pass

class DecodeUtf8Error(BError):
    pass

class HdError(BError):
    pass

# end error.py


