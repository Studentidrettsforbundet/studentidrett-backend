from rest_framework.permissions import IsAdminUser


class GetInterestPermission(IsAdminUser):
    def has_permission(self, request, view):
        if request.method != "GET":
            return True
        else:
            return super().has_permission(request, view)
