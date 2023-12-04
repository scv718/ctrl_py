# from sqlalchemy.orm import Session
from sqlalchemy import text, inspect
from fastapi.responses import JSONResponse
import db.gigaeyes_models as models
import db.gigaeyes_schema as schemas
import datetime as dt
import core.log as common

## engine을 사용함으로 ORM을 사용하는것이 아닌 SQL 자체를 건드리는 방식을 사용하는 것으로 성능 이슈가 없다고 나옴
## with 과 같이 사용하면 sqlalchmy에서 conn 변수가 사용이 끝나면 자동으로 닫아줌. 컨텍스트 관리 및 자원해제를 자동으로 관리해줌

log = common.logging.getLogger("api")


def insert(engine, table, data):
    user_dict = data
    if not isinstance(data, dict):
        user_dict = data.dict()

    table_name = table.__tablename__

    keys = user_dict.keys()
    ## {user_id : "123", user_reg : Now() }
    # user_id, user_reg
    column_names = ",".join([f'"{col}"' for col in keys])
    placeholders = ",".join([f':{col}' for col in keys])
    print(keys)
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
            return {"res_code": 200, "msg": "DB INSERT SUCCESS"}
        except Exception as e:
            trans.rollback()
            print(e)
            print("Insert DB Fail")
            return {"res_code": 400, "msg": "DB INSERT FAIL"}


def insert_user_cam_info(conn, table, data):
    user_dict = data
    if not isinstance(data, dict):
        user_dict = data.dict()

    table_name = table.__tablename__

    keys = user_dict.keys()
    column_names = ",".join([f'"{col}"' for col in keys])
    placeholders = ",".join([f':{col}' for col in keys])
    print(keys)

    if table_name.isupper():
        sql = f'INSERT INTO "{table_name}" ({column_names}) VALUES ({placeholders})'
    else:
        sql = f'INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})'

    try:

        result = conn.execute(text(sql), user_dict)

        log.info("insert result : %s", result)
        return {"res_code": 200, "msg": "DB INSERT SUCCESS"}
    except Exception as e:
        print(e)
        log.info("Insert DB Fail")
        return {"res_code": 400, "msg": "DB INSERT FAIL"}


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
            columns = result.keys()
            data = [dict(zip(columns, row)) for row in result.fetchall()]
            print("data : ", data)
        return data

    except Exception as e:
        print("Select DB Fail", e)
        return {"error": "Selection failed"}


def selectUserCodeDB(conn, table, user_code, cam_code):
    table_name = table.__tablename__

    print(user_code)
    if table_name.isupper():
        sql = text(f'select * from "{table_name}" where "USER_CODE" = :user_code and "CAM_CODE" = :cam_code')
    else:
        sql = text(f'select * from {table_name} where "USER_CODE" = :user_code and "CAM_CODE" = :cam_code')

    print(sql)
    params = {
        "user_code": user_code,
        "cam_code": cam_code}
    try:
        result = conn.execute(sql, params)
        # data = [dict(row) for row in result.fetchall()]
        columns = result.keys()

        # Fetch all rows as a list of dictionaries
        data = [dict(zip(columns, row)) for row in result.fetchall()]
        print(data)
        return data
    except Exception as e:
        print("Select DB Fail", e)
        return {"error": "Selection failed"}


def selectJson(engine, table, json_data):
    table_name = table.__tablename__

    print(json_data)

    json_col = [col for col in json_data.keys()]

    where_clause = " AND ".join([f'"{col}" =:{col}' for col in json_col])

    print(where_clause)
    if table_name.isupper():
        # sql = f'select * from "{table_name}" where {where_clause}'
        sql = f'select * from "{table_name}" where {where_clause}'
    else:
        sql = f'select * from {table_name} where {where_clause}'

    try:
        with engine.connect() as conn:
            print(sql)
            result = conn.execute(text(sql), json_data)
            # data = [dict(row) for row in result.fetchall()]
            columns = result.keys()

            # Fetch all rows as a list of dictionaries
            data = [dict(zip(columns, row)) for row in result.fetchall()]

            print("data:", data)
        return data
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
