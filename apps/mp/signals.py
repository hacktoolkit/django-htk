# Python Standard Library Imports
from __future__ import absolute_import

# Django Imports
from django.apps import apps
from django.dispatch.dispatcher import _make_id


# This function similar to django.dispatch.dispatcher.Signal::connect()
def priority_connect(self, receiver, sender=None, children=True):
    if sender and children:
        if sender._meta.abstract:
            for child in apps.get_models():
                if issubclass(child, sender):
                    priority_connect(self, receiver, child, children=False)
            return

    lookup_key = (_make_id(receiver), _make_id(sender))

    with self.lock:
        self._clear_dead_receivers()
        for r_key, _ in self.receivers:
            if r_key == lookup_key:
                break
        else:
            # Adding priority receiver to beginning of the list
            self.receivers.insert(0, (lookup_key, receiver))
        self.sender_receivers_cache.clear()
