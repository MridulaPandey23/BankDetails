from services.authService import (register_user,set_password,login_user)

async def register_user_controller(data, db):
    return await register_user(name=data.name,email=data.email,db=db)
                               
async def set_password_controller(data, db):
    return await set_password(token=data.token,new_password=data.password,db=db)
 
async def login_controller(data, db):
    return await login_user(email=data.email,password=data.password,db=db)
