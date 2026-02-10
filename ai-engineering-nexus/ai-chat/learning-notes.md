In your current models.py, you probably have os.getenv('GOOGLE_API_KEY'). If you misspell that key in your .env file, os.getenv just returns None, and your app crashes only when someone tries to chat.

With Pydantic, the app won't even start if a required variable is missing. It acts as a "Gatekeeper."