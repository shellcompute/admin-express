import re
import time
from markupsafe import Markup
"""
公用方法
"""


def has_chinese(i_str):
    """
    字符串是否包含中文
    :param i_str: 需要检查的字符串
    :return bool
    """
    for c in i_str:
        if u'\u4e00' <= c <= u'\u9fff':
            return True

    return False


def replace_special_chars(ori_str):
    """去除特殊字符"""
    if ori_str is not None and type(ori_str) is str:
        ori_str = ori_str.replace('/', '').replace('\\', '').replace('?', '').replace('[', '').replace(']', '')
        ori_str = ori_str.replace('*', '').replace(':', '').replace("<u>", "").replace("</u>", "")

        ori_str = "".join(ori_str.split())
        return ori_str

    return ori_str


def is_1st_char_alphanumeric(code_text):
    """判断首字符是否为字母或数字"""
    is_alphanumeric = False
    if code_text is not None and code_text[0:1].isalnum():
        pattern = re.compile(u'[\u4e00-\u9fa5]+')
        result = pattern.match(code_text[0:1])
        if not result:
            is_alphanumeric = True
    return is_alphanumeric


def replace_blank(ori_string, old_char=" ", new_char=""):
    """全量替换空格，默认删除空格，也可将空格替换为指定字符"""
    return str(ori_string).replace(old_char, new_char)


def trim_blank(ori_string):
    """首尾去空格"""
    if ori_string is not None:
        return str(ori_string).strip(" ")
    else:
        return None


def trim_null_line(ori_string):
    """去除空行"""
    if ori_string is not None:
        """去除连续的换行"""
        new_str = re.sub('([ ]*[\n][ ]*)+', '\n', ori_string)
        """去除开头和结尾的换行"""
        return new_str.strip('\n')
    else:
        return None


def is_empty(input_str):
    """字符串是否为空"""
    return input_str is None or input_str == ''


def is_blank(input_str):
    """字符串是否为空或空格"""
    return input_str is None or (type(input_str) is str and len(input_str.strip()) == 0)


def num_to_str(num_str):
    """
    检测 float 格式的整数，转换为 int 格式，然后继续转换为str并返回
    excel 中的数值，默认保存为 float，但实际需要的应该是 int"""
    if type(num_str) is str:
        return num_str
    elif type(num_str) is float and num_str.is_integer():
        return str(int(num_str))
    else:
        return str(num_str)


def get_hyper_link(target_sheet_name, target_cell="A1", show_text="转到"):
    """获取Excel文件内部超链接字符串"""
    return '=HYPERLINK("#\'' + target_sheet_name + '\'!' + target_cell + '", "' + show_text + '")'


def get_outer_hyper_link(outer_file_name, target_sheet_name, target_cell="A1", show_text="转到"):
    """获取外部文件超链接字符串"""
    return '=HYPERLINK("' + outer_file_name + '#\'' + target_sheet_name + '\'!' + target_cell + '", "' + show_text + '")'


def get_replaced_new_str(origin):
    if origin is None or len(origin) == 0:
        return None
    datetime_str = time.strftime("%Y%m%d%H%M%S", time.localtime())
    date_str = time.strftime("%Y%m%d", time.localtime())
    new_str = origin.replace('{$date}', date_str).replace('{$datetime}', datetime_str)
    return new_str


def url_formatter(view, context, model, name):
    """
    设置 字段格式 为 url链接
    callback function for BaseModelView objects
    :param view: current administrative view
    :param context: instance of jinja2.runtime.Context
    :param model: model instance
    :param name: property name of the model
    :return:
    """
    if hasattr(model, name) and getattr(model, name):
        val = getattr(model, name)
        url_string = "<a href='%s' target='_blank'>%s</a>" % (val, val)
        return Markup(url_string)
    else:
        return None


if __name__ == '__main__':
    # print(get_hyper_link("sheet1"))
    # print(get_outer_hyper_link("e:\\tmp\\outa.xlsx", "sheet1"))
    # print(get_replaced_new_str("hehe_{$datetime}_aa_{$date}.abc"))
    assert not has_chinese('Lily'), '不含中文'
    assert has_chinese('刘亦菲'), '含中文'
