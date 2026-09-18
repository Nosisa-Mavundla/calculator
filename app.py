"""
Simple Calculator (Flask + HTML/CSS)
-------------------------------------
A calculator with a real button-grid UI. All calculation logic runs in
Python on the server; the page is plain HTML/CSS with no JavaScript.
Each button press submits a small form back to Flask, which updates the
current expression and re-renders the display.
"""

import ast
import operator
from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-me"  # only needed to keep session state

# Only these operators are allowed when evaluating an expression.
SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
}


def safe_eval(expression: str) -> float:
    """
    Safely evaluate a simple arithmetic expression (numbers, +, -, *, /)
    without using Python's built-in eval() on arbitrary input.
    """
    node = ast.parse(expression, mode="eval").body
    return _eval_node(node)


def _eval_node(node):
    if isinstance(node, ast.BinOp) and type(node.op) in SAFE_OPERATORS:
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return SAFE_OPERATORS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in SAFE_OPERATORS:
        return SAFE_OPERATORS[type(node.op)](_eval_node(node.operand))
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    raise ValueError("Invalid expression")


@app.route("/", methods=["GET"])
def index():
    expression = session.get("expression", "")
    return render_template("index.html", expression=expression or "0")


@app.route("/press", methods=["POST"])
def press():
    key = request.form.get("key", "")
    expression = session.get("expression", "")

    if key == "C":
        expression = ""
    elif key == "DEL":
        expression = expression[:-1]
    elif key == "=":
        try:
            result = safe_eval(expression)
            # Show integers without a trailing ".0"
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            expression = str(result)
        except (ValueError, ZeroDivisionError, SyntaxError):
            expression = "Error"
    else:
        # Prevent building an invalid expression after an error
        if expression == "Error":
            expression = ""
        expression += key

    session["expression"] = expression
    return render_template("index.html", expression=expression or "0")


if __name__ == "__main__":
    app.run(debug=True)
