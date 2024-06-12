import math
import traceback
from django.db.models import QuerySet
from typing_extensions import Dict


def pagination_utility(total_entries: QuerySet, page: int, items: int) -> Dict:
    """
    Custom pagination utility function.

    Args:
        total_entries (QuerySet): QuerySet containing total entries.
        page (int): Current page number.
        items (int): Number of items per page.

    Returns:
        dict: Paginated data along with page details.
    """
    try:
        total_entries_count = total_entries.count()
        total_pages = math.ceil(total_entries_count / items)

        return {
            "next_page": page + 1 if total_pages != page else None,
            "previous_page": page - 1 if page != 1 else 0,
            "total_pages": total_pages,
            "items": items,
            "total_entries": total_entries_count,
        }
    except Exception as e:
        print(e, traceback.format_exc())
