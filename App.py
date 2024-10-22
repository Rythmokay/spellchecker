from flask import Flask, request, render_template
from spell_checker import SpellCheckerModule
from textblob import TextBlob  # Import TextBlob

app = Flask(__name__)
spell_checker_module = SpellCheckerModule()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/spell', methods=['POST'])
def spell():
    corrected_text = ""
    corrected_grammar = []
    misspelled_words = []
    
    if request.method == 'POST':
        text = request.form.get('text', '')
        corrected_text = spell_checker_module.correct_spell(text)
        corrected_grammar, _ = spell_checker_module.correct_grammar(text)

        # Extract misspelled words
        for word in text.split():
            corrected_word = str(TextBlob(word).correct())
            if word != corrected_word:
                misspelled_words.append((word, corrected_word))
    
    return render_template('index.html', corrected_text=corrected_text, corrected_grammar=corrected_grammar, misspelled_words=misspelled_words)

@app.route('/grammar', methods=['POST'])
def grammar():
    corrected_file_text = ""
    corrected_file_grammar = []
    misspelled_words = []
    
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            readable_file = file.read().decode('utf-8', errors='ignore')
            corrected_file_text = spell_checker_module.correct_spell(readable_file)
            corrected_file_grammar, _ = spell_checker_module.correct_grammar(readable_file)

            # Extract misspelled words
            for word in readable_file.split():
                corrected_word = str(TextBlob(word).correct())
                if word != corrected_word:
                    misspelled_words.append((word, corrected_word))

    return render_template('index.html', corrected_file_text=corrected_file_text, corrected_file_grammar=corrected_file_grammar, misspelled_words=misspelled_words)

# Main execution block
if __name__ == "__main__":
    app.run(debug=True)
