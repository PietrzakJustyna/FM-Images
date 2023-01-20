from images.views import ImageViewset
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register("images", ImageViewset)
urlpatterns = router.urls
