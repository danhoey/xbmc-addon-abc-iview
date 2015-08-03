#
#  ABC iView XBMC Addon
#  Copyright (C) 2012 Andy Botting
#
#  This addon includes code from python-iview
#  Copyright (C) 2009-2012 by Jeremy Visser <jeremy@visser.name>
#
#  This addon is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This addon is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this addon. If not, see <http://www.gnu.org/licenses/>.
#

import os, sys
import classes, comm, config, utils, urlparse
import xbmc, xbmcgui, xbmcplugin, xbmcaddon

def play(url, subtitles_dir):
    time = 5000  #in miliseconds
    xbmc.executebuiltin('Notification(%s, %s, %d)'%("iView","Loading...", time))
    addon = xbmcaddon.Addon(config.ADDON_ID)

    try:
        p = classes.Program()
        p.parse_xbmc_url(url)

        listitem=xbmcgui.ListItem(label=p.get_list_title(), iconImage=p.thumbnail, thumbnailImage=p.thumbnail)
        listitem.setInfo('video', p.get_xbmc_list_item())

        if hasattr(listitem, 'addStreamInfo'):
            listitem.addStreamInfo('audio', p.get_xbmc_audio_stream_info())
            listitem.addStreamInfo('video', p.get_xbmc_video_stream_info())

        try:
            subtitles = get_setting_subtitles(addon)
            if subtitles:
                iview_config = comm.get_config()
                o = urlparse.urlparse(p.url)
                subtitles_file = comm.get_captions(iview_config, o.path[o.path.index(o.path.split("/")[3]):].split('.')[0], subtitles_dir)
                if subtitles_file:
                    listitem.setSubtitles([subtitles_file])
        except:
            # oops print error message
            time = 10000  #in miliseconds
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%("iView","Unable to load subtitles", time, p.thumbnail))
            utils.log_error();

        xbmc.Player().play(p.get_url(), listitem)
      
    except:
        utils.handle_error("Unable to play video")

def get_setting_subtitles(addon):
  #values="None|Download" default="None"
  subtitles = addon and addon.getSetting('subtitles_control')
  if subtitles:
    if subtitles == 'None' or subtitles == '0':
      return None
    elif subtitles == 'Download' or subtitles == '1':
      return 'download'
  # default
  return None