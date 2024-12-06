from hashlib import md5
import re , os
from tqdm import tqdm
from translate import fy




def extract_msgid_msgstr(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    units = []  # 存储所有单元
    current_unit = []  # 当前正在处理的单元
    in_msgid = False  # 标记是否在处理msgid块
    for line in lines:

        line = line.strip()  # 去除每行的前后空格

        # 如果是msgid行，开始新的单元
        if line.startswith('msgid'):
            if current_unit:  # 如果当前有正在处理的单元，保存它
                units.append(current_unit)
            current_unit = [line]  # 新的msgid行开始一个新的单元
            in_msgid = True

        # 如果当前处于msgid块内，且未遇到msgstr
        elif in_msgid:
            if line.startswith('msgstr'):
                # 遇到msgstr行，结束当前单元并不包含msgstr行
                units.append(current_unit)
                current_unit = []  # 重置当前单元
                in_msgid = False
            else:
                # 继续添加当前msgid单元的内容
                current_unit.append(line)

    # 处理文件结束后的最后一个单元（如果有）
    if current_unit:
        units.append(current_unit)

    return units


def extract_strings_from_lines(units):
    # 提取每个单元中每一行的双引号内容
    extracted_strings = []
    for unit in units:
        unit_strings = []
        for line in unit:
            # 使用正则表达式提取双引号中的内容
            matches = re.findall(r'"(.*?)"', line)
            unit_strings.extend(matches)  # 将所有匹配的字符串添加到该单元的列表中
        extracted_strings.append(unit_strings)
    return extracted_strings


def replace_msgstr_content(file_path, output_file_path,units,to_lang):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()  # 读取文件的所有行

    modified_lines = []  # 用于存储修改后的行
    i = 0
    for line in tqdm(lines, desc="Processing"):
        line = line.strip()  # 去掉前后空格

        if line.startswith('msgstr'):

            # 找到以msgstr开头的行
            parts = line.split(' ', 1)  # 将msgstr和后面的内容分开
            if len(parts) > 1:
                # 如果有内容在msgstr后面，替换掉
                for idx, unit_strings in enumerate(units[i]):
                    if idx == 0:
                        translation = fy(units[i][0])
                        print("翻译",units[i][0],translation)
                        result = re.sub(r'\* \*', '**', translation)
                        new_line = parts[0] + ' ' + '"' + result + '"'
                    else:
                        translation = fy(unit_strings)
                        print(unit_strings,translation)
                        result = re.sub(r'\* \*', '**', translation)
                        new_line = new_line + "\n"+ '"' + result + '"'
            modified_lines.append(new_line)
            i+=1
        else:
            # 其他行保持不变
            modified_lines.append(line)

    # 保存修改后的文件
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.writelines([line + '\n' for line in modified_lines])

    print(f"文件已保存为 {output_file_path}")

def _translation_api(input_path, output_path, to_lang):
    file_path = input_path  # 替换为你的文件路径
    msgid_msgstr_units = extract_msgid_msgstr(file_path)

    # 提取每个单元中的双引号内容
    extracted_strings = extract_strings_from_lines(msgid_msgstr_units)

    # 打印提取到的双引号中的内容
    for i, unit_strings in enumerate(extracted_strings):
        print(f"Unit {i + 1}:")
        for string in unit_strings:
            print(f"{string}")
        print('-' * 50)

    # 调用函数
    replace_msgstr_content(file_path,output_path,extracted_strings,to_lang)




# 调用翻译方法
_translation_api('test\_inventory_and_mrp.po', '_inventory_and_mrp.th.po', 'th')







