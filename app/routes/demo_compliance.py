"""
Backward compatibility shim: re-export the router from the
`app.routes.compliance` module so old imports continue to work.

NOTE: Use `app.routes.compliance` in new code.
"""

from app.routes.compliance import router as router

__all__ = ["router"]

