from math import floor

from django.core.paginator import Paginator


def make_pagination_range(
    total_pages,
    display_pages,
    current_page,
):
    total_range = list(range(1, total_pages + 1))
    middle_range = floor(display_pages / 2)
    if (current_page - middle_range >= 0): 
        if (display_pages % 2 == 0):
            return_page = total_range[(current_page - middle_range):(current_page + middle_range)]
        else:
            return_page = total_range[(current_page - 1 - middle_range):(current_page + middle_range)]
        if current_page - 1 - middle_range <= 0:
            return_page = total_range[0:display_pages]
    else:
        return_page = total_range[0:display_pages]

    return {
        'range': return_page,
        'first_out_of_range': current_page - middle_range > 0 if (display_pages % 2 == 0) else current_page - 1 - middle_range > 0, 
        'last_out_of_range': current_page + middle_range < len(total_range),
        'last_page': total_pages,
        'selected_page': current_page,
    }

def make_pagination(request, queryset, per_paginator, per_page = 6):
    page_number = request.GET.get('page', 1)

    paginator = Paginator(object_list=queryset, per_page=per_page)
    page_obj = paginator.get_page(page_number)
    pages = make_pagination_range(
        total_pages=int(paginator.num_pages),
        display_pages=per_paginator,
        current_page=int(page_number)
    )

    return pages, page_obj

def make_many_pagination(*querysets_with_names, request, per_paginator, per_page=9):
    page_numbers = {}
    paginators = {}
    pages_obj = {}  # Return
    pages = {}  # Return

    for id, (queryset_name, queryset) in enumerate(querysets_with_names):
        page_number = request.GET.get(f'page{queryset_name}', 1) 
        page_numbers[f'page{queryset_name}'] = page_number

        paginator = Paginator(object_list=queryset, per_page=per_page)
        paginators[f'paginator{queryset_name}'] = paginator

        page_obj = paginator.get_page(page_number)
        pages_obj[f'page_obj{queryset_name}'] = page_obj

        page = make_pagination_range(
            total_pages=int(paginator.num_pages),
            display_pages=per_paginator,
            current_page=int(page_number)
        )
        pages[f'page{queryset_name}'] = page

    return {'pages': pages, 'pages_obj': pages_obj, 'page_numbers': page_numbers}
    