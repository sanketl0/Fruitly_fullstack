# permissions.py

from rest_framework import permissions

from datetime import datetime, timedelta

class IsUseradmin(permissions.BasePermission):
    """
    Allows access only to user1 or admin roles.
    """
    def has_permission(self, request, view):
        user_role = request.user.role
        return user_role == 'admin'

class IsUser1(permissions.BasePermission):
    """
    Allows access only to user1 or admin roles.
    """
    def has_permission(self, request, view):
        user_role = request.user.role
        return user_role == 'user1'


class IsUser2(permissions.BasePermission):
    """
    Allows access only to user2 role.
    """
    def has_permission(self, request, view):
        user_role = request.user.role
        return user_role == 'user2'


class IsUser1OrUser2(permissions.BasePermission):
    """
    Allows access if user is either user1 or user2.
    """
    def has_permission(self, request, view):
        user_role = request.user.role
        return user_role in ['user1', 'user2']
    
class IsUser2OneMonthRange(permissions.BasePermission):
    """
    Ensures user2 can only fetch statements within a one-month range.
    """

    def has_permission(self, request, view):
        if request.user.role != 'user2':
            return True  # Allow other roles unrestricted access
        
        # Extract parameters from view.kwargs (since they are in the URL)
        from_date_str = view.kwargs.get('from_date')
        to_date_str = view.kwargs.get('to_date')

        if not from_date_str or not to_date_str:
            return False  # Missing date values

        try:
            # Convert to date objects
            from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
            to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()

            # Ensure from_date is before or equal to to_date
            if from_date > to_date:
                return False
            
            # Check if the date range exceeds one month
            if (to_date - from_date).days > 31:
                return False

            # Alternative check using month-year comparison
            if from_date.year == to_date.year:
                if to_date.month - from_date.month > 1:
                    return False
            elif to_date.year - from_date.year == 1:
                if (from_date.month == 12 and to_date.month != 1) or (to_date.month - from_date.month != -11):
                    return False
            elif to_date.year - from_date.year > 1:
                return False

        except ValueError:
            return False  # Invalid date format

        return True