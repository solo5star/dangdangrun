import uvicorn
from dangdangrun import settings

uvicorn.run(
    "dangdangrun.server:app",
    host="0.0.0.0",
    port=3355,
    reload=settings.DEBUG,
    debug=settings.DEBUG,
)
