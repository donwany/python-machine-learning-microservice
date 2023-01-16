from flask import Flask, request, render_template
import language_tool_python

app = Flask(__name__)


def model(text):
    # create an instance of the LanguageTool class
    tool = language_tool_python.LanguageTool('en-US')
    matches = tool.check(text)
    corrected_text = language_tool_python.utils.correct(text, matches)
    return corrected_text


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/check_grammar', methods=['POST'])
def check_grammar():
    text = request.form['text']
    # use your AI model to check grammar here
    corrected_text = model(text)
    return render_template('results.html', text=corrected_text)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
