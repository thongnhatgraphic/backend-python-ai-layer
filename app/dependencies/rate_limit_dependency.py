from fastapi import HTTPException, Depends
from app.core.redis import redis_client
from uuid import UUID
from app.dependencies.auth_dependency import get_current_user




# limit request per user per minute "limit = 100"
def rate_limitter(
    user_id: UUID = Depends(get_current_user)
):
    limit = 2
    key = f"rate_limit:{user_id}"
    number_of_requests = redis_client.incr(key)
    
    print(f"\n number_of_requests {number_of_requests} \n \n \n ")

    if number_of_requests == 1:
        redis_client.expire(key, 60)
        
    if int(number_of_requests) > limit:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded"
        )
    return True
