from textblob import TextBlob
import language_tool_python

class SpellCheckerModule:
    def __init__(self):
        try:
            self.tool = language_tool_python.LanguageTool('en-US')
        except Exception as e:
            print(f"Failed to initialize LanguageTool: {str(e)}")
            self.tool = None  # Set tool to None if it fails

    def correct_spell(self, text):
        words = text.split()
        corrected_words = [str(TextBlob(word).correct()) for word in words]
        return " ".join(corrected_words)

    def correct_grammar(self, text):
        if not self.tool:
            return [], 0  # Return empty if tool is not available

        matches = self.tool.check(text)
        corrections = [(match.context, match.replacements[0] if match.replacements else '') for match in matches]
        return corrections, len(corrections)  # Return corrections and count
