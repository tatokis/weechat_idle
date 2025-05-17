#!/usr/bin/env python3

import dbus
from gi.repository import GLib
from dbus.mainloop.glib import DBusGMainLoop
import subprocess
import argparse

parser = argparse.ArgumentParser(
                    prog="weechat_idle",
                    description="Switches to the 'weechat' buffer when the system idles."
                )

parser.add_argument("--host", required=False, help="SSH host running WeeChat (for remote control)")
defpipe = "~/.weechat/weechat_fifo"
parser.add_argument("--pipe", default=defpipe, required=False, help=f"location of WeeChat FIFO (defaults to {defpipe})")

args = parser.parse_args()
ssh_host = args.host
pipe = args.pipe

away_reason = "Computer is idle"

weechat_var = "plugins.var.idle_autoswitch.last_buffer"
to_weechat_cmd  = f"*/eval /mute /set {weechat_var} ${{buffer.full_name}}\\n*/buffer weechat\\n*/aaway {away_reason}"
to_previous_cmd = f"*/eval /buffer ${{{weechat_var}}}\\n*/aaway"

# Wrap them in echo and pipe them
# -e needed for newlines
to_weechat_cmd  = f"echo -e '{to_weechat_cmd }' > {pipe}"
to_previous_cmd = f"echo -e '{to_previous_cmd}' > {pipe}"

# Call ssh if desired
if ssh_host:
    to_weechat_cmd  = ["ssh", ssh_host, to_weechat_cmd ]
    to_previous_cmd = ["ssh", ssh_host, to_previous_cmd]

ml = DBusGMainLoop(set_as_default=True)

bus = dbus.SessionBus()

# For some reason ActiveChanged is not emitted over the freedesktop one. *sigh*
# If you're on KDE Plasma, uncomment the freedesktop one and comment the gnome one
#obj = bus.get_object("org.freedesktop.ScreenSaver", "/org/freedesktop/ScreenSaver")
obj = bus.get_object("org.gnome.ScreenSaver", "/org/gnome/ScreenSaver")

def active_changed(active):
    cmd = to_weechat_cmd if active else to_previous_cmd
    subprocess.run(cmd, shell=not ssh_host)

obj.connect_to_signal("ActiveChanged", active_changed)

GLib.MainLoop().run()
