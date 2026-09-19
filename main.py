from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle
import math

Window.clearcolor = (0.035, 0.04, 0.055, 1)


class ProButton(Button):
    def __init__(self, bg=(0.11, 0.13, 0.17, 1), **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)
        self.color = (1, 1, 1, 1)
        self.font_size = dp(23)

        with self.canvas.before:
            Color(*bg)
            self.shape = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(22)]
            )

        self.bind(pos=self.update_shape, size=self.update_shape)

    def update_shape(self, *args):
        self.shape.pos = self.pos
        self.shape.size = self.size


class Calculator(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(12),
            **kwargs
        )

        self.expression = ""
        self.history = []
        self.dark = True

        top = BoxLayout(size_hint_y=0.09, spacing=dp(10))

        title = Label(
            text="CALCULATOR",
            font_size=dp(18),
            bold=True,
            color=(0.65, 0.75, 1, 1)
        )

        history = Button(
            text="HISTORY",
            font_size=dp(13),
            background_normal="",
            background_color=(0.12, 0.16, 0.23, 1),
            color=(0.75, 0.83, 1, 1)
        )
        history.bind(on_press=self.show_history)

        mode = Button(
            text="☀",
            font_size=dp(21),
            background_normal="",
            background_color=(0.12, 0.16, 0.23, 1)
        )
        mode.bind(on_press=self.change_mode)

        top.add_widget(title)
        top.add_widget(history)
        top.add_widget(mode)
        self.add_widget(top)

        display_box = BoxLayout(
            orientation="vertical",
            padding=[dp(10), dp(15)],
            size_hint_y=0.22
        )

        self.small_display = Label(
            text="",
            font_size=dp(18),
            color=(0.45, 0.50, 0.60, 1),
            halign="right"
        )

        self.display = Label(
            text="0",
            font_size=dp(46),
            bold=True,
            color=(1, 1, 1, 1),
            halign="right"
        )

        display_box.add_widget(self.small_display)
        display_box.add_widget(self.display)
        self.add_widget(display_box)

        grid = GridLayout(
            cols=4,
            spacing=dp(10),
            size_hint_y=0.69
        )

        buttons = [
            ("AC", "clear"), ("⌫", "back"), ("(", "normal"), (")", "normal"),
            ("√", "sqrt"), ("%", "percent"), ("±", "sign"), ("÷", "operator"),
            ("7", "normal"), ("8", "normal"), ("9", "normal"), ("×", "operator"),
            ("4", "normal"), ("5", "normal"), ("6", "normal"), ("−", "operator"),
            ("1", "normal"), ("2", "normal"), ("3", "normal"), ("+", "operator"),
            ("0", "normal"), (".", "normal"), ("=", "equal"), ("⌫", "back")
        ]

        for text, action in buttons:
            if action == "operator":
                color = (0.12, 0.38, 0.82, 1)
            elif action == "equal":
                color = (0.20, 0.60, 0.35, 1)
            elif action in ["clear", "back", "sqrt", "percent", "sign"]:
                color = (0.22, 0.25, 0.31, 1)
            else:
                color = (0.11, 0.13, 0.17, 1)

            btn = ProButton(bg=color, text=text)

            if text == "=":
                btn.font_size = dp(29)
                btn.bold = True

            btn.bind(
                on_press=lambda button, a=action:
                self.press(button.text, a)
            )

            grid.add_widget(btn)

        self.add_widget(grid)

    def press(self, value, action):
        if action == "clear":
            self.expression = ""
            self.small_display.text = ""
            self.display.text = "0"
            return

        if action == "back":
            self.expression = self.expression[:-1]

        elif action == "sqrt":
            try:
                number = eval(
                    self.expression,
                    {"__builtins__": None},
                    {}
                )
                result = math.sqrt(number)
                self.small_display.text = "√" + self.expression
                self.expression = str(result)
            except:
                self.show_error()
                return

        elif action == "percent":
            try:
                number = eval(
                    self.expression,
                    {"__builtins__": None},
                    {}
                )
                result = number / 100
                self.small_display.text = self.expression + "%"
                self.expression = str(result)
            except:
                self.show_error()
                return

        elif action == "sign":
            if self.expression:
                self.expression = "-" + self.expression

        elif action == "operator":
            if value == "×":
                value = "*"
            elif value == "÷":
                value = "/"
            elif value == "−":
                value = "-"

            if self.expression:
                self.expression += value

        elif action == "equal":
            self.calculate()
            return

        else:
            self.expression += value

        self.display.text = self.expression or "0"

    def calculate(self):
        try:
            allowed = "0123456789+-*/(). "

            if not self.expression:
                return

            if not all(c in allowed for c in self.expression):
                raise ValueError

            result = eval(
                self.expression,
                {"__builtins__": None},
                {}
            )

            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)

            old = self.expression
            self.small_display.text = old + " ="
            self.expression = str(result)
            self.display.text = str(result)

            self.history.append(
                old + " = " + str(result)
            )

        except:
            self.show_error()

    def show_error(self):
        self.display.text = "Error"
        self.expression = ""

    def show_history(self, instance):
        content = BoxLayout(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10)
        )

        text = "\n".join(self.history[-20:]) if self.history else "No calculations yet."

        label = Label(
            text=text,
            font_size=dp(17),
            halign="left"
        )

        close = Button(
            text="CLOSE",
            size_hint_y=0.15,
            background_normal="",
            background_color=(0.12, 0.38, 0.82, 1)
        )

        content.add_widget(label)
        content.add_widget(close)

        popup = Popup(
            title="Calculation History",
            content=content,
            size_hint=(0.9, 0.75)
        )

        close.bind(on_press=popup.dismiss)
        popup.open()

    def change_mode(self, instance):
        self.dark = not self.dark

        if self.dark:
            Window.clearcolor = (0.035, 0.04, 0.055, 1)
            self.display.color = (1, 1, 1, 1)
        else:
            Window.clearcolor = (0.92, 0.93, 0.96, 1)
            self.display.color = (0.05, 0.05, 0.07, 1)


class CalculatorApp(App):
    def build(self):
        self.title = "Calculator Pro"
        return Calculator()


CalculatorApp().run()
