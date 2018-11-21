from django.utils.http import urlencode
from django.core.urlresolvers import reverse_lazy

def reverse_with_query(viewname, query_kwargs=None):

    url = reverse_lazy(viewname)
    if query_kwargs:
        msg = urlencode(query_kwargs)
        return "%s?%s"%(url, msg)

    return url