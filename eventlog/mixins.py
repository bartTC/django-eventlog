#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from django.utils.html import format_html

from .events import EventGroup



class LoggerMixin:
    """
    you can inherit this logger mixin to use logger attribute

    e.g.
        class Apply(LoggerMixin, models.Model):
            ...
        apply = Apply.objects.create()
        apply.logger.info("%s create the apply", request.user)
    """

    def get_group_id(self) -> str:
        return f"{self.__class__.__module__}{self.__class__.__name__}-{self.pk}"

    @property
    def logger(self) -> EventGroup:
        if hasattr(self, "_logger"):
            return self._logger
        event_log = EventGroup(group_id = self.get_group_id())
        self._logger = event_log
        return self._logger


class LoggerAdminMixin:
    """
    You can inherit LoggerAdminMixin in your admin class so that you can view loggers related to the specific object

    e.g.

        @admin.register(Tag)
        class YouModelAdmin(LoggerAdminMixin, admin.ModelAdmin):
            list_display = ["id", "logger"]  # add logger in list_display

    """

    def logger(self, obj):
        group_id = obj.get_group_id()
        return format_html(f'<a href="/admin/eventlog/event/?group={group_id}">view logs</a>')
