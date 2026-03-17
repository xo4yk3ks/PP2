import shutil
import os

# Copy file
shutil.copy("example.txt", "copy_example.txt")

# Delete file
os.remove("copy_example.txt")
