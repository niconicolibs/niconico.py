"""Example of login with mail address, password, and session id."""

from niconico import NicoNico

client = NicoNico()

# 1. login with mail address and password
client.login_with_mail("mail@example.com", "password")

# 2. login with mail address and password, using 2FA
client.login_with_mail("mail@example.com", "password", "1234")

# 3. login with session id (cookie called `user_session` of nicovideo.jp)
client.login_with_session("user_session_~~~~")
