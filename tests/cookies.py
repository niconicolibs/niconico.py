
import path_magic
from niconico import Cookies


print(list(Cookies.from_file("cookies.txt").keys()))