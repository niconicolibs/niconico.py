"""Examples of logging in to NicoNico."""

from niconico import NicoNico

client = NicoNico()

# Sign in interactively. The login page opens in a browser; fill in the form,
# solve the bot challenge and submit it, and the session is picked up for you.
# Requires the browser extra: pip install "niconico.py[browser]"
client.login_with_browser()

# The mail and password can be prefilled, but you still submit the form yourself.
client.login_with_browser("mail@example.com", "password")

# Reusing a profile directory keeps you signed in between runs, and launching an
# installed browser instead of the bundled Chromium helps with the bot challenge.
client.login_with_browser(user_data_dir="./.niconico-profile", channel="chrome")

# If you already have a session token, use it directly.
client.login_with_session("user_session_~~~~")

print(client.get_user_session())
