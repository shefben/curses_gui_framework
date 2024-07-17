# Custom Curses GUI Wrapper

This repository contains a custom curses-based GUI wrapper for building text-based user interfaces. The `Window` class manages various GUI components like textboxes, buttons, checklists, and menus, allowing for interactive console applications.

## Features

- **TextBox**: An input field with a label, supporting color configuration.
- **Button**: A clickable button that can execute actions.
- **CheckList**: A checklist item that can be toggled on and off.
- **MenuList**: A menu item that can trigger actions.
- **Mouse and Keyboard Support**: Interact with GUI elements using both mouse and keyboard.
- **Configurable Colors**: Set custom colors for text, background, highlights, and hover states for all GUI elements.
- **Validation**: Buttons can have validation logic to check for required fields.
- **Windows and Linux Sypport**
- 
## Screen Shot
![image](https://github.com/user-attachments/assets/6006c82b-d97c-47f7-acd5-fb9939f6c492)

## Example Usage

Below are some snippets demonstrating how to instantiate and use each GUI element.

### Setting Up the Window

```python
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
```

#### TextBox Parameters:
- **parent:** The parent window object (typically None when initializing).
- **y:** The y-coordinate position of the textbox.
- **x:** The x-coordinate position of the textbox.
- **label:** The label displayed next to the textbox.
- **max_length:** The maximum length of the text input.
- **is_required:** Whether the textbox input is required (default False).
- **index:** The index position for tab ordering.

### Button Example:
```python
# Create a button
button = Window.Button(None, 7, 10, "Exit", lambda: exit(), index=5)

# Configure colors for the button
button.configure_colors(
    button_color=win.rgb_to_color_pair(0, 0, 255, 0, 0, 0, 13),
    button_highlight_color=win.rgb_to_color_pair(0, 255, 255, 0, 0, 0, 14)
)

# Draw the button
button.draw()

```

#### Button Parameters:
- **parent:** The parent window object (typically None when initializing).
- **y:** The y-coordinate position of the button.
- **x:** The x-coordinate position of the button.
- **label:** The label displayed on the button.
- **action:** The function to execute when the button is pressed.
- **validate:** Whether to validate the form before executing the action (default False).
- **index:** The index position for tab ordering.

### CheckBox Example:
```python
# Create a checklist item
checklist = Window.CheckList(None, 6, 2, "Option 1", is_checked=True, index=7)

# Configure colors for the checklist item
checklist.configure_colors(
    checkbox_color=win.rgb_to_color_pair(255, 255, 0, 0, 0, 0, 15),
    x_color=win.rgb_to_color_pair(255, 0, 255, 0, 0, 0, 16),
    label_color=win.rgb_to_color_pair(0, 0, 0, 0, 0, 0, 17),
    highlight_color=win.rgb_to_color_pair(255, 255, 255, 0, 0, 0, 18)
)

# Draw the checklist item
checklist.draw()

```

#### CheckList Parameters:
- **parent:** The parent window object (typically None when initializing).
- **y:** The y-coordinate position of the checklist item.
- **x:** The x-coordinate position of the checklist item.
- **label:** The label displayed next to the checklist item.
- **is_checked:** Whether the checklist item is initially checked (default False).
- **index:** The index position for tab ordering.

### MenuList Example:
```python
Create a menu item
menu = Window.MenuList(None, 8, 2, "Menu Item 1", lambda: print("Menu Item 1 selected"), index=9)

# Configure colors for the menu item
menu.configure_colors(
    menu_color=win.rgb_to_color_pair(100, 100, 100, 0, 0, 0, 19),
    menu_highlight_color=win.rgb_to_color_pair(200, 200, 200, 0, 0, 0, 20)
)

# Draw the menu item
menu.draw()
```

#### MenuList Parameters:
- **parent:** The parent window object (typically None when initializing).
- **y:** The y-coordinate position of the MenuList item.
- **x:** The x-coordinate position of the MenuList item.
- **label:** The label displayed next to the MenuList item.
- **action:** The function to execute when the MenuList item is selected.
- **index:** The index position for tab ordering.

### Label Example:
```python
class Label:
    def __init__(self, parent, y, x, text, index=0):
        self.parent = parent
        self.y = y
        self.x = x
        self.text = text
        self.index = index

    def draw(self):
        self.parent.screen.addstr(self.y, self.x, self.text)

# Create and draw a label
label = Label(None, 1, 2, "This is a label", index=0)
label.draw()
```

### Header Example:
```python
class Header:
    def __init__(self, parent, y, x, text, index=0):
        self.parent = parent
        self.y = y
        self.x = x
        self.text = text
        self.index = index

    def draw(self):
        self.parent.screen.addstr(self.y, self.x, self.text, curses.A_BOLD)

# Create and draw a header
header = Header(None, 0, 2, "This is a header", index=0)
header.draw()
```

### Data/TextBox Validation W/ Button to execute validation:
```python
# Create a textbox and set it as required
textbox = Window.TextBox(None, 2, 2, "Enter the admin server IP: ", 50, True, index=1)

# Create a button with validation
button = Window.Button(None, 7, 50, "Submit", lambda **kwargs: print("Form submitted with values:", kwargs), validate=True, index=6)

# Draw the button and textbox
textbox.draw()
button.draw()

# Execute the button action with validation
button.execute_action()
```

### Indexing / Tab Order Example:
```python
# Create multiple GUI elements with different indices
textbox1 = Window.TextBox(None, 2, 2, "First Textbox: ", 50, True, index=1)
textbox2 = Window.TextBox(None, 3, 2, "Second Textbox: ", 50, True, index=2)
button = Window.Button(None, 4, 2, "Submit", lambda **kwargs: print("Form submitted"), index=3)

# Tab order will follow the index values
components = [textbox1, textbox2, button]

# Draw the components
for component in components:
    component.draw()
```

## License

This project is licensed under the Creative Commons Attribution 4.0 International (CC BY 4.0) License. You are free to use, share, and adapt the code as long as proper credit is given. For more information, see the [LICENSE](./LICENSE) file or visit [https://creativecommons.org/licenses/by/4.0/](https://creativecommons.org/licenses/by/4.0/).





