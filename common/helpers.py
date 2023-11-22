from apps.role.models import AccessRole


def module_perm(name, user, perm):
    user_access = AccessRole.objects.filter(id=user.role_id)
    if not user_access:
        return False
    user_access = user_access.first()
    role_permissions = user_access.role_permissions
    module_permissions = [
        permission.split(":")[1]
        for permission in role_permissions
        if permission.startswith(f"{name.title()}:")
    ]
    if f"{perm}" in module_permissions:
        return True
    return False


SS_MODULE_PERMISSIONS = [
    {
        "module": "User",
        "permissions": [
            ("view", "Users View"),
            ("add", "Users Add"),
            ("update", "Users Update"),
            ("delete", "Users Delete"),
        ],
    },
    {
        "module": "Invitation",
        "permissions": [
            ("view", "Invitations View"),
            ("add", "Invitations Add"),
            ("update", "Invitations Update"),
            ("delete", "Invitations Delete"),
            ("regenerate", "Invitations Regenerate"),
        ],
    },
    {
        "module": "Role",
        "permissions": [
            ("view", "Roles View"),
            ("add", "Roles Add"),
            ("update", "Roles Update"),
            ("delete", "Roles Delete"),
        ],
    },
    {
        "module": "Company",
        "permissions": [
            ("view", "Companies View"),
            ("add", "Companies Add"),
            ("update", "Companies Update"),
            ("delete", "Companies Delete"),
            ("regenerate", "Invitations Regenerate"),
        ],
    },
]

COM_MODULE_PERMISSIONS = [
    {
        "module": "User",
        "permissions": [
            ("view", "Users View"),
            ("add", "Users Add"),
            ("update", "Users Update"),
            ("delete", "Users Delete"),
        ],
    },
    {
        "module": "Invitation",
        "permissions": [
            ("view", "Invitations View"),
            ("add", "Invitations Add"),
            ("update", "Invitations Update"),
            ("delete", "Invitations Delete"),
            ("regenerate", "Invitations Regenerate"),
        ],
    },
    {
        "module": "Role",
        "permissions": [
            ("view", "Roles View"),
            ("add", "Roles Add"),
            ("update", "Roles Update"),
            ("delete", "Roles Delete"),
        ],
    },
    {
        "module": "Client",
        "permissions": [
            ("view", "Clients View"),
            ("add", "Clients Add"),
            ("update", "Clients Update"),
            ("delete", "Clients Delete"),
        ],
    },
]

ss_available_role_permissions = [
    "User:view",
    "User:add",
    "User:update",
    "User:delete",
    "Invitation:view",
    "Invitation:add",
    "Invitation:update",
    "Invitation:delete",
    "Invitation:regenerate",
    "Role:view",
    "Role:add",
    "Role:update",
    "Role:delete",
    "Company:view",
    "Company:add",
    "Company:update",
    "Company:delete",
    "Company:regenerate",
]

com_available_role_permissions = [
    "User:view",
    "User:add",
    "User:update",
    "User:delete",
    "Invitation:view",
    "Invitation:add",
    "Invitation:update",
    "Invitation:delete",
    "Invitation:regenerate",
    "Role:view",
    "Role:add",
    "Role:update",
    "Role:delete",
    "Client:view",
    "Client:add",
    "Client:update",
    "Client:delete",
]
