import aiomysql
from fastapi import APIRouter, UploadFile
from app.schemas import TageItem
from typing import List
from app.models.tag import Tag

tag = APIRouter()

#db = pymysql.connect(host='localhost', port=3306, user='root', passwd='ineeji1234', db='ineeji', charset='utf8')
# async def go():
#     conn = await aiomysql.create_pool(host='127.0.0.1', port=3306,
#                                       user='root', password='ineeji1234',
#                                       db='mysql', autocommit=False)
#     return conn

# 전체 태그 정보
@tag.get(path="/getTagList",description="전체태그리스트" ,tags=["TAG"])
async def read_tag_list():
    conn = await aiomysql.connect(host='220.94.157.27', port=53307,
                                      user='ineeji', password='ineeji1234',
                                      db='ineeji', autocommit=True)
    async with conn.cursor() as cursor:
        await cursor.execute("SELECT * FROM tb_tag")
        result = await cursor.fetchall()
        tags = []
    for item in result:
        tag = {"id": item[0],"name":item[1], "unit": item[2], "description": item[3]}
        tags.append(tag)   
    conn.close()
    return tags


# 태그 추가
@tag.post(path="/createTag",description="태그 추가",tags=["TAG"])
async def create_tag(data :List[TageItem] ):
    tags = []
    for item in data:
        tag = (item.name,item.unit,item.description)
        tags.append(tag)  
        print(tags)
    conn = await aiomysql.connect(host='220.94.157.27', port=53307,
                                      user='ineeji', password='ineeji1234',
                                      db='ineeji', autocommit=False)
    async with conn.cursor() as cursor:
        # query = "INSERT INTO tb_tag (id, name, unit, description) VALUES (%s, %s, %s, %s)"
        # values = (id, name, unit, description)
        # await cursor.executemay(query, values)
        query = "INSERT INTO tb_tag (name, unit, description) VALUES ( %s, %s, %s)"
        await cursor.executemany(query, tags)
    await conn.commit()
    conn().close()
    return {"message": "Item has been created successfully."}

# 태그 수정하기
@tag.put(path="/updateTag",description= "태그 수정",tags=["TAG"])
async def update_tag(id: int, name: str, unit: str, desc:str):
    conn = await aiomysql.connect(host='220.94.157.27', port=53307,
                                      user='ineeji', password='ineeji1234',
                                      db='ineeji', autocommit=False)
    async with conn.cursor() as cursor:
        query = "UPDATE tb_tag SET name=%s, unit=%s, description=%s WHERE id=%s"
        values = (name, unit, desc,id)
        await cursor.execute(query, values)
    await conn.commit()
    # conn().close()
    return {"message": "Item has been updated successfully."}


#태그 삭제하기
@tag.delete(path="/deleteTag/{id}",description="태그 삭제",tags=["TAG"])
async def delete_tag(id: int):
    conn = await aiomysql.connect(host='220.94.157.27', port=53307,
                                      user='ineeji', password='ineeji1234',
                                      db='ineeji', autocommit=True)
    async with conn.cursor() as cursor:
        query = "DELETE FROM tb_tag WHERE id=%s"
        values = (id,)
        await cursor.execute(query, values)
    await conn.commit()
    return {"message": "Item has been deleted successfully."}

# 사용중인 태그 정보
@tag.post(path="/inUseTag",description="사용중인 태그 정보" ,tags=["TAG"])
async def in_use_tag(data :List[TageItem] ):
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
    tags = []
    for item in result:
        tag = {"name":item[1], "unit": item[2], "description": item[3]}
        tags.append(tag)   
    conn.close()
    return tags

# @tag.post(path="/uploadfile",description="CSV 파일 업로드",tags=["TAG"])
# async def create_upload_file(file: UploadFile):
#     print(await file.read())
#     return {"filename": file.filename}