from unittest import TestCase

from utils.pagination import make_pagination_range


class TestPagination(TestCase):
    def test_pagination_is_changing_dinamically(self):
        current_page = 6
        display_pages = 5
        pag_list = make_pagination_range(total_pages=60, display_pages=display_pages, current_page=current_page)
        if current_page > 1:
            if display_pages % 2 == 0:
                self.assertEqual(pag_list['range'][1], current_page)
            else:
                self.assertEqual(pag_list['range'][2], current_page)
        else:
            self.assertEqual(pag_list['range'][0], current_page)