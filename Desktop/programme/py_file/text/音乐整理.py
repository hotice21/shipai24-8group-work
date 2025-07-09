import os
def tidy_music_files(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path):
            index = filename.find('-')
            print(f"文件名: {filename}，'-' 字符位置: {index if index != -1 else '未找到'}")
            if index != -1:
                folder_name = filename[:index].strip()
                target_folder = os.path.join(folder, folder_name)
                if not os.path.exists(target_folder):
                    os.mkdir(target_folder)
                os.rename(file_path, os.path.join(target_folder, filename))
    print("finish")
def remove_file(folder):
    for filename in os.listdir(folder):
        path_filename=os.path.join(folder,filename)
        if os.path.isdir(path_filename):
            number=len(os.listdir(path_filename))
            if number <=3:
                for name in os.listdir(path_filename):
                    os.rename(os.path.join(folder,filename,name),os.path.join(folder,name))
                os.rmdir(path_filename)
            else:
                print(filename)
    print("finish")

if __name__ == "__main__":
    folder=input("请输入文件夹路径: ")
    tidy_music_files(folder)
    remove_file(folder)