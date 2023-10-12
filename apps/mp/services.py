# Future Imports
from __future__ import absolute_import, print_function

# Python Standard Library Imports
import time
import traceback
import weakref
from collections import defaultdict
from functools import partial

# Third Party (PyPI) Imports
import rollbar

# Django Imports
import django
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import signals

# HTK Imports
from htk.apps.mp.signals import priority_connect
from htk.apps.mp.utils import format_model_name


EXTRA_VERBOSITY = False

MAGIC_VALUE_NOT_SET_STRING = '\0'

registered_mps = defaultdict(dict)


def materialized_property(
    field_definition,
    depends_on=None,
    _force_no_debug=False,
    no_auto_back_fill=False,
    use_is_set_field=False,
    mp_name=None,
    dbl_check_on_post_save=False,
    eventually_consistent=False,
    verify_qs=None,
):
    """Decorator to create a Materialized Property"""

    def wrap(f):
        return MaterializedPropertySubstitution(
            f,
            field_definition=field_definition,
            depends_on=depends_on,
            _force_no_debug=_force_no_debug,
            no_auto_back_fill=no_auto_back_fill,
            use_is_set_field=use_is_set_field,
            mp_name=mp_name,
            dbl_check_on_post_save=dbl_check_on_post_save,
            eventually_consistent=eventually_consistent,
            verify_qs=verify_qs,
        )

    return wrap


prepare_handlers = []


def to_field_name(mp_name):
    """Get the field name for the Materialized Property named `mp_name`"""
    return '_' + mp_name


class MaterializedPropertySubstitution(object):
    def __init__(
        self,
        f,
        field_definition,
        depends_on,
        _force_no_debug,
        no_auto_back_fill,
        use_is_set_field,
        mp_name,
        dbl_check_on_post_save,
        eventually_consistent,
        verify_qs,
    ):
        self.f = f
        self.field_definition = field_definition
        self.depends_on = set(depends_on or [])
        self._force_no_debug = _force_no_debug
        self.no_auto_back_fill = no_auto_back_fill
        self.use_is_set_field = use_is_set_field
        self.dependent_mps = []
        self.name = mp_name
        self.dbl_check_on_post_save = dbl_check_on_post_save
        self.eventually_consistent = eventually_consistent
        self.verify_qs = verify_qs

    def wrapped(self, *args, **kwargs):
        return self.f(*args, **kwargs)

    def contribute_to_class(self, cls, name):
        if self.verify_qs is not None and not callable(self.verify_qs):
            raise Exception(
                'verify_qs on {}.{} should be lambda, got {}'.format(
                    cls, name, type(self.verify_qs)
                )
            )
        if not self.name:
            self.name = name
        registered_mps[cls][self.name] = self
        self.cls = cls
        self.field_name = to_field_name(self.name)
        if not self.field_definition.db_column:
            self.field_definition.db_column = self.name
        is_set_field_name = (
            self.field_definition.db_column + '_is_set'
            if self.use_is_set_field
            else None
        )
        self.is_set_field_name = is_set_field_name

        if not self.no_auto_back_fill and not self.use_is_set_field:
            if isinstance(
                self.field_definition, models.CharField
            ) or isinstance(self.field_definition, models.TextField):
                is_set_q = {self.field_name: MAGIC_VALUE_NOT_SET_STRING}
                is_magic = lambda x: x == MAGIC_VALUE_NOT_SET_STRING
                self.field_definition.default = MAGIC_VALUE_NOT_SET_STRING
            else:
                is_set_q = {self.field_name + '__isnull': True}
                is_magic = lambda x: x is None
                self.field_definition.null = True
            self.is_not_set = lambda x: is_magic(getattr(x, self.field_name))
        else:
            is_set_q = {is_set_field_name: False}

            def is_not_set(instance):
                v = getattr(instance, is_set_field_name, 'Not set')
                if v == 'Not set':
                    extra_data = {}
                    try:
                        extra_data['all_field_names'] = ','.join(
                            type(instance)._meta.get_all_field_names()
                        )
                        extra_data['stacktrace'] = '\n'.join(
                            (
                                '%s, %s, %s, %s' % x
                                for x in traceback.extract_stack()
                            )
                        )
                    except:
                        rollbar.report_exc_info(
                            extra_data={
                                'message': 'Failed to evaluate extra_data for MP {} report'.format(
                                    name
                                ),
                            }
                        )
                    rollbar.report_message(
                        'instance of type {} for MP {} does not have property {}'.format(
                            type(instance), name, is_set_field_name
                        ),
                        level='error',
                        extra_data=extra_data,
                    )
                    return True
                return not v

            self.is_not_set = is_not_set

        def get_real(instance):
            real = self.f(instance)
            if (
                not self.no_auto_back_fill
                and not self.use_is_set_field
                and is_magic(real)
            ):
                rollbar.report_message(
                    'Real value returned by {}(pk={})::{} same as MAGIC_VALUE_NOT_SET, will cause cache miss (can impact performance)'.format(
                        cls.__name__, instance.pk, self.name
                    ),
                    level='error',
                )
            return real

        self.get_real = get_real

        def get_cached(instance):
            if not self.no_auto_back_fill and self.is_not_set(instance):
                real = get_real(instance)
                # rollbar.report_message(
                #     'setattr (initialize) attr=%s, value=%s, instance=%s' % (
                #         self.field_name,
                #         real,
                #         fmt(instance),
                #     ),
                #     level='info'
                # )
                self.update_on_instance(instance, real, more_q=is_set_q)
                return real

            return getattr(instance, self.field_name)

        def prop(instance):
            cached = get_cached(instance)
            if (
                False
                and settings.DEBUG_MATERIALIZED_PROPERTIES
                and not self._force_no_debug
            ):
                real = get_real(instance)
                if not self.values_equal(real, cached):
                    message = "Real value '{}' does not match cached value '{}' for {}::{} on {}".format(
                        real, cached, cls.__name__, self.name, instance.pk
                    )
                    if settings.MATERIALIZED_PROPERTIES_STRICT_CHECK:
                        raise Exception(message)
                    else:
                        print(message)
                        traceback.print_stack()
                return cached
            else:
                return cached

        prop.__is_mp__ = True
        setattr(cls, name, property(prop))
        self.field_definition.contribute_to_class(cls, self.field_name)
        if self.use_is_set_field:
            models.BooleanField(default=False, null=False).contribute_to_class(
                cls, is_set_field_name
            )
        prepare_handlers.append(self.handle_prepared)

    def values_equal(self, x, y):
        if isinstance(self.field_definition, models.DecimalField):
            if x is None or y is None:
                return x == y
            try:
                return self.field_definition.format_number(
                    x
                ) == self.field_definition.format_number(y)
            except:
                rollbar.report_exc_info(
                    extra_data={
                        'message': 'Failed to compare values for mp {}.{}, fallback to =='.format(
                            self.cls, self.name
                        ),
                        'x': x,
                        'y': y,
                    }
                )
        return x == y

    def handle_prepared(self):
        dependent_models = defaultdict(set)
        paths = {}
        for dependency in self.depends_on:
            for model, attr, path in parse_dependency(self.cls, dependency):
                depends_on_mp = registered_mps.get(model, {}).get(attr, None)
                if depends_on_mp:
                    if EXTRA_VERBOSITY:
                        print(
                            'MP dependency found: {}->{}'.format(
                                self.name, attr
                            )
                        )
                    depends_on_mp.dependent_mps.append((self, path))
                    continue

                if EXTRA_VERBOSITY:
                    print(
                        'Parsing dependency cls=%s, model=%s attr=%s path=%s'
                        % (self.cls, model, attr, path)
                    )
                dependent_models[model].add(attr)
                if attr != '*':
                    try:
                        field = model._meta.get_field(attr)
                    except models.FieldDoesNotExist:
                        message = 'MP {}.{} has dependency {} of attribute {} that is not a field or mp on {}'.format(
                            self.cls.__name__,
                            self.name,
                            dependency,
                            attr,
                            model.__name__,
                        )
                        raise Exception(message)
                if model in paths:
                    if paths[model] != path:
                        message = 'Model {} (dependent for {}) is accessible by dependents by using different paths {} and {}, which is not supported now'.format(
                            model, self.cls, paths[model], path
                        )

                        raise Exception(message)
                else:
                    paths[model] = path

        for model in dependent_models:
            path = paths[model]
            depends_on = dependent_models[model]
            self.connect_receiver(model, path, depends_on)

    def update_on_instance(
        self, instance, value, more_q=None, save=True, force=None
    ):
        if more_q is None:
            more_q = {}

        upd = {self.field_name: value}
        if self.use_is_set_field:
            upd[self.is_set_field_name] = True
        for k, v in upd.items():
            setattr(instance, k, v)
        if force is not None:
            force.update(upd.keys())
        if not save or not instance.pk:
            return

        if not self.cls.objects.filter(pk=instance.pk, **more_q).update(**upd):
            if not more_q:
                rollbar.report_message(
                    'Update failed when saving value of %s for %s with %s'
                    % (
                        self.name,
                        fmt(instance),
                        value,
                    ),
                    level='warning',
                )

    def store_mp_or_async(
        self,
        resolved_instance,
        source=None,
        save=True,
        force=None,
        changed_only=True,
    ):
        from htk.apps.mp.tasks import async_store_mp

        if self.eventually_consistent:
            cls = type(resolved_instance)
            async_store_mp.delay(
                format_model_name(cls),
                resolved_instance.pk,
                self.name,
            )
        else:
            self.store_mp(
                resolved_instance,
                source=source,
                save=save,
                force=force,
                changed_only=changed_only,
            )

    def store_mp(
        self,
        resolved_instance,
        source=None,
        save=True,
        force=None,
        changed_only=True,
    ):
        if resolved_instance.pk in pending_delete:
            # this `resolved_instance` is pending deletion
            # rollbar.report_message(
            #     'ignoring %s, in pending_delete(source=%s)' % (
            #         fmt(resolved_instance),
            #         source,
            #     ),
            #     level='info'
            # )
            pass
        else:
            # calculate the updated value
            value = self.f(resolved_instance)

            if changed_only and value == getattr(
                resolved_instance, self.field_name
            ):
                # skip for unchanged values

                # rollbar.report_message(
                #     'Skip setattr(value unchanged) attr=%s, value=%s, instance=%s, source=%s' % (
                #         self.field_name,
                #         value,
                #         fmt(resolved_instance),
                #         source,
                #     ),
                #     level='info'
                # )

                pass
            else:
                # rollbar.report_message(
                #     'setattr attr=%s, value=%s, instance=%s, changed_only=%s, source=%s' % (
                #         self.field_name,
                #         value,
                #         fmt(resolved_instance),
                #         changed_only,
                #         source,
                #     ),
                #     level='info'
                # )
                self.update_on_instance(
                    resolved_instance, value, save=save, force=force
                )

    def __repr__(self):
        return 'MaterializedProperty {} on {}'.format(
            self.name, self.cls.__name__
        )

    def connect_receiver(self, model, path, depends_on):
        def change_receiver(
            instance,
            signame,
            update_fields=None,
            save=True,
            force=None,
            second_check=False,
            *args,
            **kwargs  # fmt: skip
        ):
            source = '%s receiver %s, path %s, update_fields %s' % (
                signame,
                fmt(instance),
                path,
                update_fields,
            )
            if (
                '*' not in depends_on
                and update_fields is not None
                and not (set(update_fields) & depends_on)
            ):
                return
            if save:
                force = None
            for resolved_instance in resolve_instances(instance, path):
                old_resolved_instance = None
                if second_check:
                    old_resolved_instance = resolved_instance
                    resolved_instance = (
                        resolved_instance._meta.model.objects.get(
                            pk=resolved_instance.pk
                        )
                    )
                self.store_mp_or_async(
                    resolved_instance,
                    source=source,
                    save=save,
                    force=force,
                    changed_only=second_check,
                )
                if old_resolved_instance:
                    setattr(
                        old_resolved_instance,
                        self.field_name,
                        getattr(resolved_instance, self.field_name),
                    )

            if second_check:
                return

            for dependent_mp, dependent_path in self.dependent_mps:
                for resolved_instance in resolve_instances(
                    instance, dependent_path
                ):
                    dependent_mp.store_mp_or_async(
                        resolved_instance, source=source
                    )

        if model == self.cls and not self.eventually_consistent:
            priority_connect(
                signals.pre_save,
                partial(change_receiver, signame='pre_save', save=False),
                sender=model,
            )
            if self.dbl_check_on_post_save:
                priority_connect(
                    signals.post_save,
                    partial(
                        change_receiver,
                        signame='post_save(2)',
                        second_check=True,
                    ),
                    sender=model,
                )
        else:
            priority_connect(
                signals.post_save,
                partial(change_receiver, signame='post_save'),
                sender=model,
            )

        if model != self.cls:
            priority_connect(
                signals.post_delete,
                partial(change_receiver, signame='post_delete'),
                sender=model,
            )
        else:
            priority_connect(
                signals.pre_delete, mark_pending_delete, sender=model
            )
            priority_connect(
                signals.post_delete, unmark_pending_delete, sender=model
            )


pending_delete = weakref.WeakValueDictionary()


def mark_pending_delete(instance, **kwargs):
    pending_delete[instance.pk] = instance


def unmark_pending_delete(instance, **kwargs):
    if instance.pk in pending_delete:
        del pending_delete[instance.pk]


def fmt(instance):
    if instance is None:
        return 'None'
    return '{}(pk={})'.format(instance._meta.model_name, instance.pk)


def resolve_instances(instance, path):
    if not path:
        yield instance
        return
    attr = path[0]
    path = path[1:]
    try:
        value = getattr(instance, attr)
    except ObjectDoesNotExist:
        value = None
    if value is None:
        return
    if isinstance(value, models.Model):
        for x in resolve_instances(value, path):
            yield x
    elif hasattr(value, 'all'):
        for singular in value.all():
            for x in resolve_instances(singular, path):
                yield x
    else:
        rollbar.report_message(
            'Unknown value in resolve_instance({}, {}): {}'.format(
                instance, path, value
            ),
            level='error',
        )


def parse_dependency(model, dependency):
    dependency_arr = dependency.split('.')
    path = []
    for attr_name in dependency_arr:
        yield model, attr_name, path[:]
        if len(path) == len(dependency_arr) - 1:
            return
        try:
            field = getattr(model, attr_name)
            relation_class_name = field.__class__.__name__
            # django.VERSION is a tuple. First item is major version
            if django.VERSION[0] == 1:
                if hasattr(field, 'field'):
                    # for ReverseSingleRelatedObjectDescriptor
                    is_reverse = relation_class_name.startswith('Reverse')
                    field = field.field
                    model = field.rel.related_model if is_reverse else field.rel.to
                    related_name = (
                        field.name if is_reverse else field.rel.related_name
                    )

                else:
                    model = field.related.model
                    related_name = field.related.field.name
            else:  # Django version is >= 2 - (Tested on Django 2.2.28, 3.2.22, 4.2.6)
                if relation_class_name == 'ForwardManyToOneDescriptor':
                    model = field.field.related_model
                    related_name = field.field.remote_field.related_name
                elif relation_class_name == 'ReverseManyToOneDescriptor':
                    model = field.field.model
                    related_name = field.field.name
                elif relation_class_name == 'ForwardOneToOneDescriptor':
                    model = field.field.related_model
                    related_name = field.field.remote_field.related_name
                elif relation_class_name == 'ReverseOneToOneDescriptor':
                    model = field.related.related_model
                    related_name = field.related.related_name
                elif relation_class_name == 'ManyToManyDescriptor':
                    if field.reverse:
                        model = field.field.related_model
                        related_name = field.field.remote_field.related_name
                    else:
                        model = field.field.model
                        related_name = field.field.name
                else:
                    raise TypeError('Unknown relation Descriptor: `{}`'.format(
                        relation_class_name
                    ))

            if not related_name or related_name == '+':
                raise Exception(
                    "Fields with no explicit related name aren't supported for now: {}".format(
                        field
                    )
                )

            path.insert(0, related_name)
        except Exception as e:
            raise Exception(
                'Failed to parse dependency {} on {}: {}'.format(
                    attr_name, model, e.message
                )
            )


def invalidate_for_instance(instance, mps, save=False):
    """Invalidates the Materialized Properties `mps` for this `instance

    Save immediately if `save == True`
    """
    if isinstance(mps, basestring):
        mps = [mps]
    for mp in mps:
        if isinstance(mp, basestring):
            model = instance._meta.model
            if model._meta.proxy:
                model = model._meta.proxy_for_model
            mp = registered_mps[model][mp]
        value = mp.get_real(instance)
        # rollbar.report_message(
        #     'setattr (invalidation) attr=%s, value=%s, instance=%s' % (
        #         mp.field_name,
        #         value,
        #         fmt(instance),
        #     ),
        #     level='info'
        # )
        mp.update_on_instance(instance, value, save=save)


def invalidate_for_instances(instances, mps, save=False):
    for instance in instances:
        invalidate_for_instance(instance, mps, save)


def default_dbg(x):
    print(x)


def default_stat(failed, total, not_set):
    print('failed {} of {}, not set on {}'.format(failed, total, not_set))


def default_exception(err, instance):
    print('Failed to evaluate for {}: {}'.format(fmt(instance), err))


class Throttler(object):
    def __init__(self, throttle_count):
        self.throttle_count = throttle_count
        self.counter = 0

    def throttle(self):
        if not self.throttle_count:
            return
        self.counter += 1
        if self.counter >= self.throttle_count:
            self.counter = 0
            time.sleep(1)


NOP_THROTTLER = Throttler(0)


def test_mp(
    it,
    model,
    mp,
    fix=False,
    log_dbg=default_dbg,
    log_stat=default_stat,
    log_err=default_exception,
    throttler=NOP_THROTTLER,
):
    if isinstance(mp, basestring):
        mp_name = mp
        mp = registered_mps[model].get(mp_name, None)
        if not mp:
            raise Exception(
                'Unknown mp {} on {}'.format(mp_name, model.__name__)
            )
    total = 0
    failed = 0
    not_set = 0
    attr_name = mp.field_name
    suspects = []

    pk_name = model._meta.pk.name
    if fix:
        for suspect_pk in suspects:
            try:
                instance = model.objects.get(**{pk_name: suspect_pk})
            except model.DoesNotExist:
                rollbar.report_message(
                    '{}(pk={}) did not exist in test_mp'.format(
                        model.__name__, suspect_pk
                    ),
                    level='warning',
                )
                continue
            throttler.throttle()
            try:
                invalidate_for_instance(instance, mp.name, save=True)
            except:
                rollbar.report_exc_info(
                    extra={
                        'message': 'Invalidation failed in test_mp',
                        'model': model.__name__,
                        'suspect_pk': suspect_pk,
                    }
                )
                continue

    log_stat(failed, total, not_set)


def extract_stack_safe():
    try:
        stack = '\n'.join(
            ('%s, %s, %s, %s' % x for x in traceback.extract_stack())
        )
    except:
        rollbar.report_exc_info(
            extra_data={'message': 'Failed to get stack trace for MP warning'}
        )
        stack = '<stack unknown>'
    return stack
