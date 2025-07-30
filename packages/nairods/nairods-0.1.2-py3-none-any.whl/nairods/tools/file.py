# 文件名：file.py
# 作者：nairoads
# 日期：2025-06-18 15:22:37
# 描述：文件与文件夹、Excel、PDF、YML、压缩包、临时文件等操作工具

import os
import zipfile
import pandas as pd
import xlwt
import yaml
import fitz
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup

# ================= 文件夹操作 =================
class FolderUtils:
    """
    文件夹操作工具
    """
    @staticmethod
    def create_folder(folder_path: str) -> str:
        """
        文件夹不存在则创建
        :param folder_path: 文件夹地址
        :return: 创建成功
        """
        if not os.path.exists(folder_path):
            try:
                os.makedirs(folder_path)
                return "创建成功"
            except OSError as exc:
                raise exc
        return "已存在"

    @staticmethod
    def walk_folder_path(destination_folder: str) -> Dict[str, List[str]]:
        """
        遍历目标文件夹下的所有文件
        :param destination_folder:  目标文件夹
        :return: 文件列表
        """
        result = {}
        for root, dirs, files in os.walk(destination_folder):
            files_list = [os.path.join(root, file) for file in files]
            if files_list:
                result[root] = files_list
        return result

    @staticmethod
    def save_latest_files(folder_path: str) -> str:
        """
        保留文件夹下最新的文件
        :param folder_path:  目标文件夹
        :return: F'已保留最新文件'
        """
        files_list = [(f, os.path.getmtime(os.path.join(folder_path, f))) for f in os.listdir(folder_path)]
        sorted_files = sorted(files_list, key=lambda x: x[1])
        for file, _ in sorted_files[:-1]:
            os.remove(os.path.join(folder_path, file))
        return '已保留最新文件'

# ================= Excel 操作 =================
class ExcelUtils:
    """
    Excel 文件操作工具
    """
    def __init__(self, excel_path: str = ""):
        self.excel_path = excel_path

    def read_excel(self) -> Any:
        """
        读取 Excel 文件
        :return: 全部数据，为 numpy 数组
        """
        result = pd.read_excel(self.excel_path, header=0, keep_default_na=False).values
        return result

    @staticmethod
    def save_list_to_excel(title: List[str], result_li: List[List[Any]], save_name: str, sheet: str = "sheet1") -> str:
        """
        列表保存到表格
        :param title: 表头
        :param result_li: 数据列表
        :param save_name: 保存的文件名称
        :param sheet: 表格的第一个窗口名
        :return: 保存的文件名称
        """
        book = xlwt.Workbook()
        sheet_obj = book.add_sheet(sheet)
        for i, t in enumerate(title):
            sheet_obj.write(0, i, t)
        for i, d in enumerate(result_li):
            for j, one in enumerate(d):
                sheet_obj.write(i + 1, j, one)
        book.save(f"{save_name}.xls")
        return save_name

# ================= PDF 操作 =================
class PdfUtils:
    """
    PDF 文件操作工具
    """
    @staticmethod
    def pdf_to_images(pdf_path: str, pic_path: str) -> None:
        """
        PDF 转化为图片
        :param pdf_path: PDF 文件路径
        :param pic_path: 图片保存路径
        """
        pdf_doc = fitz.open(pdf_path)
        for pg in range(pdf_doc.page_count):
            page = pdf_doc[pg]
            mat = fitz.Matrix(1.33333333, 1.33333333).prerotate(0)
            pix = page.get_pixmap(matrix=mat, alpha=False)
            if not os.path.exists(pic_path):
                os.makedirs(pic_path)
            img_name = f"{os.path.splitext(os.path.basename(pdf_path))[0]}_{pg}.png"
            pix.save(os.path.join(pic_path, img_name))

# ================= YML 操作 =================
class YamlUtils:
    """
    YAML 文件操作工具
    """
    def __init__(self, yml_path: str = ""):
        self.yml_path = yml_path

    def read_yaml(self) -> Any:
        """
        读取 YAML 文件
        :return: 全部数据，为字典
        """
        with open(self.yml_path, 'r', encoding='utf-8') as f:
            result = yaml.safe_load(f)
        return result

# ================= ZIP 操作 =================
class ZipUtils:
    """
    ZIP 文件操作工具
    """
    @staticmethod
    def unzip_file(zip_file: str, save_folder: str) -> str:
        """
        解压文件到指定文件夹
        :param zip_file:  需要解压的文件
        :param save_folder:    保存的本地文件夹
        :return: 保存成功
        """
        FolderUtils.create_folder(save_folder)
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(save_folder)
        return "解压成功"

# ================= 临时文件操作 =================
class TempFileUtils:
    """
    临时文件操作工具
    """
    @staticmethod
    def read_temp(tmp_file: str) -> str:
        """
        读取临时文件内容
        :param tmp_file:  需要读取的临时文件
        :return: 临时文件内容
        """
        with open(tmp_file, "r", encoding="utf-8") as f:
            tmp_content = f.read()
        return tmp_content

    @staticmethod
    def tmp_color_picfh(tmp_file: str, color: str) -> Dict[str, str]:
        """
        解析 tmp 中带颜色的文字和它的前一项
        :param tmp_file:  需要读取的临时文件
        :param color: 颜色代码
        :return: 字典格式 {key:value}
        """
        with open(tmp_file, "r", encoding="utf-8") as f:
            tmp_content = f.read()
        soup = BeautifulSoup(tmp_content, 'html.parser')
        font_elements = soup.find_all('font', {'color': color})
        result_dict = {}
        for font_element in font_elements:
            td_element = font_element.parent
            mess_element = td_element.find_previous_sibling('td', {'id': 'mess'})
            mess_value = mess_element.get_text() if mess_element else ''
            b_value = font_element.get_text()
            result_dict[mess_value] = b_value
        return result_dict

    @staticmethod
    def tmp_blade_df(tmp_file: str) -> pd.DataFrame:
        """
        读取临时文件，清理数据，返回 DataFrame
        :param tmp_file:  需要读取的临时文件
        :return: DataFrame
        """
        with open(tmp_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        lines = lines[3:]
        header = lines.pop(0).strip().lstrip('#').split('; ')
        data = [line.strip().split(';') for line in lines]
        df = pd.DataFrame(data, columns=header)
        return df

__all__ = [
    "FolderUtils", "ExcelUtils", "PdfUtils", "YamlUtils", "ZipUtils", "TempFileUtils"
] 