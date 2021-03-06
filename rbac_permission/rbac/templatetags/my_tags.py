from django import template
register = template.Library()


@register.inclusion_tag("menu_permission.html")
def menu_permission(request):
    menu_permission_list = request.session["menu_permission_list"]
    print("----------", menu_permission_list)
    return {"menu_permission_list": menu_permission_list}
