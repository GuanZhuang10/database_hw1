from be.model import error
from be.model.db_conn import DBConn


class Seller(DBConn):
    def __init__(self):
        DBConn.__init__(self)

    def add_book(
            self,
            user_id: str,
            store_id: str,
            book_id: str,
            book_json_str: str,
            stock_level: int,
    ):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)
            if self.book_id_exist(store_id, book_id):
                return error.error_exist_book_id(book_id)

            # 在MongoDB中插入书本信息
            book_info = {
                "store_id": store_id,
                "book_id": book_id,
                "book_info": book_json_str,
                "stock_level": stock_level,
            }
            self.db.db.store.insert_one(book_info)
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    def add_stock_level(
            self, user_id: str, store_id: str, book_id: str, add_stock_level: int
    ):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)

            # 更新MongoDB中书本的库存
            filter = {"store_id": store_id, "book_id": book_id}
            update = {"$inc": {"stock_level": add_stock_level}}
            self.db.db.store.update_one(filter, update)
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    def create_store(self, user_id: str, store_id: str) -> (int, str):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if self.store_id_exist(store_id):
                return error.error_exist_store_id(store_id)

            # 在MongoDB中插入商店信息
            store_info = {"store_id": store_id, "user_id": user_id}
            self.db.db.user_store.insert_one(store_info)
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

# import sqlite3 as sqlite
# from be.model import error
# from be.model import db_conn
#
#
# class Seller(db_conn.DBConn):
#     def __init__(self):
#         db_conn.DBConn.__init__(self)
#
#     def add_book(
#         self,
#         user_id: str,
#         store_id: str,
#         book_id: str,
#         book_json_str: str,
#         stock_level: int,
#     ):
#         try:
#             if not self.user_id_exist(user_id):
#                 return error.error_non_exist_user_id(user_id)
#             if not self.store_id_exist(store_id):
#                 return error.error_non_exist_store_id(store_id)
#             if self.book_id_exist(store_id, book_id):
#                 return error.error_exist_book_id(book_id)
#
#             self.conn.execute(
#                 "INSERT into store(store_id, book_id, book_info, stock_level)"
#                 "VALUES (?, ?, ?, ?)",
#                 (store_id, book_id, book_json_str, stock_level),
#             )
#             self.conn.commit()
#         except sqlite.Error as e:
#             return 528, "{}".format(str(e))
#         except BaseException as e:
#             return 530, "{}".format(str(e))
#         return 200, "ok"
#
#     def add_stock_level(
#         self, user_id: str, store_id: str, book_id: str, add_stock_level: int
#     ):
#         try:
#             if not self.user_id_exist(user_id):
#                 return error.error_non_exist_user_id(user_id)
#             if not self.store_id_exist(store_id):
#                 return error.error_non_exist_store_id(store_id)
#             if not self.book_id_exist(store_id, book_id):
#                 return error.error_non_exist_book_id(book_id)
#
#             self.conn.execute(
#                 "UPDATE store SET stock_level = stock_level + ? "
#                 "WHERE store_id = ? AND book_id = ?",
#                 (add_stock_level, store_id, book_id),
#             )
#             self.conn.commit()
#         except sqlite.Error as e:
#             return 528, "{}".format(str(e))
#         except BaseException as e:
#             return 530, "{}".format(str(e))
#         return 200, "ok"
#
#     def create_store(self, user_id: str, store_id: str) -> (int, str):
#         try:
#             if not self.user_id_exist(user_id):
#                 return error.error_non_exist_user_id(user_id)
#             if self.store_id_exist(store_id):
#                 return error.error_exist_store_id(store_id)
#             self.conn.execute(
#                 "INSERT into user_store(store_id, user_id)" "VALUES (?, ?)",
#                 (store_id, user_id),
#             )
#             self.conn.commit()
#         except sqlite.Error as e:
#             return 528, "{}".format(str(e))
#         except BaseException as e:
#             return 530, "{}".format(str(e))
#         return 200, "ok"
