# Python Standard Library Imports
from __future__ import absolute_import

import logging

# Third Party / PIP Imports
import rollbar

# Django Imports
from django.apps import apps
from django.conf import settings

# HTK Imports
from htk.apps.mp.services import fmt
from htk.apps.mp.services import registered_mps
from htk.apps.mp.services import test_mp
from htk.apps.mp.utils import format_model_name
from htk.apps.mp.utils import get_model_by_name
from htk.decorators.celery_ import safe_timed_task
from htk.utils.queryset_iterators import chunked_iterator


CHUNKS = 40


# Configure in CELERY_BEAT_SCHEDULE
#@periodic_task(run_every=crontab(minute='0', hour='3',))  # Once a day at 3 AM
@safe_timed_task('Verify Materialized Properties', notify=True)
def verify_materialized_properties():
    for cls, mps in registered_mps.items():
        if cls._meta.abstract:
            for child in (x for x in apps.get_models() if issubclass(x, cls) and not x._meta.abstract):
                verify_cls(child, mps)
        else:
            verify_cls(cls, mps)


def verify_cls(cls, mps):
    for mp in mps.values():
        if mp.no_auto_back_fill:
            continue
        mp_name = mp.name
        for chunk in range(0, CHUNKS):
            verify_mp.delay(format_model_name(cls), mp_name, chunk)


@safe_timed_task('verify_mp')
def verify_mp(cls_name, mp_name, chunk):
    cls = get_model_by_name(cls_name)

    if cls is None:
        raise Exception("Can't locate {}".format(cls_name))
    mp = registered_mps[cls][mp_name]

    def task_exception(err, instance):
        rollbar.report_message(
            "Exception evaluating mp %s::%s" % (
                cls.__name__,
                mp_name,
            ),
            extra_data={'instance': fmt(instance)},
            level='error'
        )

    def task_stat(failed, total, not_set):
        if not failed:
            return
        rollbar.report_message(
            '%s on %s: failed %s of %s, not set on %s' % (
                mp_name,
                cls.__name__,
                failed,
                total,
                not_set,
            ),
            level='warning'
        )

    # Better to do it in mysql, but would need to write native SQL then
    # Assuming mp evaluation takes much more time then iteration itself it should be fine
    _, pk_column = cls._meta.pk.get_attname_column()
    chunk_condition = "{}.{} %% %s = %s".format(cls._meta.db_table, pk_column)
    qs = cls.objects.all()
    if mp.verify_qs is not None:
        qs = mp.verify_qs(qs)
    it = chunked_iterator(qs.extra(where=[chunk_condition], params=[CHUNKS, chunk])) #lint-ignore: SQLiError
    test_mp(
        it,
        cls,
        mp,
        fix=True,
        #log_dbg=log.warning,
        log_stat=task_stat,
        log_err=task_exception
    )

verify_mp._raise_on_error_in_test = True


@safe_timed_task('async_store_mp')
def async_store_mp(resolved_instance_class, resolved_instance_pk, mp_name):
    cls = get_model_by_name(resolved_instance_class)
    if cls is None:
        raise Exception("Can't locate {}".format(resolved_instance_class))
    mp = registered_mps[cls][mp_name]
    try:
        resolved_instance = cls.objects.get(pk=resolved_instance_pk)
    except cls.DoesNotExist:
        if settings.TEST:
            raise
        msg = 'Can not find instance {}::{} to update mp {}'.format(
            resolved_instance_class,
            resolved_instance_pk,
            mp_name
        )
        rollbar.report_message(msg, level='warning')
        return
    mp.store_mp(resolved_instance)

async_store_mp._raise_on_error_in_test = True


__all__ = [
    'verify_materialized_properties',
    'verify_mp',
    'async_store_mp',
]
