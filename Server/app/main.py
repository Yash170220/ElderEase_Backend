
from fastapi import FastAPI # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from app.routes import router

app = FastAPI(
    title="Elder Ease",
    description="Recommends Medicare and Subsidy Schemes for elderly users in the U.S.",
    version="0.1.0"
)

# Enable CORS (you can restrict origins in production)
app.add_middleware(
    CORSMiddleware,
   # allow_origins=["*"],  # Replace with frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)
