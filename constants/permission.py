from enums import ActionEnum, ResourceEnum, RoleEnum

ROLE_PERMISSIONS = {
    RoleEnum.ADMIN: {
        ResourceEnum.USER: list(ActionEnum),
        ResourceEnum.PERMISSION: list(ActionEnum),
    },
    RoleEnum.SUPPORT: {
        ResourceEnum.USER: [ActionEnum.READ, ActionEnum.UPDATE, ActionEnum.DELETE],
        ResourceEnum.PERMISSION: [ActionEnum.READ],
    },
    RoleEnum.USER: {
        ResourceEnum.USER: [ActionEnum.READ, ActionEnum.UPDATE, ActionEnum.DELETE],
        ResourceEnum.PERMISSION: [ActionEnum.READ],
    },
}
