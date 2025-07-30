# Models
from .models import Menu
from .utils import get_user_menu


def menu(request):
    return {"menu_tree": build_user_menu(request.user)}


def build_user_menu(user):
    if not user.is_authenticated or not user.is_active:
        return []

    user_perms = set(user.get_all_permissions())
    object_list = (
        Menu.objects.filter(parent__isnull=True, is_active=True)
        .select_related("action", "parent")
        .prefetch_related(
            "submenus",
            "submenus__action",
            "submenus__parent",
            "submenus__submenus",
            "submenus__submenus__action",
            "submenus__submenus__parent",
            "submenus__submenus__submenus",
            "submenus__submenus__submenus__action",
            "submenus__submenus__submenus__parent",
            "submenus__submenus__submenus__submenus",
            "submenus__submenus__submenus__submenus__action",
            "submenus__submenus__submenus__submenus__parent",
            "submenus__submenus__submenus__submenus__submenus",
            "submenus__submenus__submenus__submenus__submenus__action",
            "submenus__submenus__submenus__submenus__submenus__parent",
        )
    )
    return get_user_menu(object_list, user, user_perms)


