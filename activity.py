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

import gtk
import pango

from ctypes import cdll
from gettext import gettext as _

from sugar.activity import activity

logger = logging.getLogger('Tuxmath')

DEBUG_TERMINAL = False

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
     
        # Set the activity toolbox
        toolbox = activity.ActivityToolbox(self)
        self.set_toolbox(toolbox)

        self.ceibaljam_icon_path = os.getenv("SUGAR_BUNDLE_PATH") + "/images/ceibaljam.png"

        box_canvas = gtk.VBox(False, 0)
        self.set_canvas(box_canvas)

        # Title
        box_title = gtk.VBox(False, 0)
        label_title = gtk.Label(_("Tuxmath"))
        label_title.set_justify(gtk.JUSTIFY_CENTER)
        label_title.modify_font(pango.FontDescription("Arial 22"))

        box_title.add(gtk.Label("\n\n\n"))
        box_title.add(label_title)
        box_title.add(gtk.Label("\n"))

        # Author
        box_author = gtk.VBox(False, 0)
        box_author.add(gtk.Label(""))
        box_author.add(gtk.Label(_("Created by Tux4kids")))
        label_author_url = gtk.Label('<b>http://tux4kids.alioth.debian.org</b>')
        label_author_url.set_use_markup(True)
        box_author.add(label_author_url)

        # Options box
        box_options = gtk.VBox(False, 0)
        label_options = gtk.Label(_("Options:"))
        label_options.set_justify(gtk.JUSTIFY_LEFT)
        self.checkbtn_sound = gtk.CheckButton(label=_("No sound"))
        self.checkbtn_sound.set_active(True)
        self.checkbtn_negatives = gtk.CheckButton(label=_("Include negative numbers"))
        self.checkbtn_negatives.set_active(False)

        # Pack the checkboxes in HBoxes to center them
        hbox1 = gtk.HBox(False, 0)
        hbox1.add(gtk.Label(""))
        hbox1.add(gtk.Label(""))
        hbox1.add(gtk.Label(""))
        hbox1.add(gtk.Label(""))
        hbox1.add(gtk.Label(""))
        hbox1.add(gtk.Label(""))
        hbox1.add(gtk.Label(""))
        hbox1.add(self.checkbtn_sound)
        hbox1.add(gtk.Label(""))
        hbox1.add(gtk.Label(""))
        hbox1.add(gtk.Label(""))
        hbox1.add(gtk.Label(""))
        hbox1.add(gtk.Label(""))
        hbox1.add(gtk.Label(""))
        box_options.add(hbox1)

        # Credits
        box_credits = gtk.VBox(False, 0)
        box_credits.add(gtk.Label(""))
        box_credits.add(gtk.Label(_('Spanish translation and pedagogical evaluation by %(TEACHER)s') % { 'TEACHER': 'Ana Cichero' }))
        label_teacher_email= gtk.Label('<b>ana.cichero@gmail.com</b>')
        label_teacher_email.set_use_markup(True)
        box_credits.add(label_teacher_email)
        box_credits.add(gtk.Label(_('Sugarized by %(SUGARIZER)s') % { 'SUGARIZER': 'Marcos Orfila' }))
        label_sugarizer_website = gtk.Label('<b>http://www.marcosorfila.com</b>')
        label_sugarizer_website.set_use_markup(True)
        box_credits.add(label_sugarizer_website)
        box_credits.add(gtk.Label(""))

        # Footer box (Activities on CeibalJAM! website)
        box_footer = gtk.VBox(False, 0)
        box_footer.add(gtk.Label(""))
        box_footer.add(gtk.Label(_('Find more activities on %(CEIBALJAM)s website:') % { 'CEIBALJAM': 'CeibalJAM!'}))
        label_ceibaljam_website = gtk.Label('<b>http://activities.ceibaljam.org</b>')
        label_ceibaljam_website.set_use_markup(True)
        box_footer.add(label_ceibaljam_website)
        box_footer.add(gtk.Label(""))

        # CeibalJAM! image
        box_ceibaljam_image = gtk.VBox(False, 0)
        image_ceibaljam = gtk.Image()
        image_ceibaljam.set_from_file(self.ceibaljam_icon_path)
        box_ceibaljam_image.pack_end(image_ceibaljam, False, False, 0)

        # Buttons box
        box_buttons = gtk.HBox(False, 0)
        self.button_play = gtk.Button(_("Play"))
        self.button_play.connect("clicked", self._button_play_clicked_cb)
        self.button_exit = gtk.Button(_("Exit"))
        self.button_exit.connect("clicked", self._button_exit_clicked_cb)
        box_buttons.add(gtk.VBox())
        box_buttons.add(self.button_play)
        box_buttons.add(gtk.VBox())
        box_buttons.add(self.button_exit)
        box_buttons.add(gtk.VBox())

    	# Get all the boxes together
        box_canvas.pack_start(box_title, False, False, 0)
        box_canvas.pack_start(box_options, False, False, 0)
        box_canvas.pack_end(gtk.Label("\n\n"), False, False, 0)
        box_canvas.pack_end(box_buttons, False, False, 0)
        box_canvas.pack_end(gtk.Label("\n"), False, False, 0)
        box_canvas.pack_end(box_footer, False, False, 0)
        box_canvas.pack_end(box_ceibaljam_image, False, False, 0)
        box_canvas.pack_end(box_credits, False, False, 0)
        box_canvas.pack_end(box_author, False, False, 0)

        self.button_play.grab_focus()
        self.show_all()

    def run_game(self):
        bundle_path = activity.get_bundle_path()

        self.load_libs = ARCH != "arm"
        if self.load_libs:
            libs_path = os.path.join(bundle_path, "lib/", ARCH)
            vte = cdll.LoadLibrary(os.path.join(libs_path, "libvte.so.9"))
            sys.path.append(libs_path)

        import vte

        super(SuperTuxActivity, self).__init__(handle, create_jobject=False)

        self.__source_object_id = None

        # creates vte widget
        self._vte = vte.Terminal()

        if DEBUG_TERMINAL:
            toolbox = activity.ActivityToolbox(self)
            toolbar = toolbox.get_activity_toolbar()
            self.set_toolbox(toolbox)

            self._vte.set_size(30,5)
            self._vte.set_size_request(200, 300)
            font = 'Monospace 10'
            self._vte.set_font(pango.FontDescription(font))
            self._vte.set_colors(gtk.gdk.color_parse('#E7E7E7'),
                                 gtk.gdk.color_parse('#000000'),
                                 [])

            vtebox = gtk.HBox()
            vtebox.pack_start(self._vte)
            vtesb = gtk.VScrollbar(self._vte.get_adjustment())
            vtesb.show()
            vtebox.pack_start(vtesb, False, False, 0)
            self.set_canvas(vtebox)

            toolbox.show()
            self.show_all()
            toolbar.share.hide()
            toolbar.keep.hide()

        # now start subprocess.
        self._vte.connect('child-exited', self.exit_with_sys)
        self._vte.grab_focus()

        argv = [
            "/bin/sh",
            "-c",
            os.path.join(bundle_path, "bin/tuxmath"),
            "--homedir %s" % tux_homedir,
            "--fullscreen"
        ]

        self._pid = self._vte.fork_command \
            (command='/bin/sh',
             argv=argv,
             envv=envv,
             directory=bundle_path)

    def exit_with_sys(self, widget=None):
        "This method is invoked when the user's script exits."
        if not DEBUG_TERMINAL:
            sys.exit()

    def _button_play_clicked_cb(self, widget):
       self.run_game()

    def _button_exit_clicked_cb(self, widget):
       self.exit_with_sys()

