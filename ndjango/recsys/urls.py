from recsys.individual_urls.recsys_1 import urlpatterns as rec1_urls
from recsys.individual_urls.recsys_2 import urlpatterns as rec2_urls
from recsys.individual_urls.recsys_3 import urlpatterns as rec3_urls

app_name = 'recsys'

urlpatterns = sum([rec1_urls, rec2_urls, rec3_urls], [])

