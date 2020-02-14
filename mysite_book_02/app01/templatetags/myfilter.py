from django import template
register = template.Library()


@register.filter(name="sb")
def add_sb(arg):
    return "{}是个大帅比".format(arg)


# 告诉django的模板语言我现在有一个自定义filter方法，名字叫add_str
@register.filter(name="add_str")
def add_str(arg, arg2):
    """
    第一个参数永远是管道符前面的变量
    :param arg: 管道符前面那个变量
    :param arg2: 冒号后面的那个变量
    :return:
    """
    return "{}{}".format(arg, arg2)