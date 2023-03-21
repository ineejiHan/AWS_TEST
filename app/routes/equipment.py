import json
import aiomysql
from fastapi import APIRouter
from app.schemas import EquipItem
from typing import List
equip = APIRouter()

#db = pymysql.connect(host='localhost', port=3306, user='root', passwd='ineeji1234', db='ineeji', charset='utf8')
# async def go():
#     conn = await aiomysql.create_pool(host='127.0.0.1', port=3306,
#                                       user='root', password='ineeji1234',
#                                       db='mysql', autocommit=False)
#     return conn

# 전체 설비 정보
@equip.get(path="/getEquipList",description="전체 설비 리스트" ,tags=["EQUIP"])
async def read_equip_List():
    conn = await aiomysql.connect(host='220.94.157.27', port=53307,
                                      user='ineeji', password='ineeji1234',
                                      db='ineeji', autocommit=True)
    async with conn.cursor() as cursor:
        await cursor.execute("SELECT id, name, input, output, internal, description FROM tb_equipment")
        result = await cursor.fetchall()
        equips = []
    for item in result:
        equip = {"id": item[0],"name":item[1], "input": item[2], "output": item[3] , "internal": item[4] , "description": item[5]}
        equips.append(equip)   
    conn.close()
    return equips

# 태그 추가
@equip.post(path="/createEquip",description="태그 추가",tags=["EQUIP"])
async def create_equip(data :List[EquipItem] ):
    equips = []
    for item in data:
        equip = (item.name,json.dumps(item.input),json.dumps(item.output),json.dumps(item.internal),item.description)
        equips.append(equip)  
    conn = await aiomysql.connect(host='220.94.157.27', port=53307,
                                      user='ineeji', password='ineeji1234',
                                      db='ineeji', autocommit=False)
    async with conn.cursor() as cursor:
        query = "INSERT INTO tb_equipment (name, input, output, internal, description) VALUES ( %s, %s, %s, %s, %s)"
        await cursor.executemany(query, equips)
    await conn.commit()
    #conn().close()
    return {"message": "Item has been created successfully."}

# 설비 수정하기
@equip.put(path="/updateEquip",description= "설비 수정",tags=["EQUIP"])
async def update_equip(data:EquipItem):
    conn = await aiomysql.connect(host='220.94.157.27', port=53307,
                                      user='ineeji', password='ineeji1234',
                                      db='ineeji', autocommit=False)
    async with conn.cursor() as cursor:
        query = "UPDATE tb_equipment SET  name=%s, input=%s, output=%s, internal=%s, description=%s WHERE id=%s"
        values = (data.name, json.dumps(data.input), json.dumps(data.output), json.dumps(data.internal), data.description, data.id)
        await cursor.execute(query, values)
    await conn.commit()
    # conn().close()
    return {"message": "Item has been updated successfully."}

#섧비 삭제하기
@equip.delete(path="/deleteEquip/{id}",description="설비 삭제",tags=["EQUIP"])
async def delete_equip(id: int):
    conn = await aiomysql.connect(host='220.94.157.27', port=53307,
                                      user='ineeji', password='ineeji1234',
                                      db='ineeji', autocommit=True)
    async with conn.cursor() as cursor:
        query = "DELETE FROM tb_equipment WHERE id=%s"
        values = (id,)
        await cursor.execute(query, values)
    await conn.commit()
    return {"message": "Item has been deleted successfully."}

# 지정된 태그를 사용하는 설비
@equip.get(path="inUseTagForEquip",description="지정된 태그를 사용하는 설비" ,tags=["EQUIP"])
async def in_use_tag_for_equip(id:List[int]):
    query = "SELECT * FROM tb_tag WHERE name IN ("
    for item in data:
        query += "'"+item.name+"',"
    query = query[0:-1]
    query += ");"

    conn = await aiomysql.connect(host='220.94.157.27', port=53307,
                                      user='ineeji', password='ineeji1234',
                                      db='ineeji', autocommit=True)
    async with conn.cursor() as cursor:
        await cursor.execute(query)
        result = await cursor.fetchall()
        print(result)
        
    tags = []
    for item in result:
        tag = {"name":item[1], "unit": item[2], "description": item[3]}
        tags.append(tag)   
    conn.close()
    return tags