import curses

from custom_gui_utils import Window


def main(screen):
    textboxes = [
        Window.TextBox(None, 2, 2, "Enter the admin server IP: ", 50, True, index=1),
        Window.TextBox(None, 3, 2, "Enter the admin server port: (Default: 32666) ", 50, True, index=2),
        Window.TextBox(None, 4, 2, "Enter the admin username: ", 50, True, index=3),
        Window.TextBox(None, 5, 2, "Enter the admin password: ", 50, True, index=4)
    ]
    buttons = [
        Window.Button(None, 7, 10, "Exit", lambda: exit(kwargs), index=5),
        Window.Button(None, 7, 50, "Submit", lambda **kwargs: print("Form submitted with values:", kwargs), validate=True, index=6)
    ]
    checklists = [
        Window.CheckList(None, 6, 2, "Option 1", is_checked=True, index=7),
        Window.CheckList(None, 6, 20, "Option 2", is_checked=False, index=8)
    ]
    menus = [
        Window.MenuList(None, 8, 2, "Menu Item 1", lambda: print("Menu Item 1 selected"), index=9),
        Window.MenuList(None, 9, 2, "Menu Item 2", lambda: print("Menu Item 2 selected"), index=10)
    ]

    win = Window(screen, textboxes, buttons, checklists, menus)

    # Example color configurations
    win.textboxes[0].configure_colors(
        win.rgb_to_color_pair(255, 255, 255, 0, 0, 0, 10),  # label color
        win.rgb_to_color_pair(0, 0, 0, 255, 255, 255, 21),  # label background color
        win.rgb_to_color_pair(255, 0, 0, 0, 0, 0, 11),      # textbox color
        win.rgb_to_color_pair(0, 0, 0, 255, 255, 255, 22),  # textbox background color
        win.rgb_to_color_pair(0, 255, 0, 0, 0, 0, 12),      # textbox highlight color
        win.rgb_to_color_pair(0, 0, 0, 0, 255, 0, 23)       # textbox highlight background color
    )
    win.buttons[0].configure_colors(win.rgb_to_color_pair(0, 0, 255, 0, 0, 0, 13), win.rgb_to_color_pair(0, 255, 255, 0, 0, 0, 14))
    win.checklists[0].configure_colors(win.rgb_to_color_pair(255, 255, 0, 0, 0, 0, 15), win.rgb_to_color_pair(255, 0, 255, 0, 0, 0, 16), win.rgb_to_color_pair(0, 0, 0, 0, 0, 0, 17), win.rgb_to_color_pair(255, 255, 255, 0, 0, 0, 18))
    win.menus[0].configure_colors(win.rgb_to_color_pair(100, 100, 100, 0, 0, 0, 19), win.rgb_to_color_pair(200, 200, 200, 0, 0, 0, 20))

    win.main_loop()


if __name__ == "__main__":
    curses.wrapper(main)
