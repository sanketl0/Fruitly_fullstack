

# import os
# import sys
# from pathlib import Path
# from django.core.wsgi import get_wsgi_application

# os.environ['LIFECYCLE'] = 'LIVE'

# path_home = str(Path(__file__).parents[1])
# if path_home not in sys.path:
#     sys.path.append(str(path_home))

# from django.core.wsgi import get_wsgi_application

# # os.environ['DJANGO_SETTINGS_MODULE'] = 'CodeRizeBanking.settings'
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CodeRizeBanking.settings')

# application = get_wsgi_application()


import os
import sys
from pathlib import Path
from django.core.wsgi import get_wsgi_application

os.environ['LIFECYCLE'] = 'LIVE'

path_home = str(Path(__file__).parents[1])
if path_home not in sys.path:
    sys.path.append(path_home)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CodeRizeBanking.settings')

application = get_wsgi_application()
