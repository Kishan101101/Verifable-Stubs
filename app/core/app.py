"""FastAPI application factory"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import get_config
from app.core.database import init_db
from app.logging_config import configure_logging
from app.routes.academic_router import router as academic_router
from app.routes.doctor_router import router as doctor_router
from app.routes.insurance_router import router as insurance_router

def create_app(env: str = "development") -> FastAPI:
    """Create and configure FastAPI application"""
    
    # Configure logging
    configure_logging()
    
    # Get configuration
    settings = get_config(env)
    
    # Initialize database
    init_db()
    
    # Create FastAPI app with lifespan context
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Startup
        print("Application startup")
        yield
        # Shutdown
        print("Application shutdown")
    
    app = FastAPI(
        title=settings.API_TITLE,
        version=settings.API_VERSION,
        description="FastAPI for doctor onboarding, academic admission, and insurance claim flows.",
        lifespan=lifespan
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(academic_router, prefix="/api/v1/academic", tags=["Academic"])
    app.include_router(doctor_router, prefix="/api/v1/doctors", tags=["Doctor"])
    app.include_router(insurance_router, prefix="/api/v1/insurance", tags=["Insurance"])
    
    # Health check endpoint
    @app.get("/api/v1/health", tags=["Health"])
    async def health_check():
        """Health check endpoint"""
        return {
            "status": "healthy",
            "message": "Verifiable Stubs API is running"
        }
    
    # Favicon endpoint (suppress 404)
    @app.get("/favicon.ico", include_in_schema=False)
    async def favicon():
        """Return empty response for favicon requests"""
        return "", 204
    
    return app
