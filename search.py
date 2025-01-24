from pathlib import Path

   
    
def check_string(file_path):
    with open(file_path, encoding="utf-8") as f:
        txt = f.read()
        if "alert" in txt or "ALERT" in txt:
            return True
    return False



folder = r"C:\Users\ME\Desktop\메\Dump"
entries = Path(folder)
for entry in entries.iterdir():
    file_path = folder + "\\" + entry.name
    if Path(file_path).is_file():
        if check_string(file_path):
            print(file_path)


print("byebye")