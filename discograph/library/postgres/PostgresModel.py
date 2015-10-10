# -*- encoding: utf-8 -*-
import peewee
import random
from abjad.tools import systemtools


database = peewee.PostgresqlExtDatabase(
    'discograph',
    user='postgres',
    )


class PostgresModel(peewee.Model):

    ### PEEWEE FIELDS ###

    random = peewee.FloatField(index=True)

    ### PEEWEE META ###

    class Meta:
        database = database

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatManager.get_storage_format(self)
        return str(self)

    def __repr__(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatManager.get_repr_format(self)

    ### PRIVATE PROPERTIES ###

    @property
    def _storage_format_specification(self):
        keyword_argument_names = sorted(self._fields)
        if 'id' in keyword_argument_names:
            keyword_argument_names.remove('id')
        for keyword_argument_name in keyword_argument_names[:]:
            value = getattr(self, keyword_argument_name)
            if isinstance(value, list) and not value:
                keyword_argument_names.remove(keyword_argument_name)
        return systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=keyword_argument_names,
            )

    @property
    def _repr_specification(self):
        return self._storage_format_specification

    ### PUBLIC METHODS ###

    @classmethod
    def get_random(cls):
        n = random.random()
        return cls.select().where(cls.random > n).order_by(cls.random).get()