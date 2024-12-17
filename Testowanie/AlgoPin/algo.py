import random
import string
from flask import Flask, render_template_string, request

class CodeGenerator:
    def __init__(self, length: int):
        if length not in [4, 6, 12, 16]:
            raise ValueError("Długość kodu musi mieć tyle cyfr: 4, 6, 12, 16")
        
        self.length = length
        self.code = self._generate_code()
        
    def _generate_code(self) -> str:
        if self.length in [4, 6]:
            charset = string.digits
        else:
            charset = string.digits + string.ascii_letters
        return ''.join(random.choice(charset) for _ in range(self.length))
    
    def show_code(self) -> str:
        return self.code

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8" />
    <title>Generator kodów</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 50px;
        }
        .container {
            max-width: 400px;
        }
        input[type="text"], select {
            width: 100%;
            padding: 0.5em;
            margin-bottom: 1em;
        }
        button {
            padding: 0.7em 1.2em;
            margin-right: 1em;
        }
        .result {
            margin-top: 1em;
            font-size: 1.2em;
            font-weight: bold;
            color: #333;
            word-break: break-all;
        }
    </style>
</head>
<body>
    <section class="container">
        <h1>Generator kodów</h1>
        <form method="POST">
            <label for="length">Wybierz długość kodu:</label>
            <select name="length" id="length">
                <option value="4" {% if length == 4 %}selected{% endif %}>4 (PIN)</option>
                <option value="6" {% if length == 6 %}selected{% endif %}>6 (PIN)</option>
                <option value="12" {% if length == 12 %}selected{% endif %}>12 (TOKEN)</option>
                <option value="16" {% if length == 16 %}selected{% endif %}>16 (TOKEN)</option>
            </select>
            
            <button type="submit" name="action" value="generate">Generuj</button>
        </form>
        
        {% if code %}
        <div class="result">
            Wygenerowany kod: {{ code }}
        </div>
        {% endif %}
        
        {% if message %}
        <div class="result">
            {{ message }}
        </div>
        {% endif %}
    </section>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    code = None
    message = None
    length = None
    
    if request.method == 'POST':
        action = request.form.get('action')
        length = request.form.get('length', type=int)
        
        if action == 'generate':
            try:
                generator = CodeGenerator(length)
                code = generator.show_code()
            except ValueError as e:
                message = str(e)
    else:
        length = 4
    return render_template_string(HTML_TEMPLATE, code=code, message=message, length=length)

if __name__ == '__main__':
    app.run(debug=True)