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

from qtile_extras import widget
from qtile_extras.widget.decorations import BorderDecoration

# Variables
mod = "mod4"
my_terminal = "alacritty"
my_browser = "firefox"
my_file_manager = "thunar"
screenshot = "scrot -e 'mv $f ~/Pictures/screenshots/Screenshot%Y-%m-%d%H:%M:%S.png'"

# Shortcuts
keys = [

    # Launch staff
    Key([mod], "Return", lazy.spawn(my_terminal), desc="alacritty"),
    Key([mod], "b", lazy.spawn(my_browser), desc="firefox"),
    Key([mod], "d", lazy.spawn("rofi -show drun"), desc="rofi"),
    Key([mod], "t", lazy.spawn("alacritty -e htop"), desc="htop"),
    Key([mod], "f", lazy.spawn(my_file_manager), desc="thunar"),

    # Audio control
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume 0 +5%")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume 0 -5%")),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute 0 toggle")),

    # Screen brightness control
    Key([], "XF86MonBrightnessUp", lazy.spawn("xbacklight -inc 15")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("xbacklight -dec 15")),

    # Screenshot
    Key([mod], "Print", lazy.spawn(screenshot)),

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
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
]

groups = [Group(i) for i in ["WEB", "DEV", "SYS", "DOC",
                             "VBOX", "CHAT", "MUS", "VID", "GAME"]]
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
    Key([mod], "n",
        lazy.group['scratchpad'].dropdown_toggle('my_terminal')),
])

# Colors
colors = {
    "flamingo": "#F3CDCD",
    "mauve": "#DDB6F2",
    "pink": "#f5c2e7",
    "maroon": "#e8a2af",
    "red": "#f28fad",
    "peach": "#f8bd96",
    "yellow": "#fae3b0",
    "green": "#abe9b3",
    "teal": "#b4e8e0",
    "blue": "#96cdfb",
    "sky": "#89dceb",
    "white": "#d9e0ee",
    "white1": "#FAF9F6",
    "gray": "#6e6c7e",
    "black": "#1a1826",
    "black1": "#575268",
}

# Default theme for layouts
layout_theme = {
    "border_width": 2,
    "margin": 4,
    "border_focus": colors["maroon"],
    "border_normal": colors["black"],
}

# Layouts to be used
layouts = [
    layout.MonadTall(**layout_theme, ratio=0.55),
    layout.Max(),
    layout.Floating(**layout_theme),
]

# Define prompt
prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

# Default widget settings
widget_defaults = dict(
    font='JetBrainsMono Nerd Font',
    fontsize=14,
    padding=2,
    background=colors["black"],
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Image(
                    filename="~/.config/qtile/icons/python.png",
                    scale="False",
                    mouse_callbacks={
                        'Button1': lambda: qtile.cmd_spawn(my_terminal)}
                ),
                widget.TextBox(
                    text="|",
                    padding=0,
                    fontsize=12,
                    foreground='474747',
                    background=colors["black"],
                ),
                widget.GroupBox(
                    active=colors["white"],
                    inactive=colors["yellow"],
                    rounded=False,
                    highlight_color=[colors["black"]],
                    highlight_method="line",
                    this_current_screen_border=colors["blue"],
                    this_screen_border=colors["green"],
                    other_current_screen_border=colors["blue"],
                    other_screen_border=colors["green"],
                    foreground=colors["white"],
                    background=colors["black"],
                ),
                widget.TextBox(
                    text="|",
                    padding=0,
                    fontsize=12,
                    foreground='474747',
                    background=colors["black"],
                ),
                widget.CurrentLayoutIcon(
                    custom_icon_paths=[os.path.expanduser(
                        "~/.config/qtile/icons")],
                    foreground=colors["white1"],
                    background=colors["black"],
                    padding=0,
                    scale=0.7
                ),
                widget.CurrentLayout(
                    foreground=colors["white1"],
                    background=colors["black"],
                    padding=5
                ),
                widget.TextBox(
                    text="|",
                    padding=0,
                    fontsize=12,
                    foreground='474747',
                    background=colors["black"],
                ),
                widget.TaskList(
                    icon_size=0,
                    foreground=colors["white1"],
                    background=colors["black"],
                    borderwidth=1,
                    border=colors["gray"],
                    margin=0,
                    padding=1,
                    highlight_method="block",
                    title_width_method="uniform",
                    urgent_alert_method="border",
                    urgent_border=colors["mauve"],
                    rounded=False,
                    txt_floating="缾 ",
                    txt_maximized="类 ",
                    txt_minimized="絛 ",
                ),
                widget.TextBox(
                    text="|",
                    padding=0,
                    fontsize=12,
                    foreground='474747',
                    background=colors["black"],
                ),
                widget.Systray(
                    padding=0
                ),
                widget.Sep(
                    linewidth=0,
                    padding=5,
                    foreground=colors["black"],
                    background=colors["black"]
                ),
                widget.CPU(
                    format=" CPU {load_percent:04}%",
                    foreground=colors["maroon"],
                    background=colors["black"],
                    padding=5,
                    decorations=[
                        BorderDecoration(
                            colour=colors["maroon"],
                            border_width=[0, 0, 2, 0],
                        )
                    ],
                ),
                widget.Sep(
                    linewidth=0,
                    padding=5,
                    foreground=colors["black"],
                    background=colors["black"]
                ),
                widget.Memory(
                    format=' Mem {MemUsed:.0f}{mm}/{MemTotal:.0f}{mm}',
                    foreground=colors["peach"],
                    background=colors["black"],
                    padding=5,
                    decorations=[
                        BorderDecoration(
                            colour=colors["peach"],
                            border_width=[0, 0, 2, 0],
                        )
                    ],
                ),
                widget.Sep(
                    linewidth=0,
                    padding=5,
                    foreground=colors["black"],
                    background=colors["black"]
                ),
                widget.Volume(
                    fmt="墳 {}",
                    mute_command="amixer -D pulse set Master toggle",
                    foreground=colors["sky"],
                    background=colors["black"],
                    padding=5,
                    decorations=[
                        BorderDecoration(
                            colour=colors["sky"],
                            border_width=[0, 0, 2, 0],
                        )
                    ],
                ),
                widget.Sep(
                    linewidth=0,
                    padding=5,
                    foreground=colors["black"],
                    background=colors["black"]
                ),
                widget.Clock(
                    format=" %d %b - %H:%M",
                    foreground=colors["pink"],
                    background=colors["black"],
                    padding=5,
                    decorations=[
                        BorderDecoration(
                            colour=colors["pink"],
                            border_width=[0, 0, 2, 0],
                        )
                    ],
                ),
            ],
            20,
        ),
        wallpaper='~/Pictures/wallpaper/wallpaper_4.jpg',
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
    subprocess.call([home + '/.config/qtile/autostart.sh'])


wmname = "LG3D"
