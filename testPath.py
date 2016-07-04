import pathlib

p = "/home/chucxin/programming/rfid_ad/test.py"

print(pathlib.PurePath(p).parents[0].joinpath("userdata.py"))
