import sqlalchemy


storage_ref = ''
storage_auf_name = ''
engine = sqlalchemy.create_engine(storage_ref)


def select_all_query_execute(column_to_value: dict[str, str], table_name: str) -> list[dict[str, str]] | None:
    with engine.connect() as connection:
        meta = sqlalchemy.MetaData()
        meta.reflect(bind=engine)
        table = meta.tables[table_name]

        query = sqlalchemy.select(table).where(
            sqlalchemy.and_(
                *[
                    sqlalchemy.column(column) == value
                    for column, value in column_to_value.items()
                ]
            )
        )
        result = connection.execute(query)

        if result.rowcount == 0:
            return None

        return result.mappings().all()


def insert_query_execute(column_to_value: dict[str, str], table_name: str) -> None:
    with engine.connect() as connection:
        meta = sqlalchemy.MetaData()
        meta.reflect(bind=engine)
        table = meta.tables[table_name]
        query = sqlalchemy.insert(table).values(**column_to_value)
        connection.execute(query)
        connection.commit()
