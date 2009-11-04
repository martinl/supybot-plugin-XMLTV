###
# Copyright (c) 2009, Martin Lillepuu
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
import xmltv
import datetime
from dateutil.parser import *

xmltv.locale = 'UTF-8'
path = '/home/yamamoto/xmltv/'
filenames = []
filenames.append(path + '11_channeldata.xml')
filenames.append(path + '12_channeldata.xml')
filenames.append(path + '13_channeldata.xml')
filenames.append(path + '6_channeldata.xml')
filenames.append(path + '9_channeldata.xml')
filenames.append(path + '10_channeldata.xml')
filenames.append(path + '15_channeldata.xml')
filenames.append(path + '16_channeldata.xml')

class XMLTV(callbacks.Plugin):
    """XMLTV plugin is used for displaying current
    TV shows. Usage: !tv"""

    def tv(self, irc, msg, args):
        """takes no arguments

        Returns the list of current TV shows.
        """
        global filenames
        now = datetime.datetime.today()
        show_list  = ""
        show_count = 0

        for filename in filenames:
            print filename
            try:
                chans = xmltv.read_channels(open(filename, 'r'))
                for chan in chans:
                    try:
                        chan_name = chan['display-name'][0][0]
                        print chan_name
                        shows = xmltv.read_programmes(open(filename, 'r'))
                        for show in shows:
                           try:
                               start_time = parse(show['start'],ignoretz=True)
                               stop_time = parse(show['stop'],ignoretz=True)
                               if (start_time <= now and stop_time >= now):
				   show_count = show_count + 1
                                   show_list = show_list + "\x0F" + "\x02" + chan_name + "\x0F" + " " + str(start_time.strftime("%H:%M")) + " " + (show['title'][0][0]).encode("UTF-8") + " "
#                                   if not (show_count % 3):
#                                      irc.reply(show_list)
#                                      show_list = ""
                           except:
                               pass
                    except:
                        pass
            except:
                pass
        irc.reply(show_list)
        print show_list
    tv = wrap(tv)

    def chan(self, irc, msg, args):
        """takes no arguments

        Returns the list of TV channels from XMLTV feed.
        """
        global filenames
        chan_list = ''
        for filename in filenames:
            try:
                chans = xmltv.read_channels(open(filename, 'r'))
                for chan in chans:
                    try:
                        chan_list = chan_list + chan['display-name'][0][0] + ' '
                    except:
                        pass
            except:
                pass
        irc.reply(chan_list)
    channels = wrap(chan)


Class = XMLTV


# vim:set shiftwidth=4 tabstop=4 expandtab
