# Enterprise MEAL Known Issues

## Bootstrap-only shell

The current shell renders placeholder module pages. Domain models, workflow processes, imports, Microsoft sign-in, and dashboards are not implemented yet.

## Local auth only

The first slice intentionally uses Django local authentication. Microsoft Entra OIDC mapping is a planned slice after CRDB confirms app registration and group/role mapping.

## Form runtime not implemented

The repository records the XLSForm/XForm boundary, but pyxform conversion and web runtime rendering are not implemented yet.
