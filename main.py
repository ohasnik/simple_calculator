from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QVBoxLayout, QWidget, QLineEdit
from PySide6.QtCore import Qt
import math


class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Simple Calculator')
        self.setGeometry(100, 100, 400, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.layout.addWidget(self.display)

        self.buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
            ('0', 3, 0), ('.', 3, 1), ('=', 3, 2), ('+', 3, 3),
            ('(', 4, 0), (')', 4, 1), ('sqrt', 4, 2), ('^2', 4, 3),
            ('^3', 5, 0), ('sin', 5, 1), ('cos', 5, 2), ('tan', 5, 3),
            ('cot', 6, 0), ('sec', 6, 1), ('csc', 6, 2), ('arcsin', 6, 3),
            ('arccos', 7, 0), ('arctan', 7, 1), ('arccot', 7, 2), ('arcsec', 7, 3),
            ('arccsc', 8, 0), ('CE', 8, 1), ('C', 8, 2), ('<-', 8, 3)
        ]

        self.grid_layout = QGridLayout()
        self.layout.addLayout(self.grid_layout)

        for button_text, row, col in self.buttons:
            button = QPushButton(button_text)
            button.clicked.connect(self.on_button_clicked)
            self.grid_layout.addWidget(button, row, col)

        self.current_expression = ''

    def on_button_clicked(self):
        button = self.sender()
        button_text = button.text()

        if button_text == '=':
            try:
                result = str(self.evaluate_expression(self.current_expression))
                self.display.setText(result)
                self.current_expression = result
            except Exception:
                self.display.setText('Error')
                self.current_expression = ''
        elif button_text == 'CE':
            self.current_expression = ''
            self.display.setText('')
        elif button_text == 'C':
            self.current_expression = self.current_expression[:-1]
            self.display.setText(self.current_expression)
        elif button_text == '<-':
            if len(self.current_expression) > 0:
                self.current_expression = self.current_expression[:-1]
                self.display.setText(self.current_expression)
        else:
            self.current_expression += button_text
            self.display.setText(self.current_expression)

    def evaluate_expression(self, expr):
        expr = expr.replace('^2', '**2').replace('^3', '**3')
        expr = expr.replace('sqrt', 'math.sqrt')
        expr = expr.replace('sin', 'math.sin').replace('cos', 'math.cos')
        expr = expr.replace('tan', 'math.tan').replace('cot', '1 / math.tan')
        expr = expr.replace('sec', '1 / math.cos').replace('csc', '1 / math.sin')
        expr = expr.replace('arcsin', 'math.asin').replace('arccos', 'math.acos')
        expr = expr.replace('arctan', 'math.atan').replace('arccot', 'math.atan2(1, x)')
        expr = expr.replace('arcsec', 'math.acos(1 / x)').replace('arccsc', 'math.asin(1 / x)')

        for func in ['arccot', 'arcsec', 'arccsc']:
            if func in expr:
                x = self.extract_value(expr, func)
                expr = expr.replace(f'{func}({x})', f'{self.math_function(func, x)}')

        expr = self.balance_parentheses(expr)

        return eval(expr, {"math": math})

    def extract_value(self, expr, func):
        start = expr.index(f'{func}(') + len(f'{func}(')
        end = expr.index(')', start)
        return expr[start:end].strip()

    def math_function(self, func, x):
        if func == 'arccot':
            return math.atan2(1, x)
        elif func == 'arcsec':
            return math.acos(1 / x)
        elif func == 'arccsc':
            return math.asin(1 / x)

    def balance_parentheses(self, expr):
        open_count = expr.count('(')
        close_count = expr.count(')')
        if open_count > close_count:
            expr += ')' * (open_count - close_count)
        return expr


if __name__ == "__main__":
    app = QApplication([])
    calculator = Calculator()
    calculator.show()
    app.exec()
