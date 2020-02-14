

def init_session(request, user):
    # 在session中注册用户 ID
    request.session["user_id"] = user.pk

    # 方法1
    # # 查询当前用户登陆的所有权限  distinct(去重)
    # permission = user.roles.all().values("permissions__url").distinct()
    # permission_list = []
    # for item in permission:
    #     permission_list.append(item["permissions__url"])
    # print(permission_list)
    # request.session["permission_list"] = permission_list

    # 方法2
    permissions = user.roles.all().values("permissions__url", "permissions__action", "permissions__group_id")
    permissions_dict = {}
    for item in permissions:
        group_id = item["permissions__group_id"]
        # 键不在字典里
        if group_id not in permissions_dict:
            permissions_dict[group_id] = {
                "urls": [item["permissions__url"]],
                "actions": [item["permissions__action"]],
            }
        # 键在字典里
        else:
            permissions_dict[group_id]["urls"].append(item["permissions__url"])
            permissions_dict[group_id]["actions"].append(item["permissions__action"])
    print(permissions_dict)
    request.session["permissions_dict"] = permissions_dict

    ret = user.roles.all().values("permissions__url", "permissions__action", "permissions__group__name",)
    print("ret:", ret)
    menu_permission_list = []
    for item in ret:
        if item["permissions__action"] == "list":
            menu_permission_list.append((item["permissions__url"], item["permissions__group__name"]))
    request.session["menu_permission_list"] = menu_permission_list
