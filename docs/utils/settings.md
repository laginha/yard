# Settings

### JSON_INDENT

Defines the number of spaces for *JSON* response indentation. Although it might be useful for debugging puposes, it is not recommended for production environments.

    JSON_INDENT = 4


### YARD_DEBUG_TOOLBAR

If set to `True`, the resource returns a `JsonDebugResponse` whenever possible, which is useful while in develop mode. (*Django Debug Toolbar* integration).
If set to `False`, the resource returns a `ProperJsonResponse` whenever possible.

    YARD_DEBUG_TOOLBAR = False
