"""
BIPS CLI Entrypoint
"""

from ps_cli.controllers import (
    AddressGroup,
    Asset,
    Database,
    Entitlement,
    EntityType,
    Folder,
    ISARequest,
    ManagedAccount,
    ManagedSystem,
    Organization,
    Platform,
    Request,
    Safe,
    Secret,
    Settings,
    User,
    Usergroups,
    Workgroup,
)
from ps_cli.core.app import App


def main() -> None:
    controllers = [
        AddressGroup,
        Safe,
        Folder,
        Secret,
        ManagedAccount,
        ManagedSystem,
        Workgroup,
        User,
        Usergroups,
        Database,
        Organization,
        Settings,
        Asset,
        Entitlement,
        EntityType,
        ISARequest,
        Platform,
        Request,
    ]

    app = App(controllers=controllers)
    app.run()


if __name__ == "__main__":
    main()
