"""Simple helper to paginate query
"""
from flask import url_for, request

DEFAULT_PAGE_SIZE = 20
DEFAULT_PAGE_NUMBER = 1


def paginate(query, schema, field=None, exclude=[]):
    '''
    Returns the pagination object that include:
    iter_pages, next, prev, has_next, has_prev, next_num, prev_num.
    '''
    if query:
        page = int(request.args.get('page', DEFAULT_PAGE_NUMBER))
        per_page = int(request.args.get('perPage', DEFAULT_PAGE_SIZE))

        all_objects = request.args.get('all', 'no')
        try:
            if all_objects == 'yes':
                if exclude:
                    schema = schema.__class__(
                        many=schema.many, only=schema.only, exclude=exclude)
                    return schema.jsonify(query)
                else:
                    raise AttributeError(
                        'all_objects should only expose limited fields,'
                        'other fields have to be excluded')
        except AttributeError:
            return {'message': 'Invalid argument or not supported'}, 400

        if field:
            paginated_obj = query.paginate_field(
                field, page=page, per_page=per_page)
        else:
            paginated_obj = query.paginate(page=page, per_page=per_page)
        results = schema.dump(paginated_obj.items).data
        return {
            'total': paginated_obj.total,
            'pages': paginated_obj.pages,
            'next': paginated_obj.next_num,
            'prev': paginated_obj.prev_num,
            'results': results
        }
    else:
        return {
            'total': 0,
            'pages': 0,
            'next': 1,
            'prev': 1,
            'results': []
        }
