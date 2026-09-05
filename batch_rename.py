from pathlib import Path
import re

def batch_rename(folder: str,old: str,new: str) -> None:
    """
    folder:文件夹路径
    old:  要替换的内容(如"IMG_")
    new:  要替换成什么(如"photo_")
    """

    p = Path(folder)
    for f in p.iterdir():
        if f.is_file():
            new_name = f.name.replace(old,new)
            if new_name != f.name:
                f.rename(p / new_name)
                print(f"{f.name}->{new_name}")
batch_rename(r"C:\Users\zzz\Desktop\test_rename","IMG_","photo_")