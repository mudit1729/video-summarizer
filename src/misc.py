import random

class Misc:
    @staticmethod
    def loaderx():
        n = random.randint(0, 3)  # Changed to 0-3 to match the number of loader messages
        loader = [
            "🔄 Loading... Hold on tight!",
            "⏳ AI is brewing your content potion...",
            "🌟 The AI is working its magic...",
            "🤖 Processing your request... AI at work!"
        ]
        return n, loader