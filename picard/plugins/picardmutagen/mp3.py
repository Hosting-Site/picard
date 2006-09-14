# -*- coding: utf-8 -*-
#
# Picard, the next-generation MusicBrainz tagger
# Copyright (C) 2006 Lukáš Lalinský
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

"""Mutagen-based MP3 metadata reader."""

from picard.file import File
from picard.util import encode_filename
from mutagen.mp3 import MP3
from mutagen import id3
from picard.plugins.picardmutagen.mutagenext.compatid3 import CompatID3, TCMP
from picard.plugins.picardmutagen._id3 import read_id3_tags, write_id3_tags

class MutagenMP3File(File):

    def read(self):
        
        mp3file = MP3(encode_filename(self.filename), ID3=CompatID3)
        read_id3_tags(mp3file.tags, self.orig_metadata)

        self.orig_metadata["~filename"] = self.base_filename
        self.orig_metadata["~#length"] = int(mp3file.info.length * 1000)
        self.orig_metadata["~#bitrate"] = int(mp3file.info.bitrate / 1000)

        self.metadata.copy(self.orig_metadata)

    def save(self):
        """Save ID3 tags to the file."""
        
        id3file = CompatID3(encode_filename(self.filename), translate=False)
        write_id3_tags(id3file, self.metadata)
        id3file.update_to_v23()
        id3file.save(v2=3)
