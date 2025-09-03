from usecases import PermissionUsecase


def get_permission_usecase() -> PermissionUsecase:
    """Get the permission usecase.

    Returns:
        The permission usecase.

    """
    return PermissionUsecase()
