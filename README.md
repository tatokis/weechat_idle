# weechat_idle

A small script to automatically switch to the `weechat` buffer when the system is idling, and back to the previous buffer when it's no longer idle.

NOTE: This is **NOT** a WeeChat plugin. It is meant to run externally.

You might need to modify the script to get it working on KDE Plasma. It's only been tested under Unity, but presumably it will work with anything GNOME-based.

# Why?

WeeChat likes to eat notifications and highlights for the current buffer, preventing relay applications (such as WeeChat Android) from notifying the user.

# Usage

If WeeChat is running on a remote machine, SSH key-based authentication will need to be set up so that this script can run the ssh client without being prompted to enter a password.

WeeChat also needs to be configured to [enable the FIFO pipe](https://weechat.org/files/doc/stable/weechat_user.en.html#fifo_pipe).

```
$ ./weechat_idle.py --help
usage: weechat_idle [-h] [--host HOST] [--pipe PIPE]

Switches to the 'weechat' buffer when the system idles.

optional arguments:
  -h, --help   show this help message and exit
  --host HOST  SSH host running WeeChat (for remote control)
  --pipe PIPE  location of WeeChat FIFO (defaults to ~/.weechat/weechat_fifo)
```
