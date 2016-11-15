from __future__ import unicode_literals
import sqlite3
import logging


class Session(object):
    def __init__(self, db_address=None, **kwargs):
        self.db_address = db_address
        self.connection = None
        self.cursor = None
        self.connected = False

    def connect(self):
        """
        Establish connection to the database
        :return: None
        """
        logging.info("Connecting to {}".format(self.db_address))
        self.connection = sqlite3.connect(self.db_address)
        self.cursor = self.connection.cursor()
        self.connected = True

    def disconnect(self):
        """
        Establish connection to the database
        :return: None
        """
        logging.info("Disconnecting from {}".format(self.db_address))
        self.connection.close()
        self.cursor = None
        self.connected = False

    def execute(self, sql):
        """
        Execute operation given constructed SQL
        :param sql: A string of valid SQL
        """
        logging.info(sql)
        self.cursor.execute(sql)

    def commit(self):
        return self.connection.commit()

    def get(self, entity, eid, fields=None):
        """
        Retrieve a single instance of an entity from the database by its primary key.

        :param entity: subclass of Entity, represented in database
        :param eid: unique identifier of the Entity
        :param fields: list of fields to return in the resolved Entity. Defaults to Entity.__fields__.keys()
        :return: an instance of an Entity object or None if not found
        """

        sql = """
        SELECT {fields} FROM {table_name} WHERE {primary_key} = {eid};
        """.format(
            fields=', '.join(fields) if fields else '*',
            table_name=entity.__table_name__,
            primary_key=entity.__primary_key__,
            eid=eid
        )
        self.execute(sql)
        # Parse results
        result = self.cursor.fetchone()
        columns = [description[0] for description in self.cursor.description]
        if not result:
            return None
        else:
            return self.deserialize(entity, columns, result)

    def get_all(self, entity, fields=None, filters=None):
        """
        Retrieve multiple instances of an Entity from the database by a selection of filters
        :param entity: subclass of Entity, represented in database
        :param fields: list of fields to return in the resolved Entity. Defaults to Entity.__fields__.keys()
        :param filters: dictionary of filters keyed by attribute name, only supports '==' operand and 'IS NULL'
        :return: a list of instances of an Entity object
        """

        filter_phrase = None
        if filters:
            # Construct filters into SQL phrase
            filter_list = []
            for attr, value in filters.items():
                if value is None:
                    filter_list.append('{} IS NULL'.format(attr))
                else:
                    filter_list.append('{}=="{}"'.format(attr, value))

            if filter_list:
                filter_phrase = 'WHERE ' + ' AND '.join(filter_list)

        sql = """
        SELECT {fields} FROM {table_name} {filter_phrase};
        """.format(
            fields=', '.join(fields) if fields else '*',
            table_name=entity.__table_name__,
            filter_phrase=filter_phrase or ''
        )

        # Execute operation
        self.execute(sql)

        # Parse results
        results = []
        columns = [description[0] for description in self.cursor.description]
        for result in self.cursor.fetchall():
            results.append(self.deserialize(entity, columns, result))

        return results

    def add(self, entity):
        fields = [key for key in entity.__fields__.keys() if hasattr(entity,key)]
        values = ['"' + getattr(entity, field) + '"' for field in fields]

        sql = """
        INSERT INTO {table_name} ({fields}) VALUES ({values});
        """.format(
            table_name=entity.__table_name__,
            fields=', '.join(fields),
            values=', '.join(values)
        )

        self.execute(sql)

    def deserialize(self, entity, columns, raw_data):
        """
        Takes our result from a database query and constructs an Entity instance given the fields specified by the query
        :param entity:
        :param columns:
        :param raw_data:
        :return:
            Entity instance
        """
        return entity(**dict(zip(columns, raw_data)))


class Entity(object):
    """
    Base object for representing a single row in a DB as a python object
    """
    __table_name__ = None
    __primary_key__ = 'id'
    __fields__ = {}

    def __init__(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, self._sanitize(attr, value))

    def _sanitize(self, attr, value):
        """
        Attempts to coerce a given value to the type of an attribute listed in the __fields__ dict. Note that sqlite3
        handles the basic types we would be serializing (int, str, float, etc.), though datetime is an interesting
        example to handle on our own.
        :param attr:
        :param value:
        :return:
        """
        if attr not in self.__fields__.keys():
            raise AttributeError("'{attr}' is not a valid attribute for {entity}".format(
                attr=attr,
                entity=type(self).__name__
            ))

        try:
            sane_value = self.__fields__[attr](value)
        except BaseException:
            raise ValueError("'{value}' could not be coerced into a sane value for {entity}.{attr}".format(
                value=value,
                attr=attr,
                entity=type(self).__name__
            ))
        return sane_value

    def __repr__(self):
        """
        Clean representation of any entity, listing primary key and available fields.
        :return:
            str
        """
        field_reprs = []
        for attr in self.__fields__.keys():
            if attr != self.__primary_key__:
                field_reprs.append('{0}={1}'.format(attr, getattr(self, attr, None)))

        field_repr_str = ', '.join(field_reprs)
        if field_repr_str:
            field_repr_str = ' ' + field_repr_str

        return "{entity_name}({primary_key}{field_repr})".format(
            entity_name=type(self).__name__,
            primary_key=getattr(self, self.__primary_key__, None),
            field_repr=field_repr_str
        ).encode('utf8')

