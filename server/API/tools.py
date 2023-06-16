# import urllib.parse as urlparse
# from urllib.parse import urlencode
#
#
# def process_redirect_url(redirect_url: str, new_entries: dict) -> str:
#     # Prepare the redirect URL
#     url_parts = list(urlparse.urlparse(redirect_url))
#     queries = dict(urlparse.parse_qsl(url_parts[4]))
#     queries.update(new_entries)
#     url_parts[4] = urlencode(queries)
#     url = urlparse.urlunparse(url_parts)
#     return url
