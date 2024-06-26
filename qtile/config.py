# Imports
import os
import socket
import subprocess
from libqtile import qtile
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy
from libqtile.command import lazy
from typing import List

# Variables
mod = "mod4"
rofi_applets = os.path.expanduser('~') + '/.config/qtile/scripts/'
my_terminal = "alacritty"
my_browser = "firefox"
my_file_manager = "thunar"
screenshot = "scrot -e 'mv $f ~/Imagens/Screenshots/Screenshot_%d-%m-%Y_%H:%M:%S.png'"

# Shortcuts
keys = [

    # Launch staff
    Key([mod], "Return", lazy.spawn(my_terminal), desc="alacritty"),
    Key([mod], "b", lazy.spawn(my_browser), desc="firefox"),
    Key([mod], "d", lazy.spawn("rofi -show drun -show-icons"), desc="rofi"),
    Key([mod], "x", lazy.spawn(rofi_applets + "powermenu"), desc="powermenu"),
    Key([mod], "t", lazy.spawn("alacritty -e htop"), desc="htop"),
    Key([mod], "f", lazy.spawn(my_file_manager), desc="thunar"),

    # Audio control
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume 0 +5%")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume 0 -5%")),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute 0 toggle")),
    # Screen brightness control
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl -inc 15")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl -dec 15")),

    # Screenshot
    Key([mod], "Home", lazy.spawn(screenshot)),

    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
        ),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
]

groups = [Group("1", layout='monadtall'),
          Group("2", layout='monadtall',
                matches=[Match(wm_class=["code"])]),
          Group("3", layout='monadtall'),
          Group("4", layout='monadtall',
                matches=[Match(wm_class=["Thunar"])]),
          Group("5", layout='monadtall',
                matches=[Match(wm_class=["lxappearance", "GParted", "gsmartcontrol"])]),
          Group("6", layout='monadtall'),
          Group("7", layout='monadtall',
                matches=[Match(wm_class=["spotify"])]),
          Group("8", layout='monadtall',
                matches=[Match(wm_class=["discord-screenaudio"])]),
          Group("9", layout='monadtall',
                matches=[Match(wm_class=["steam", "lutris", "Heroic"])])
          ]

group_hotkey = "123456789"

for g, k in zip(groups, group_hotkey):
    keys.extend(
        [
            Key([mod], k, lazy.group[g.name].toscreen(),
                desc="Switch to group {}".format(g.name)),

            Key([mod, "shift"], k, lazy.window.togroup(g.name, switch_group=False),
                desc="Switch to & move focused window to group {}".format(g.name)),
        ]
    )

# Append scratchpad with dropdowns to groups
groups.append(ScratchPad('scratchpad', [
    DropDown('my_terminal', my_terminal, width=0.4,
             height=0.5, x=0.3, y=0.2, opacity=1)
]))
# extend keys list with keybinding for scratchpad
keys.extend([
    Key([mod, "shift"], "n",
        lazy.group['scratchpad'].dropdown_toggle('my_terminal')),
])

# Colors
colors = {
    "bg": '#282a36',
    "fg": '#f8f8f2',
    "cl": '#44475a',
    "black": '#21222c',
    "gray": '#808080',
    "purple": '#bd93f9',
}

# Default theme for layouts
layout_theme = {
    "border_width": 2,
    "margin": 4,
    "border_focus": colors["purple"],
    "border_normal": colors["bg"],
}

# Layouts to be used
layouts = [
    layout.MonadTall(**layout_theme, ratio=0.55),
    layout.Floating(**layout_theme),
    layout.Max(**layout_theme),
]

# Define prompt
prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

# Default widget settings
widget_defaults = dict(
    font='JetBrainsMono Nerd Font',
    fontsize=12,
    padding=2,
    background=colors["bg"],
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Sep(
                    fontsize=12,
                    foreground='474747',
                    padding=10,
                ),
                widget.CurrentLayoutIcon(
                    scale=0.7,
                    use_mask=True,
                    foreground=colors['fg'],
                    padding=0,
                ),
                widget.Sep(
                    fontsize=12,
                    foreground='474747',
                    padding=10,
                ),
                widget.GroupBox(
                    highlight_method='block',
                    this_current_screen_border=colors['purple'],
                    inactive=colors['gray'],
                    active=colors['fg'],
                    hide_unused=True,
                    disable_drag=True,
                    use_mouse_wheel=False,
                    fontsize=12,
                    padding=5,
                ),
                widget.Sep(
                    fontsize=12,
                    foreground='474747',
                    padding=10,
                ),
                widget.TextBox(
                    text='󰖲',
                    fontsize=14,
                    foreground=colors['fg'],
                    padding=5,
                ),
                widget.WindowCount(
                    text_format='{num}',
                    show_zero=True,
                    foreground=colors['purple'],
                ),
                widget.Sep(
                    fontsize=12,
                    foreground='474747',
                    padding=10,
                ),
                widget.Spacer(
                ),
                widget.TextBox(
                    text='󰃰',
                    fontsize=14,
                    foreground=colors['fg'],
                    padding=5,
                ),
                widget.Clock(
                    format='%d %b %H:%M',
                    foreground=colors['purple'],
                ),
                widget.Spacer(
                ),
                widget.Systray(
                    foreground=colors['fg'],
                    padding=5,
                ),
                widget.Sep(
                    fontsize=12,
                    foreground='474747',
                    padding=10,
                ),
                widget.TextBox(
                    text='󰕾',
                    fontsize=14,
                    foreground=colors['fg'],
                    padding=5,
                ),
                widget.Volume(
                    mute_command='amixer -D pulse set Master toggle',
                    foreground=colors['purple'],
                ),
                widget.Sep(
                    fontsize=12,
                    foreground='474747',
                    padding=10,
                ),
                widget.TextBox(
                    text='󰌌',
                    fontsize=14,
                    foreground=colors['fg'],
                    padding=5,
                ),
                widget.KeyboardLayout(
                    configured_keyboards=['us_intl'],
                    foreground=colors['purple'],
                ),
                widget.Sep(
                    fontsize=12,
                    foreground='474747',
                    padding=10,
                ),
            ],
            size=20,
            margin=[5, 5, 0, 5],
        ),
        wallpaper='~/.config/qtile/wallpaper/img-1.png',
        wallpaper_mode='fill',
    ),
]


# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
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
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None


@hook.subscribe.startup
def autostart():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/scripts/autostart'])


wmname = "LG3D"
