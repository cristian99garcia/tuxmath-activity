# -*- coding: UTF-8 -*-
# Copyright 2007-2008 One Laptop Per Child
# Copyright 2007 Gerard J. Cerchio <www.circlesoft.com>
# Copyright 2008 Andrés Ambrois <andresambrois@gmail.com>
# Copyright 2010 Marcos Orfila <www.marcosorfila.com>
# Copyright 2016 Cristian García <cristian99garcia@gmail.com>
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
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import os
import sys
import logging
import platform
import commands

from gettext import gettext as _

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Vte
from gi.repository import GLib
from gi.repository import Pango

from sugar3.activity import activity
from sugar3.graphics.toolbarbox import ToolbarBox

logger = logging.getLogger('Tuxmath')

ARCH = "x86"
if platform.machine().startswith('arm'):
    ARCH = "arm"
else:
    if platform.architecture()[0] == '64bit':
        ARCH = "x86-64"
    else:
        ARCH = "x86"


class TuxmathStart(activity.Activity):

    def __init__(self, handle):
        # Initialize the parent
        activity.Activity.__init__(self, handle)
        logger.debug('Initiating Tuxmath')
     
        # Set the activity toolbarbox
        toolbarbox = ToolbarBox()
        self.set_toolbar_box(toolbarbox)
        toolbarbox.show()

        self.ceibaljam_icon_path = os.getenv("SUGAR_BUNDLE_PATH") + "/images/ceibaljam.png"

        box_canvas = Gtk.VBox(False, 0)
        self.set_canvas(box_canvas)

        # Title
        box_title = Gtk.VBox(False, 0)
        label_title = Gtk.Label(_("Tuxmath"))
        label_title.set_justify(Gtk.Justification.CENTER)
        label_title.modify_font(Pango.FontDescription("Arial 22"))

        box_title.add(Gtk.Label("\n\n\n"))
        box_title.add(label_title)
        box_title.add(Gtk.Label("\n"))

        # Author
        box_author = Gtk.VBox(False, 0)
        box_author.add(Gtk.Label(""))
        box_author.add(Gtk.Label(_("Created by Tux4kids")))
        label_author_url = Gtk.Label('<b>http://tux4kids.alioth.debian.org</b>')
        label_author_url.set_use_markup(True)
        box_author.add(label_author_url)

        # Options box
        box_options = Gtk.VBox(False, 0)
        label_options = Gtk.Label(_("Options:"))
        label_options.set_justify(Gtk.Justification.LEFT)
        self.checkbtn_sound = Gtk.CheckButton(label=_("No sound"))
        self.checkbtn_sound.set_active(True)
        self.checkbtn_negatives = Gtk.CheckButton(_("Include negative numbers"))
        self.checkbtn_negatives.set_active(False)

        # Pack the checkboxes in HBoxes to center them
        hbox1 = Gtk.HBox(False, 0)
        hbox1.add(Gtk.Label(""))
        hbox1.add(Gtk.Label(""))
        hbox1.add(Gtk.Label(""))
        hbox1.add(Gtk.Label(""))
        hbox1.add(Gtk.Label(""))
        hbox1.add(Gtk.Label(""))
        hbox1.add(Gtk.Label(""))
        hbox1.add(self.checkbtn_sound)
        hbox1.add(Gtk.Label(""))
        hbox1.add(Gtk.Label(""))
        hbox1.add(Gtk.Label(""))
        hbox1.add(Gtk.Label(""))
        hbox1.add(Gtk.Label(""))
        hbox1.add(Gtk.Label(""))
        box_options.add(hbox1)

        # Credits
        box_credits = Gtk.VBox(False, 0)
        box_credits.add(Gtk.Label(""))
        box_credits.add(Gtk.Label(_('Spanish translation and pedagogical evaluation by %(TEACHER)s') % { 'TEACHER': 'Ana Cichero' }))
        label_teacher_email= Gtk.Label('<b>ana.cichero@gmail.com</b>')
        label_teacher_email.set_use_markup(True)
        box_credits.add(label_teacher_email)
        box_credits.add(Gtk.Label(_('Sugarized by %(SUGARIZER)s') % { 'SUGARIZER': 'Marcos Orfila' }))
        label_sugarizer_website = Gtk.Label('<b>http://www.marcosorfila.com</b>')
        label_sugarizer_website.set_use_markup(True)
        box_credits.add(label_sugarizer_website)
        box_credits.add(Gtk.Label(""))

        # Footer box (Activities on CeibalJAM! website)
        box_footer = Gtk.VBox(False, 0)
        box_footer.add(Gtk.Label(""))
        box_footer.add(Gtk.Label(_('Find more activities on %(CEIBALJAM)s website:') % { 'CEIBALJAM': 'CeibalJAM!'}))
        label_ceibaljam_website = Gtk.Label('<b>http://activities.ceibaljam.org</b>')
        label_ceibaljam_website.set_use_markup(True)
        box_footer.add(label_ceibaljam_website)
        box_footer.add(Gtk.Label(""))

        # CeibalJAM! image
        box_ceibaljam_image = Gtk.VBox(False, 0)
        image_ceibaljam = Gtk.Image()
        image_ceibaljam.set_from_file(self.ceibaljam_icon_path)
        box_ceibaljam_image.pack_end(image_ceibaljam, False, False, 0)

        # Buttons box
        box_buttons = Gtk.HBox(False, 0)
        self.button_play = Gtk.Button(_("Play"))
        self.button_play.connect("clicked", self._button_play_clicked_cb)
        self.button_exit = Gtk.Button(_("Exit"))
        self.button_exit.connect("clicked", self._button_exit_clicked_cb)
        box_buttons.add(Gtk.VBox())
        box_buttons.add(self.button_play)
        box_buttons.add(Gtk.VBox())
        box_buttons.add(self.button_exit)
        box_buttons.add(Gtk.VBox())

    	# Get all the boxes together
        box_canvas.pack_start(box_title, False, False, 0)
        box_canvas.pack_start(box_options, False, False, 0)
        box_canvas.pack_end(Gtk.Label("\n\n"), False, False, 0)
        box_canvas.pack_end(box_buttons, False, False, 0)
        box_canvas.pack_end(Gtk.Label("\n"), False, False, 0)
        box_canvas.pack_end(box_footer, False, False, 0)
        box_canvas.pack_end(box_ceibaljam_image, False, False, 0)
        box_canvas.pack_end(box_credits, False, False, 0)
        box_canvas.pack_end(box_author, False, False, 0)

        self.button_play.grab_focus()
        self.show_all()

    def run_game(self):
        self.__source_object_id = None
        bundle_path = activity.get_bundle_path()

        # creates vte widget
        self._vte = Vte.Terminal()
        self._vte.connect('child-exited', self.exit_with_sys)

        argv = [
            "/bin/sh",
            "-c",
            os.path.join(bundle_path, "bin/tuxmath"),
            "--homedir %s" % os.path.join(bundle_path, "tux_homedir("),
            "--fullscreen"
        ]

        if hasattr(self._vte, 'fork_command_full'):
            self._vte.fork_command_full(
                Vte.PtyFlags.DEFAULT,
                os.environ['HOME'],
                argv,
                [],
                GLib.SpawnFlags.DO_NOT_REAP_CHILD,
                None,
                None)
        else:
            self._vte.spawn_sync(
                Vte.PtyFlags.DEFAULT,
                os.environ['HOME'],
                argv,
                [],
                GLib.SpawnFlags.DO_NOT_REAP_CHILD,
                None,
                None)

    def exit_with_sys(self, *args):
        sys.exit()

    def _button_play_clicked_cb(self, widget):
       self.run_game()

    def _button_exit_clicked_cb(self, widget):
       self.exit_with_sys()

