# routers/stress.py
from fastapi import APIRouter, Depends
import time
from routers.auth import get_current_user
import models

router = APIRouter(prefix="/stress", tags=["stress"])

@router.get("/cpu")
def stress_cpu(
    seconds: int = 30,
    current_user: models.User = Depends(get_current_user),
):
    """
    Intentionally burn CPU for `seconds`.
    Use this to test autoscaling based on CPU utilization.
    """
    end = time.time() + seconds
    while time.time() < end:
        # Busy loop to keep CPU hot
        _ = 10**5 * 10**5
    return {"message": f"CPU stressed for {seconds} seconds"}

@router.get("/memory")
def stress_memory(
    mb: int = 500,
    current_user: models.User = Depends(get_current_user),
):
    """
    Intentionally allocate `mb` MB of RAM for 30 seconds.
    Use this to test autoscaling based on memory utilization.
    """
    data = ['X' * 1024 * 1024] * mb  # allocate MBs
    time.sleep(30)
    # Let data go out of scope after return
    return {"message": f"Allocated {mb} MB for 30 seconds"}
