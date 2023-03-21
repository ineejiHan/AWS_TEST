import aiomysql
from fastapi import APIRouter
hmid = APIRouter()

#db = pymysql.connect(host='localhost', port=3306, user='root', passwd='ineeji1234', db='ineeji', charset='utf8')
# async def go():
#     conn = await aiomysql.create_pool(host='127.0.0.1', port=3306,
#                                       user='root', password='ineeji1234',
#                                       db='mysql', autocommit=False)
#     return conn

# 전체 사용자 정보
@hmid.get(path="/getUsers",description="전체사용자정보",tags=["HMID"] )
async def read_users():
    conn = await aiomysql.connect(host='220.94.157.27', port=53307,
                                      user='ineeji', password='ineeji1234',
                                      db='ineeji', autocommit=True)
    async with conn.cursor() as cursor:
        await cursor.execute("SELECT * FROM tb_users")
        result = await cursor.fetchall()
        users = []
    for item in result:
        user = {"id": item[0],"pass":item[1], "level": item[2], "name": item[3]}
        users.append(user)   
    conn.close()
    return users


# 개별 사용자 정보
@hmid.get(path="/getUser/{id}/{password}",description="개별사용자정보",tags=["HMID"])
async def read_users(id: str,password: str):
    conn = await aiomysql.connect(host='220.94.157.27', port=53307,
                                      user='ineeji', password='ineeji1234',
                                      db='ineeji', autocommit=False)
    async with conn.cursor() as cursor:
        query = "SELECT user.id, user.name, com.id ,com.company_name FROM tb_users user , tb_company com , tb_layout lay WHERE user.id = %s AND user.password =%s AND user.company_id = com.id AND user.company_id = lay.company_id"
        await cursor.execute(query, (id,password,))
        result = await cursor.fetchone()
    conn.close()
    return {"id": result[0],"name":result[1], "company_id": result[2], "company_name": result[3]}

# 사용자별 레이아웃 정보
@hmid.get(path="/getLayout/{company_id}",description="전체레이아웃정보",tags=["HMID"])
async def read_layout(company_id: str):
    conn = await aiomysql.connect(host='220.94.157.27', port=53307,
                                      user='ineeji', password='ineeji1234',
                                      db='ineeji', autocommit=False)
    async with conn.cursor() as cursor:
        query = "SELECT id , name FROM tb_layout WHERE company_id = %s"
        await cursor.execute(query, (company_id,))
        result = await cursor.fetchall()
        lays = []
    for item in result:
        lay = {"id": item[0],"name":item[1]}
        lays.append(lay)
    conn.close()
    return lays

# 데이터 추가하기
@hmid.post(path="/createLayout",description="사용자별레이아웃 정보 추가",tags=["HMID"])
async def create_layout(company_id: str, user_id: str, lay_id: str, lay_list:str):
    conn = await aiomysql.connect(host='220.94.157.27', port=53307,
                                      user='ineeji', password='ineeji1234',
                                      db='ineeji', autocommit=False)
    async with conn.cursor() as cursor:
        query = "INSERT INTO tb_layoutlist (lay_list, company_id, user_id, lay_id) VALUES (%s, %s, %s, %s)"
        values = (lay_list, company_id, user_id, lay_id)
        await cursor.execute(query, values)
    await conn.commit()
    # conn().close()
    return {"message": "Item has been created successfully."}

# 데이터 수정하기
@hmid.put(path="/updateLayout",description="사용자별에이아웃 정보 수정",tags=["HMID"])
async def update_layout(company_id: str, user_id: str, lay_id: str, lay_list:str):
    conn = await aiomysql.connect(host='220.94.157.27', port=53307,
                                      user='ineeji', password='ineeji1234',
                                      db='ineeji', autocommit=False)
    async with conn.cursor() as cursor:
        query = "UPDATE tb_layoutlist SET lay_list=%s WHERE company_id=%s AND user_id=%s AND lay_id=%s"
        values = (lay_list, company_id, user_id, lay_id)
        await cursor.execute(query, values)
    await conn.commit()
    # conn().close()
    return {"message": "Item has been updated successfully."}