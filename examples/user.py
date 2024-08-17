"""Example of getting user information."""

from niconico import NicoNico

client = NicoNico()

user = client.user.get_user("2")

if user is None:
    print("User not found.")
else:
    print(user.nickname)
    print(user.description)
