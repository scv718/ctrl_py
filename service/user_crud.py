# from sqlalchemy.orm import Session
from sqlalchemy import text, inspect
from fastapi.responses import JSONResponse
import db.gigaeyes_models as models
import db.gigaeyes_schema as schemas
import datetime as dt
import core.log as common

## engine을 사용함으로 ORM을 사용하는것이 아닌 SQL 자체를 건드리는 방식을 사용하는 것으로 성능 이슈가 없다고 나옴
## with 과 같이 사용하면 sqlalchmy에서 conn 변수가 사용이 끝나면 자동으로 닫아줌. 컨텍스트 관리 및 자원해제를 자동으로 관리해줌

# log = common.logging.getLogger("api")


# def insertDB(engine, table, data):
#     user_dict = data.dict()
#     table_name = table.__tablename__

#     keys = user_dict.keys()
#     column_names = ",".join(keys)
#     placeholders = ",".join([f':{col}' for col in keys])

#     if table_name.isupper():
#         table_name = f'"{table_name}"'

#     sql = f'INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})'

#     print(sql)
#     print(user_dict)
#     with engine.connect() as conn:
#         trans = conn.begin()
#         try:
#             result = conn.execute(text(sql), user_dict)
#             trans.commit()
#             return {"res_code": 200}
#         except Exception as e:
#             trans.rollback()
#             print(e)
#             print("Insert DB Fail")
#             return {"error": "Insert failed"}

def selectAllDB(engine, table):
    table_name = table.__tablename__

    if table_name.isupper():
        sql = f'select * from "{table_name}"'
    else:
        sql = f'select * from {table_name}'

    print(sql)
    try:
        with engine.connect() as conn:
            result = conn.execute(text(sql))
            data = [dict(row) for row in result.fetchall()]
        return JSONResponse(content=data)

    except Exception as e:
        print("Select DB Fail", e)
        return {"error": "Selection failed"}


def insertDB(engine, table, data):
    user_dict = data.dict()
    table_name = table.__tablename__

    keys = user_dict.keys()
    column_names = ",".join([f'"{col}"' for col in keys])
    placeholders = ",".join([f':{col}' for col in keys])
    print(keys)

    # sql = "SELECT * FROM users WHERE username = %s AND password = %s"
    # conn.execute(sql, ('john', 'pass123'))

    # sql = f'INSERT INTO {table_name} (CAM_CODE, MODEL_CODE, CAM_ID, CONN_TYPE) VALUES (:CAM_CODE, :MODEL_CODE, :CAM_ID, :CONN_TYPE)'
    # result = conn.execute(text(sql), CAM_CODE=333, MODEL_CODE=1, CAM_ID='33', CONN_TYPE='N')

    # [2023-11-01 16:23:26,140] [AnyIO worker thread] [DEBUG] INSERT INTO "VMS_CAM_INFO" ("CAM_CODE","MODEL_CODE","CAM_ID","CONN_TYPE")
    #                                                         VALUES (:CAM_CODE,:MODEL_CODE,:CAM_ID,:CONN_TYPE)
    # [2023-11-01 16:23:26,140] [AnyIO worker thread] [DEBUG] {'CAM_CODE': 33113, 'MODEL_CODE': 1, 'CAM_ID': '3113', 'CONN_TYPE': 'N'}

    if table_name.isupper():
        sql = f'INSERT INTO "{table_name}" ({column_names}) VALUES ({placeholders})'
    else:
        sql = f'INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})'

    with engine.connect() as conn:
        trans = conn.begin()
        try:
            result = conn.execute(text(sql), user_dict)
            # 쿼리문
            # log.debug(sql)
            # MAP
            # log.debug(user_dict)
            trans.commit()
            return {"res_code": 200, "msg" : "DB INSERT SUCCESS"}
        except Exception as e:
            trans.rollback()
            print(e)
            print("Insert DB Fail")
            return {"res_code": 400, "msg" : "DB INSERT FAIL"}


def selectAllDB(engine, table):
    table_name = table.__tablename__

    if table_name.isupper():
        sql = f'select * from "{table_name}"'
    else:
        sql = f'select * from {table_name}'

    print(sql)
    try:
        with engine.connect() as conn:
            result = conn.execute(text(sql))
            data = [dict(row) for row in result.fetchall()]
        return JSONResponse(content=data)

    except Exception as e:
        print("Select DB Fail", e)
        return {"error": "Selection failed"}


def selectUserCodeDB(engine, table, user_code):
    table_name = table.__tablename__

    print(user_code)
    if table_name.isupper():
        sql = text(f'select * from "{table_name}" where "USER_CODE" = :user_code')
    else:
        sql = text(f'select * from {table_name} where "USER_CODE" = :user_code')

    print(sql)
    params = {"user_code" : user_code}
    try:
        with engine.connect() as conn:
            result = conn.execute(sql, params)
            # print(result)
            # data = [dict(row) for row in result.fetchall()]
        # return JSONResponse(content=data)
        return result.fetchall()
    except Exception as e:
        print("Select DB Fail", e)
        return {"error": "Selection failed"}


def selectJson(engine, table, json_data):
    table_name = table.__tablename__

    json_col = [col for col in json_data.keys()]

    where_clause = " AND ".join([f'"{col}" = :{col}' for col in json_col])

    if table_name.isupper():
        sql = text(f'select * from "{table_name}" where {where_clause}')
    else:
        sql = text(f'select * from {table_name} where {where_clause}')

    try:
        with engine.connect() as conn:
            result = conn.execute(sql, json_data)
            data = [dict(row) for row in result.fetchall()]

            print(data)
        return JSONResponse(content=data)
    except Exception as e:
        print("Select DB Fail", e)
        return {"error": "Selection failed"}


def updateDB(engine, table, data):
    user_dict = data.dict()
    table_name = table.__tablename__

    primary_key_columns = [col.name for col in table.__table__.primary_key]
    non_primary_columns = [col for col in user_dict.keys() if col not in primary_key_columns]

    set_clause = ", ".join([f'"{col}" = :{col}' for col in non_primary_columns])
    where_clause = " AND ".join([f'"{col}" = :{col}' for col in primary_key_columns])

    if table_name.isupper():
        sql = f'UPDATE "{table_name}" SET {set_clause} WHERE {where_clause}'
    else:
        sql = f'UPDATE {table_name} SET {set_clause} WHERE {where_clause}'

    try:
        with engine.connect() as conn:
            result = conn.execute(text(sql), **user_dict)
            row_count = result.rowcount

        return {"message": f"Updated {row_count} row(s)"}

    except Exception as e:
        print("Update DB Fail", e)
        return {"error": "Update failed"}


def deleteUserCodeDB(engine, table, data):
    user_dict = data.dict()
    table_name = table.__tablename__

    user_code = user_dict.get("USER_CODE")

    sql = text(f'DELETE FROM "{table_name}" WHERE "USER_CODE" = :user_code')

    try:
        with engine.connect() as conn:
            result = conn.execute(sql, user_code=user_code)
            num_deleted = result.rowcount
            print(num_deleted)
            return JSONResponse(content={"message": f"Deleted {num_deleted} row(s)"})
    except Exception as e:
        print("Delete DB Fail", e)
        return JSONResponse(content={"error": "Deletion failed"})

# def updateDB(table, data):
#     user_dict = data.dict()
#     keys = user_dict.keys()
#     values = [user_dict[key] for key in keys]
#     table_name = table.__tablename__

#     primary_key_columns = [col.name for col in table.__table__.primary_key]

#     non_primary_columns = [col for col in user_dict.keys() if col not in primary_key_columns]
#     print(values)
#     print(primary_key_columns)
#     print(non_primary_columns)

#     # set_clause = ", ".join([f'"{col}" = :{col}' for col in non_primary_columns])
#     # where_clause = " AND ".join([f'"{col}" = :{col}' for col in primary_key_columns])
#     set_clause = ", ".join([f'"{col}" = %s' for col in non_primary_columns])
#     where_clause = " AND ".join([f'"{col}" = %s' for col in primary_key_columns])


#     if table_name.isupper():
#         sql = f'UPDATE "{table_name}" SET {set_clause} WHERE {where_clause}'
#     else:
#         sql = f'UPDATE {table_name} SET {set_clause} WHERE {where_clause}'

#     conn = db.create_connection()
#     cur = db.create_cursor(conn)

#     print(sql)
#     try:
#         cur.execute(sql, values)

#         db.commit(conn)

#         return {"message": "Updated row(s)"}

#     except Exception as e:
#         print("Update DB Fail", e)
#         return {"error": "Update failed"}

#     finally:
#         db.close_cursor(cur)
#         db.close_connection(conn)

# def create_user(db: Session, user: schemas.UserCreate):
#     # db_user = models.Giga_user(USER_CODE=user.USER_CODE, USER_ID=user.USER_ID, REG_DATETIME = dt.datetime.now(), MOD_DATETIME = dt.datetime.now())

#     # db.add(db_user)
#     # db.commit()
#     # db.refresh(db_user)

#     sql = text('INSERT INTO "VMS_USER_INFO" ("USER_CODE", "USER_ID", "REG_DATETIME", "MOD_DATETIME") VALUES (:USER_CODE, :USER_ID, :REG_DATETIME, :MOD_DATETIME)')

#     result = db.execute(sql, {
#         "USER_CODE": user.USER_CODE,
#         "USER_ID": user.USER_ID,
#         "REG_DATETIME": dt.datetime.now(),
#         "MOD_DATETIME": dt.datetime.now()
#     })

#     return result

# def update_user(db: Session, user: schemas.UserUpdate):
#     existing_user = db.query(models.Giga_user).filter(models.Giga_user.USER_CODE == user.USER_CODE).first()
#     if existing_user:
#         existing_user.DEL_FLAG = user.DEL_FLAG
#         existing_user.MOD_DATETIME = dt.datetime.now()
#         db.commit()
#         db.refresh(existing_user)
#     return existing_user


