# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from os import path
from subprocess import Popen, check_output
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

home = path.expanduser('~')
qconf = home + "/.config/qtile/"

mod = "mod4"

terminal = guess_terminal()
rr = qconf + "recordrofi"
volmute = qconf + "vol.sh mute"
volup = qconf + "vol.sh up"
voldown = qconf + "vol.sh down"
sstool = "flameshot gui"
rofi= home + "/.config/rofi/launchers/type-7/launcher.sh"

col_selected="#75bd75"
col_unselected="#333333"

city="Tashkent"

autostart_sh = qconf + "autostart.sh"
getlayout = qconf + "getlayout.sh"


# Custom keyboard widget
class KbWidget(widget.TextBox):
    
    def update_self(self):
        layout = check_output([getlayout]).decode().strip()
        self.text = str(layout)
        self.draw()
    
    def __init__(self, **config):
        super().__init__("", **config)
        self.update_self()


kbl = KbWidget()

@hook.subscribe.startup_once
def autostart():
    Popen([autostart_sh])

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "shift"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

    Key([mod], "f", lazy.window.toggle_floating(), desc="Toggle floating"),
    Key([mod], "d", lazy.spawn(rofi), desc="Launch Rofi"),
    Key([], "XF86AudioMute", lazy.spawn(volmute), desc="Toggle mute"),
    Key([], "XF86AudioLowerVolume", lazy.spawn(voldown), desc="Lower volume"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn(volup), desc="Raise volume"),
    Key([], "ISO_Next_Group", lazy.function(lambda q: q.current_screen.top.widgets[kbindex].update_self()), desc="Next keyboard layout."),
    Key([], "Print", lazy.spawn(sstool), desc="Take screenshot"),


]

groups = [Group(i) for i in "123456"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            #Key(
            #    [mod, "shift"],
            #    i.name,
            #    lazy.window.togroup(i.name, switch_group=True),
            #    desc="Switch to & move focused window to group {}".format(i.name),
            #),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
                 desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Columns(
        border_width=3,
        border_focus=col_selected,
        border_normal=col_unselected,
    ),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]



widget_defaults = dict(
    font="JetBrains Mono, Bold",
    fontsize=16,
    foreground="#ebdbb2",
    fontshadow="#000000",
    padding=4,
)
extension_defaults = widget_defaults.copy()

separator="  ┇  "
block="[{}]"

screens = [
    Screen(
        top=bar.Bar(
            [
                #widget.CurrentLayout(),
                widget.Image(filename=qconf + "logo.png", margin=3),
                widget.GroupBox(
                    highlight_method="block",
                    borderwidth=4,
                    this_current_screen_border=col_selected,
                    inactive="#505050"
                ),
                widget.TextBox(" ┇  "),
                widget.Prompt(),
                widget.WindowName(),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                #widget.TextBox("default config", name="default"),
                #widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                widget.Wttr(location={city: "Home"}, fmt=block),
                widget.TextBox(separator),
                kbl,
                #widget.KeyboardLayout(
                #    fmt=block,
                #    configured_keyboards=['us', 'ru'],
                #    display_map={"us": "🇺🇸", "ru": "🇷🇺"}
                #),
                widget.TextBox(separator),
                widget.Battery(
                    fmt=block
                    #format="[ {char}  {percent:2.0%} ]"
                ),
                widget.TextBox(separator),
                widget.Clock(format="%Y-%m-%d %a %H:%M", fmt=block),
                widget.TextBox(" "),
                widget.Systray(),
                #widget.QuickExit(),
            ],
            32,
            background="#1d2021",
            border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            border_color=["3c3836", "000000", "3c3836", "000000"]  # Borders are grey 
        ),
    ),
]

# Getting index of the KbWidget (Very easy method)
kbindex = next((index for index, obj in enumerate(screens[0].top.widgets) if obj == kbl), None)

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = True 
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry

        Match(title="mpv"),
        Match(title="feh"),
    ],
    border_focus=col_selected,
    border_normal=col_unselected,
    border_width=3
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "🚀 Blazing 🚀 Fast 🚀 Qtile 🚀"
