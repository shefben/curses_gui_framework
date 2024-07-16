import curses
import time

class Window:
    def __init__(self, screen, textboxes, buttons, checklists, menus):
        self.screen = screen
        self.initialize_curses()
        self.textboxes = textboxes
        self.buttons = buttons
        self.checklists = checklists
        self.menus = menus
        self.components = self.textboxes + self.buttons + self.checklists + self.menus
        self.components.sort(key=lambda c: c.index)  # Sort components by their index
        self.current_index = 0

        for textbox in self.textboxes:
            textbox.parent = self
        for button in self.buttons:
            button.parent = self
        for checklist in self.checklists:
            checklist.parent = self
        for menu in self.menus:
            menu.parent = self

    def initialize_curses(self):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.mousemask(curses.ALL_MOUSE_EVENTS)
        curses.curs_set(1)
        self.screen.clear()

    def rgb_to_color_pair(self, fg_r, fg_g, fg_b, bg_r, bg_g, bg_b, pair_id):
        curses.init_color(pair_id, int(fg_r * 1000 / 255), int(fg_g * 1000 / 255), int(fg_b * 1000 / 255))
        bg_color_id = pair_id + 100  # Avoid collision with other color pairs
        curses.init_color(bg_color_id, int(bg_r * 1000 / 255), int(bg_g * 1000 / 255), int(bg_b * 1000 / 255))
        curses.init_pair(pair_id, pair_id, bg_color_id)
        return curses.color_pair(pair_id)

    class TextBox:
        def __init__(self, parent, y, x, label, max_length, is_required=False, index=0):
            self.parent = parent
            self.y = y
            self.x = x
            self.label = label
            self.max_length = max_length
            self.text = ""
            self.is_required = is_required
            self.active = False
            self.index = index

            self.label_color = curses.color_pair(4)
            self.label_bg_color = curses.color_pair(4)
            self.textbox_color = curses.color_pair(4)
            self.textbox_bg_color = curses.color_pair(4)
            self.textbox_highlight_color = curses.color_pair(3)
            self.textbox_highlight_bg_color = curses.color_pair(3)

        def configure_colors(self, label_color, label_bg_color, textbox_color, textbox_bg_color, textbox_highlight_color, textbox_highlight_bg_color):
            self.label_color = label_color
            self.label_bg_color = label_bg_color
            self.textbox_color = textbox_color
            self.textbox_bg_color = textbox_bg_color
            self.textbox_highlight_color = textbox_highlight_color
            self.textbox_highlight_bg_color = textbox_highlight_bg_color

        def draw(self):
            attr = self.textbox_highlight_color if self.active else self.textbox_color
            bg_attr = self.textbox_highlight_bg_color if self.active else self.textbox_bg_color
            self.parent.screen.addstr(self.y, self.x, self.label, self.label_color | self.label_bg_color)
            self.parent.screen.addstr(self.y, self.x + len(self.label), self.text + ' ' * (self.max_length - len(self.text)), attr | bg_attr)
            if self.active:
                self.parent.screen.move(self.y, self.x + len(self.label) + len(self.text))

        def handle_input(self, key):
            if key == chr(127) or key == chr(8):  # Handling backspace
                self.text = self.text[:-1]
            elif isinstance(key, str) and len(self.text) < self.max_length:
                self.text += key
            self.draw()

    class Button:
        def __init__(self, parent, y, x, label, action, validate=False, index=0):
            self.parent = parent
            self.y = y
            self.x = x
            self.label = label
            self.action = action
            self.validate = validate
            self.active = False
            self.index = index

            self.button_color = curses.color_pair(2)
            self.button_highlight_color = curses.color_pair(3)

        def configure_colors(self, button_color, button_highlight_color):
            self.button_color = button_color
            self.button_highlight_color = button_highlight_color

        def draw(self):
            attr = self.button_highlight_color if self.active else self.button_color
            self.parent.screen.addstr(self.y, self.x, f"[ {self.label} ]", attr)

        def check_click(self, my, mx):
            if my == self.y and mx >= self.x and mx < self.x + len(f"[ {self.label} ]"):
                self.execute_action()

        def execute_action(self):
            if self.validate:
                errors = []
                for textbox in self.parent.textboxes:
                    if textbox.is_required and not textbox.text.strip():
                        errors.append(f"Error: '{textbox.label.strip()}' is required and cannot be empty.")
                if errors:
                    self.parent.screen.addstr(9, 10, "Validation Errors:", curses.color_pair(1))
                    for idx, error in enumerate(errors, start=1):
                        self.parent.screen.addstr(9 + idx, 10, error, curses.color_pair(1))
                    return
            self.action(**self.parent.get_textbox_values())

    class CheckList:
        def __init__(self, parent, y, x, label, is_checked=False, index=0):
            self.parent = parent
            self.y = y
            self.x = x
            self.label = label
            self.is_checked = is_checked
            self.active = False
            self.index = index

            self.checkbox_color = curses.color_pair(2)
            self.x_color = curses.color_pair(2)
            self.label_color = curses.color_pair(2)
            self.highlight_color = curses.color_pair(3)

            self.last_toggle_time = 0
            self.debounce_time = 0.3  # Debounce time in seconds

        def configure_colors(self, checkbox_color, x_color, label_color, highlight_color):
            self.checkbox_color = checkbox_color
            self.x_color = x_color
            self.label_color = label_color
            self.highlight_color = highlight_color

        def draw(self):
            status = "[ x ]" if self.is_checked else "[   ]"
            attr = self.highlight_color if self.active else self.label_color
            self.parent.screen.addstr(self.y, self.x, status, self.checkbox_color)
            self.parent.screen.addstr(self.y, self.x + 5, self.label, attr)

        def toggle(self):
            current_time = time.time()
            if current_time - self.last_toggle_time > self.debounce_time:
                self.is_checked = not self.is_checked
                self.last_toggle_time = current_time

    class MenuList:
        def __init__(self, parent, y, x, label, action, index=0):
            self.parent = parent
            self.y = y
            self.x = x
            self.label = label
            self.action = action
            self.active = False
            self.index = index

            self.menu_color = curses.color_pair(2)
            self.menu_highlight_color = curses.color_pair(3)

        def configure_colors(self, menu_color, menu_highlight_color):
            self.menu_color = menu_color
            self.menu_highlight_color = menu_highlight_color

        def draw(self):
            attr = self.menu_highlight_color if self.active else self.menu_color
            self.parent.screen.addstr(self.y, self.x, self.label, attr)

        def execute_action(self):
            self.action()

    def main_loop(self):
        while True:
            for component in self.components:
                component.draw()

            self.place_cursor()
            key = self.screen.getch()

            if key == curses.KEY_MOUSE:
                _, mx, my, _, _ = curses.getmouse()
                for i, component in enumerate(self.components):
                    component.active = False
                    if isinstance(component, Window.TextBox):
                        if my == component.y and mx >= component.x + len(component.label) and mx < component.x + len(component.label) + component.max_length:
                            self.current_index = i
                            component.active = True
                    elif isinstance(component, Window.Button):
                        if my == component.y and mx >= component.x and mx < component.x + len(f"[ {component.label} ]"):
                            self.current_index = i
                            component.active = True
                            component.execute_action()
                    elif isinstance(component, Window.CheckList):
                        if my == component.y and mx >= component.x and mx < component.x + len("[ x ]") + len(component.label):
                            self.current_index = i
                            component.active = True
                            component.toggle()
                    elif isinstance(component, Window.MenuList):
                        if my == component.y and mx >= component.x and mx < component.x + len(component.label):
                            self.current_index = i
                            component.active = True
                            component.execute_action()

            elif key in [curses.KEY_BACKSPACE, 127, 8]:
                if isinstance(self.components[self.current_index], Window.TextBox):
                    self.components[self.current_index].handle_input(chr(key))

            elif key in [curses.KEY_UP, 353]:
                self.components[self.current_index].active = False
                self.current_index = (self.current_index - 1) % len(self.components)
                self.components[self.current_index].active = True

            elif key in [curses.KEY_DOWN, 9]:
                self.components[self.current_index].active = False
                self.current_index = (self.current_index + 1) % len(self.components)
                self.components[self.current_index].active = True

            elif key in [curses.KEY_ENTER, 10, 13]:
                if isinstance(self.components[self.current_index], Window.Button):
                    self.components[self.current_index].execute_action()
                elif isinstance(self.components[self.current_index], Window.CheckList):
                    self.components[self.current_index].toggle()
                elif isinstance(self.components[self.current_index], Window.MenuList):
                    self.components[self.current_index].execute_action()
                else:
                    self.components[self.current_index].active = False
                    self.current_index = (self.current_index + 1) % len(self.components)
                    self.components[self.current_index].active = True

            elif 32 <= key <= 126:
                if isinstance(self.components[self.current_index], Window.TextBox):
                    self.components[self.current_index].handle_input(chr(key))

            self.screen.refresh()

    def place_cursor(self):
        if isinstance(self.components[self.current_index], Window.TextBox):
            tb = self.components[self.current_index]
            self.screen.move(tb.y, tb.x + len(tb.label) + len(tb.text))

    def submit_form(self, **kwargs):
        self.screen.addstr(9, 10, "Form submitted successfully!", curses.color_pair(1))

    def exit_form(self):
        raise SystemExit("Exiting application")

    def get_textbox_values(self):
        return {textbox.label.strip().replace(" ", "_").lower(): textbox.text for textbox in self.textboxes}

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
