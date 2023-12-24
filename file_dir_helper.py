import os
import re
import shutil


# 传入一个文件的绝对路径，返回文件名，文件名带文件格式后缀
def get_filename_with_suffix_in_filepath(filepath):
    return os.path.basename(filepath)

# 传入一个文件的绝对路径，返回文件名，文件名不带文件格式后缀
def get_filename_without_suffix_in_filepath(filepath):
    return os.path.splitext(os.path.basename(filepath))[0]

# 传入一个文件名，提取出其中的后缀
def get_file_suffix(filename):
    _, file_extension = os.path.splitext(filename)
    return file_extension

# 传入一个文件的绝对路径，提取出除了文件名的后缀，最后以“/”结束
def get_file_path(filename):
    file_path, _ = os.path.split(filename)
    return file_path + "/"

# 根据文件后缀在特定的目录内查找文件，返回一个路径的字典
# 返回的字典是一个后缀对应一个list，list内存放了其所有的文件路径
def find_files_by_extension(directory, extensions):
    if isinstance(directory, str):
        directory = [directory]
    if isinstance(extensions, str):
        extensions = [extensions]

    result_files = {ext: [] for ext in extensions}
    for dir in directory:
        for root, dirs, files in os.walk(dir):
            for file in files:
                for ext in extensions:
                    if file.endswith(ext):
                        result_files[ext].append(os.path.join(root, file))
    return result_files

# 递归搜索图片文件
def find_image_files(directory):
    image_files = []
    file_dict = find_files_by_extension(directory,[".png",".jpg",".bmp"])
    for extension in file_dict:
        image_files.extend(file_dict[extension])
    return image_files

# 递归搜索markdown文件
def find_markdown_files(directory):
    return find_files_by_extension(directory, ".md")[".md"]

# 把一个md文件中的wiki格式的图片引用转换为"assets/文件名/图片名"这样的格式
def convert_md_all_reference_link_format(filepath):
    filename = get_filename_without_suffix_in_filepath(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        matches = re.findall(r"\[\[([^\]]+)\]\]", content)
        for m in matches:
            new_path = f"[{m}](assets/{filename}/{m})"
            content = content.replace(f"[[{m}]]", new_path)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# usage:
# convert_md_reference_link_format("D:\\WorkSpace\\pythonProject1\\markdown处理\\ModBus.md",[".png"])
def convert_md_reference_link_format(filepath, image_formats):
    filename = get_filename_without_suffix_in_filepath(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        matches = re.findall(r"\[\[([^\]]+)\]\]", content)
        for m in matches:
            new_path = f"[{m}](assets/{filename}/{m})"
            if image_formats:
                for format_suffix in image_formats:
                    if get_file_suffix(m) == format_suffix:
                        content = content.replace(f"[[{m}]]", new_path)
                        break

    with open(filename+".md", 'w', encoding='utf-8') as f:
        f.write(content)

# 传入一个文件列表，列表内需要存文件的绝对路径
# 返回一个由文件的绝对路径作为key，引用列表作为value的dict
# 仅查找![[]]这种格式的引用
# usage:
# ret = collect_reference_links(["D:\\WorkSpace\\pythonProject1\\markdown处理\\ModBus.md","D:\\WorkSpace\\pythonProject1\\markdown处理\\数据结构与算法笔记.md"],[".png",".jpg",".bmp",".gif"])
# for (k,v) in ret.items():
#     print(f"file name:{k}\nimage:{v}")
def collect_reference_links(file_list, image_formats):
    reference_dict = {}
    if file_list:
        for file_path in file_list:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                matches = re.findall(r"\!\[\[([^\]]+)\]\]", content)
                for m in matches:
                    if image_formats:
                        for format_suffix in image_formats:
                            if get_file_suffix(m) == format_suffix:
                                reference_dict[file_path] = matches
                                break
    return reference_dict

# 根据文件名在目录中查找文件并拷贝
def find_and_copy_file(source_directory, target_directory, file_names):
    # 如果目标文件夹不存在，则创建
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    print(source_directory)
    print(target_directory)
    print(file_names)

    for file_name in file_names:
        source_file_path = os.path.join(source_directory, file_name)
        destination_file_path = os.path.join(target_directory, file_name)
        if os.path.isfile(source_file_path):
            shutil.copy2(source_file_path, destination_file_path)
            print(f"已拷贝文件: {file_name} 到 {target_directory}")
        else:
            print(f"未找到文件: {file_name} 在 {source_directory}")

# image_path是所有图片原本的目录，是绝对路径
# note_paths是md笔记的路径
# image_formats是一个存放要修改图片的后缀的列表
def classify_and_process_files(image_path,note_path,image_formats):
    # 先处理图片
    md_files = find_markdown_files(note_path)
    for file in md_files:
        convert_md_all_reference_link_format(file)

    dict = collect_reference_links(md_files,image_formats)
    for (k,v) in dict.items():
        md_path = get_file_path(k)
        md_name =get_filename_without_suffix_in_filepath(k)
        path = f"{md_path}assets/{md_name}/"
        if not os.path.exists(path):
            os.makedirs(path)
        find_and_copy_file(image_path,path,v)

classify_and_process_files("D:\\WorkSpace\\pythonProject1\\markdown处理\\notes2\\resources","D:\\WorkSpace\\pythonProject1\\markdown处理\\notes2",[".png",".jpg","bmp","gif"])