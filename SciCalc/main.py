from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
import math

# i using back ground color black for professional( code )
Window.clearcolor = (0.08, 0.08, 0.08, 1)


class Calculator(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=10, **kwargs)

        self.display = TextInput(
            multiline=False,
            readonly=True,
            halign='right',
            font_size=36,
            size_hint=(1, 0.2),
            background_color=(0.15, 0.15, 0.15, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1)
        )
        self.add_widget(self.display)

        buttons = [
            ['(', ')', 'π', '⌫'],
            ['sin', 'cos', 'tan', '√'],
            ['log', 'ln', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['C', '0', '.', '=']
        ]

        grid = GridLayout(cols=4, spacing=8)

        for row in buttons:
            for text in row:
                btn = Button(
                    text=text,
                    font_size=22,
                    background_normal='',
                    background_color=self.get_btn_color(text),
                    color=(1, 1, 1, 1)
                )
                btn.bind(on_press=self.on_button_press)
                grid.add_widget(btn)

        self.add_widget(grid)

    def get_btn_color(self, text):
        if text == '=':
            return (0.2, 0.6, 1, 1)        # Blue
        elif text in ('+', '-', '*', '/', '%'):
            return (0.35, 0.35, 0.35, 1)  # Operator
        elif text in ('C', '⌫'):
            return (0.7, 0.2, 0.2, 1)     # Red
        else:
            return (0.2, 0.2, 0.2, 1)     # Normal

    def on_button_press(self, instance):
        text = instance.text

        if text == '⌫':
            self.display.text = self.display.text[:-1]

        elif text == 'C':
            self.display.text = ''

        elif text == '=':
            try:
                expr = self.display.text
                expr = expr.replace('sin(', '*sin(').replace('cos(', '*cos(')
                expr = expr.replace('tan(', '*tan(').replace('log(', '*log(')
                expr = expr.replace('ln(', '*ln(').replace('sqrt(', '*sqrt(')
                expr = expr.replace('pi', f'*{math.pi}')
                if expr.startswith('*'):
                    expr = expr[1:]

                expr += ')' * (expr.count('(') - expr.count(')'))

                result = eval(expr, {
                    "sin": math.sin,
                    "cos": math.cos,
                    "tan": math.tan,
                    "log": math.log10,
                    "ln": math.log,
                    "sqrt": math.sqrt
                })

                self.display.text = str(result)
            except:
                self.display.text = 'Error'

        elif text in ('sin', 'cos', 'tan', 'log', 'ln'):
            self.display.text += f'{text}('

        elif text == '√':
            self.display.text += 'sqrt('

        elif text == 'π':
            self.display.text += 'pi'

        elif text == '%':
            try:
                self.display.text = str(float(self.display.text) / 100)
            except:
                self.display.text = 'Error'

        elif text == '.':
            if not self.display.text or self.display.text[-1] in '+-*/(':
                self.display.text += '0.'
            elif '.' not in self.display.text.split()[-1]:
                self.display.text += '.'

        else:
            self.display.text += text


class SciCalculatorApp(App):
    def build(self):
        return Calculator()


SciCalculatorApp().run()
