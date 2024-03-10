# Changelog

# 2.0 (WIP)

- Overall test and code refactor.
- Documention now done with MKDocs.
- Timeline in Admin change form now supports delays of days and hours, instead of just minutes.
- *Backwards incompatible:* Removed undocumented ``Event.objects.purge()`` queryset method.
- *Backwards incompatible:* The list of event types defined in the app config is now
  set via Python dataclasses rather than a dictionary. The migration is simple.

  ```python
  event_types = {
      "info": {
          "label": _("Info"),
          "color": None,
          "bgcolor": None,
      },
      "warning": {
          "label": _("Warning"),
          "color": None,
          "bgcolor": None,
      },
      ...
  ```

  The dictionary is now a ``EventTypeList`` of ``EventType`` dataclasses:

  ```python
  from eventlog.datastructures import EventType, EventTypeList
  
  # List of event types to be used in events. A list of `EventType` classes
  event_types = EventTypeList(
      EventType(name="info", label=_("Info")),
      EventType(name="warning", label=_("Warning")),
      EventType(name="error", label=_("Error"), color="red"),
      EventType(name="critical", label=_("Critical"), color="white", bgcolor="red"),
  )
  ```
  
  You will only need to do this change if you've earlier overridden the event_type property.

## 1.5 (2024-03-08)

- Event can have optional, JSON serializable data attached.
- Fixed dark mode colors.
- Various Admin UI improvements.

## 1.4 (2024-03-05)

- Event groups can now have arbitrary names instead of UUIDs.
- Event comments is a textfield.
- Fixed potential migration warnings around AutoFields.

## 1.3 (2023-10-04)

- Python 3.12 compatibility
- Django 5.0 support
- Type Annotations

## 1.2 (2023-04-28)

- Python 3.7 to 3.11 compatibility
- Django 3.2 to 4.2 support

## 1.1 (2018-05-11)

- Added ability to manually set a group id to make an EventGroup object
  reusable through threads.

## 1.0 (2018-02-13)

- Production ready 1.0 release.
- The details Admin view now displays all events of the group with an
  annotated delay, so you can see the progress of the group.

## 0.9 (2018-02-13)

- Initial release.
- Django 1.8 to 2.0 compatibility.
- Python 2.7 to 3.6 compatibility.

