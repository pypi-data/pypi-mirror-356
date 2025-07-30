#
# Copyright (C) 2024 CESNET z.s.p.o.
#
# oarepo-requests is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.
#
"""Publish draft request type."""
from __future__ import annotations



from typing import TYPE_CHECKING, Any

import marshmallow as ma
from oarepo_runtime.i18n import lazy_gettext as _
from typing_extensions import override

from .publish_base import PublishRequestType

if TYPE_CHECKING:
    from flask_babel.speaklater import LazyString
    from flask_principal import Identity
    from invenio_drafts_resources.records import Record

from oarepo_requests.typing import EntityReference
from invenio_access.permissions import system_identity
from oarepo_runtime.datastreams.utils import get_record_service_for_record
from oarepo_requests.utils import get_requests_service_for_records_service
from invenio_requests.errors import CannotExecuteActionError
from invenio_requests.records.api import Request
class PublishDraftRequestType(PublishRequestType):
    """Publish draft request type."""

    type_id = "publish_draft"
    name = _("Publish draft")

    payload_schema = {
        **PublishRequestType.payload_schema,
        "version": ma.fields.Str(),
    }

    form = {
        "field": "version",
        "ui_widget": "Input",
        "props": {
            "label": _("Resource version"),
            "placeholder": _("Write down the version (first, second…)."),
            "required": False,
        },
    }

    @classmethod
    def is_applicable_to(
        cls, identity: Identity, topic: Record, *args: Any, **kwargs: Any
    ) -> bool:
        """Check if the request type is applicable to the topic."""
        if cls.topic_type(topic) != "initial":
            return False

        return super().is_applicable_to(identity, topic, *args, **kwargs)

    @override
    def stateful_name(
        self,
        identity: Identity,
        *,
        topic: Record,
        request: Request | None = None,
        **kwargs: Any,
    ) -> str | LazyString:
        """Return the stateful name of the request."""
        return self.string_by_state(
            identity=identity,
            topic=topic,
            request=request,
            create=_("Submit for review"),
            create_autoapproved=_("Publish draft"),
            submit=_("Submit for review"),
            submitted_receiver=_("Review and publish draft"),
            submitted_creator=_("Draft submitted for review"),
            submitted_others=_("Draft submitted for review"),
            accepted=_("Draft published"),
            declined=_("Draft publication declined"),
            cancelled=_("Draft publication cancelled"),
            created=_("Submit for review"),
        )

    @override
    def stateful_description(
        self,
        identity: Identity,
        *,
        topic: Record,
        request: Request | None = None,
        **kwargs: Any,
    ) -> str | LazyString:
        """Return the stateful description of the request."""
        return self.string_by_state(
            identity=identity,
            topic=topic,
            request=request,
            create=_(
                "By submitting the draft for review you are requesting the publication of the draft. "
                "The draft will become locked and no further changes will be possible until the request "
                "is accepted or declined. You will be notified about the decision by email."
            ),
            create_autoapproved=_(
                "Click to immediately publish the draft. "
                "The draft will be a subject to embargo as requested in the side panel. "
                "Note: The action is irreversible."
            ),
            submit=_(
                "Submit for review. After submitting the draft for review, "
                "it will be locked and no further modifications will be possible."
            ),
            submitted_receiver=_(
                "The draft has been submitted for review. "
                "You can now accept or decline the request."
            ),
            submitted_creator=_(
                "The draft has been submitted for review. "
                "It is now locked and no further changes are possible. "
                "You will be notified about the decision by email."
            ),
            submitted_others=_("The draft has been submitted for review. "),
            accepted=_("The draft has been published. "),
            declined=_("Publication of the draft has been declined."),
            cancelled=_("The draft has been cancelled. "),
            created=_("Waiting for finishing the draft publication request."),
        )

    def can_create(
            self,
            identity: Identity,
            data: dict,
            receiver: EntityReference,
            topic: Record,
            creator: EntityReference,
            *args: Any,
            **kwargs: Any,
    ) -> None:
        """Check if the request can be created."""
        topic_service = get_record_service_for_record(topic)

        request_service = get_requests_service_for_records_service(topic_service) #, extra_filters = TermQuery(status="open")
        requests = request_service.search_requests_for_draft(system_identity,  topic.pid.pid_value)

        for result in requests._results:
            if result.is_open and result.type != "approve_draft":
                # note: we can not use solely the result.is_open because changes may not be committed yet
                # to opensearch index. That's why we need to get the record from DB and re-check.
                if Request.get_record(result.uuid)["status"] in ("submitted", "created"):
                    raise CannotExecuteActionError(str(self.name), reason=_("All open requests need to be closed."))
        super().can_create(identity, data, receiver, topic, creator, *args, **kwargs)

