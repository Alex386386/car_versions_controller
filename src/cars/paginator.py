from django.core.paginator import Paginator


def run_pagination(list_obj, request, filters):
    """
    Функция Paginator для переработки списка машин
    в объект типа page_object
    """
    paginator = Paginator(list_obj, filters)
    page_number = request.GET.get("page")
    return paginator.get_page(page_number)
