from aiohttp import web
from user_db import add_user_to_db, get_user_from_db, delete_user_from_db
from hashlib import sha256

async def get_user(request):
    user = request.query.get('user')
    user_data = await get_user_from_db(user=user)
    return web.json_response({'user_data': user_data})


async def add_user(request):
    data = await request.json()
    user = data.get('user').lower()
    password = data.get('password')

    if not all([user, password]):
        return web.json_response({'msg': 'Не вистачає інформації.'}, status=400)

    await add_user_to_db(
        user=user,
        password=sha256(password.encode()).hexdigest()
    )
    return web.json_response({'msg': 'Книгу додано.'})


async def delete_user(request):
    data = await request.json()
    user = data.get('user').lower()
    password = data.get('password')

    if not all([user, password]):
        return web.json_response({'msg': 'Не вистачає інформації.'}, status=400)

    is_deleted = await delete_user_from_db(
        user=user,
        password=sha256(password.encode()).hexdigest()
    )
    if is_deleted[0] is False:
        return web.json_response({'msg': is_deleted[1]}, status=400)
    return web.json_response({'msg': is_deleted[1]})


def main():
    app = web.Application()
    app.router.add_get(path="/user/get", handler=get_user)
    app.router.add_post(path='/user/add', handler=add_user)
    app.router.add_delete(path="/user/delete", handler=delete_user)

    return app

if __name__ == '__main__':
    app = main()
    web.run_app(app=app, host='0.0.0.0', port=80)
