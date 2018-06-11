# -*- coding: utf-8 -*-

from numbers import Integral
from functools import wraps
from contextlib import contextmanager

try:
    import ujson as json
except Exception:
    import json


@contextmanager
def ServiceContext(service, auto_commit=False):
    try:
        yield

        try:
            if auto_commit:
                service.db.session.commit()
            else:
                service.db.session.flush()
        except Exception:
            service.db.session.rollback()
            raise
    except Exception:
        service.db.session.rollback()
        raise


def transaction(method, auto_commit=False):
    @wraps(method)
    def _transaction(*args, **kwargs):
        assert isinstance(args[0], BaseBareModelService)
        _auto_commit = kwargs.pop('auto_commit', auto_commit)
        with ServiceContext(args[0], auto_commit=_auto_commit):
            return method(*args, **kwargs)
    return _transaction


class BaseBareModelService(object):

    def __init__(self, db):
        self.db = db
        self.model = getattr(self, 'model', None)
        self.update_unchangeable_keys = getattr(
            self, 'update_unchangeable_keys', [])
        self.json_keys = getattr(self, 'json_keys', [])
        self.json_compress_keys = getattr(self, 'json_compress_keys', [])
        self.int_keys = getattr(self, 'int_keys', [])
        self.search_fields = getattr(self, 'search_fields', [])

    def get_keys(self):
        return self.model.__table__.columns.keys()

    def get(self, *args, **kwargs):
        model = kwargs.pop('model')
        if args:
            id_or_ins = args[0]
            if isinstance(id_or_ins, model):  # or id_or_ins is None:
                return id_or_ins
            elif isinstance(id_or_ins, Integral):
                return model.query.get(int(id_or_ins))
            else:
                return None

        query = model.query
        for key in kwargs:
            if hasattr(model, key):
                query = query.filter(getattr(model, key) == kwargs[key])

        return query.first()

    @transaction
    def insert_data(self, row, return_primarys=False):
        db_cls = self.model
        r = self.db.session.execute(db_cls.__table__.insert(), row)
        return r.inserted_primary_key[0] if return_primarys else None

    @transaction
    def insert_batch_data(self, rows, return_primarys=False):
        db_cls = self.model
        ids = []
        if return_primarys:
            for row in rows:
                row_id = self.insert_data(db_cls, row, return_primarys)
                ids.append(row_id)
        else:
            self.db.session.execute(db_cls.__table__.insert(), rows)

        return ids

    def insert(self, db_obj):
        self.db.session.add(db_obj)
        self.db.session.flush()
        db_obj = self.db.session.merge(db_obj)
        return db_obj

    def get_filter_by_query(self, **kwargs):
        if not kwargs:
            return []

        model = self.model
        query = model.query.enable_eagerloads(False)
        for key in kwargs:
            if hasattr(model, key):
                query = query.filter(getattr(model, key) == kwargs[key])

        if hasattr(model, 'id'):
            query = query.order_by(getattr(model, 'id').asc())
        return query

    def get_filter_query(self, filters):
        if not filters:
            return []
        return self.model.query.enable_eagerloads(False).filter(*filters)

    def exists_filter_by_query(self, **kwargs):
        q = self.get_filter_by_query(**kwargs)
        if not q:
            return False
        return self.db.session.query(q.exists()).scalar()

    def create(self, **kwargs):
        new = self.model()
        new = self.update_item(new, kwargs)
        new = self.insert(new)
        return True, int(new.id)

    def update(self, primary_id, **kwargs):
        item = self.get(primary_id)
        if not item:
            return False, 'db item [%s] did not exist' % primary_id

        self.update_item(item, kwargs)
        return True, primary_id

    def update_item(self, row, info, ignore_none=True):

        unchangeable_keys = ['id', 'created_at']
        unchangeable_keys.extend(self.update_unchangeable_keys)

        model_keys = self.get_keys()
        for key, value in info.iteritems():
            if (key not in model_keys or (value is None and ignore_none)
                    or key in unchangeable_keys):
                continue
            if key in self.json_keys and not isinstance(value, str):
                setattr(row, key, json.dumps(value))
            else:
                setattr(row, key, value)
        return row

    def full_update(self, primary_id, **kwargs):
        item = self.get(primary_id)
        if not item:
            return False, 'item {} not in db'.format(primary_id)
        self.update_item(item, kwargs, ignore_none=False)
        return True, primary_id

    def get_info(self, *args, **kwargs):
        item = self.get(*args, **kwargs)
        info = {}
        if item:
            model_keys = self.get_keys()
            for key in model_keys:
                if key in self.json_keys:
                    value = json.loads(getattr(item, key))
                else:
                    value = getattr(item, key, None)
                info[key] = value
        for key in self.int_keys:
            if key in info:
                info[key] = int(info[key] or 0)
        return info

    def batch_update(self, primary_ids, **kwargs):
        from app.common.data_helper import slice_list

        if not primary_ids:
            return []

        unchangeable_keys = ['id', 'created_at']
        unchangeable_keys.extend(self.update_unchangeable_keys)

        fields = {}
        model_keys = self.get_keys()
        for key, value in kwargs.iteritems():
            if key in model_keys:
                if key in unchangeable_keys:
                    continue
                if key in self.json_keys and not isinstance(value, str):
                    value = json.dumps(value)

            fields[key] = value

        for ids in slice_list(primary_ids):
            statement = self.model.__table__.update().\
                where(self.model.id.in_(ids)).\
                values(**fields)
            self.db.session.execute(statement)
            self.db.session.commit()
        self.db.session.commit()
        return True
