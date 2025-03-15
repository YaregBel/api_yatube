from rest_framework import permissions

# Класс реализующий права доступа для выполнения запроса
class OwnershipPermission(permissions.BasePermission):
    
    # Метод, проверяющий, имеет ли пользователь право для выполнения запроса к представлению view
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )
    # Метод проверяющий, имеет ли пользователь право выполнять действие над конкретным объектом. 
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
