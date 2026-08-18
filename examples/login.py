"""Examples of logging in to NicoNico."""

from niconico import NicoNico

client = NicoNico()

# Reuse the session of a browser you are already signed in with.
# Requires the browser extra: pip install "niconico.py[browser]"
client.login_with_browser_cookies()

# A specific browser can be named when several are installed.
client.login_with_browser_cookies("firefox")

# If you already have a session token, use it directly.
client.login_with_session("user_session_~~~~")

print(client.get_user_session())
