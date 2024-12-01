import os

def add_suffix_to_filename(filename, suffix):
    name, ext = os.path.splitext(filename)
    new_filename = f"{name}{suffix}{ext}"
    return new_filename