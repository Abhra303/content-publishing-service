# All the internal APIs needed for this service should be
# stored here.

import os


USER_INTERACTION_TOP_CONTENTS_API = os.environ.get('USER_INTERACTION_URL', 'http://localhost:8002/contents/books/top-contents')
