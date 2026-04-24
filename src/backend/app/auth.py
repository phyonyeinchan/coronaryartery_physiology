from fastapi import Depends, HTTPException, status

# Placeholder auth dependency for RBAC integration later
def get_current_user():
    user = {"username": "dev", "roles": ["clinician"]}
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user
