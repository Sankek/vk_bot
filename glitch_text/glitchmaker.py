import pandas as pd
import numpy as np
import os


class Glitcher:
    """
    Adds glitches (HTML combining letters) to text.
    """
    
    def __init__(self, glitch_size=10):
        path = os.path.join(os.path.dirname(__file__), 'letter_html_codes.csv')
        df = pd.read_csv(path)
        
        self.combining_codes = df[df['name'].str.startswith('Combining')]['code'].values 
        self.glitch_size = glitch_size

        
    def append_combining_codes(self, symbol):
        return symbol + ''.join(np.random.choice(self.combining_codes, size=self.glitch_size))


    def glitch(self, text):
        new_text = ''.join([self.append_combining_codes(symbol) for symbol in text])
        return new_text
