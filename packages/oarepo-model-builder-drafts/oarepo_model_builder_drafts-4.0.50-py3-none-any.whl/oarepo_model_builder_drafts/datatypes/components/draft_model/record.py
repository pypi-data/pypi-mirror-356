from oarepo_model_builder.datatypes import DataType, ModelDataType
from oarepo_model_builder.datatypes.components import RecordModelComponent
from oarepo_model_builder.datatypes.components.model.utils import set_default
from oarepo_model_builder.datatypes.components.facets import FacetDefinition
from oarepo_model_builder.utils.python_name import Import


class DraftRecordModelComponent(RecordModelComponent):
    eligible_datatypes = [ModelDataType]
    dependency_remap = RecordModelComponent

    def process_facets(self, datatype, section, **__kwargs):

        if datatype.root.profile not in ("record", "draft"):
            return section
        facets = section.config.setdefault("facets", [])
        facets.extend([
        FacetDefinition(
            path="record_status",
            dot_path="record_status",
            searchable=True,
            imports=[
                Import(
                    import_path="invenio_records_resources.services.records.facets.TermsFacet",
                    alias=None,
                )
            ],
            facet_groups={"_default": 100000},
            facet=None,
            field="TermsFacet(field='record_status', label =_('record_status'))",
        ),

        FacetDefinition(
            path="has_draft",
            dot_path="has_draft",
            searchable=True,
            imports=[
                Import(
                    import_path="invenio_records_resources.services.records.facets.TermsFacet",
                    alias=None,
                )
            ],
            facet_groups={"_default": 100000},
            facet=None,
            field="TermsFacet(field='has_draft', label =_('has_draft'))",
        ),

        FacetDefinition(
            path="expires_at",
            dot_path="expires_at",
            searchable=True,
            imports=[
                Import(
                    import_path="oarepo_runtime.services.facets.date.DateTimeFacet",
                    alias=None,
                )
            ],
            facet_groups={"_default": 100000},
            facet=None,
            field="DateTimeFacet(field='expires_at', label=_('expires_at.label'))",
        ),
        FacetDefinition(
            path="fork_version_id",
            dot_path="fork_version_id",
            searchable=True,
            imports=[
                Import(
                    import_path="invenio_records_resources.services.records.facets.TermsFacet",
                    alias=None,
                )
            ],
            facet_groups={"_default": 100000},
            facet=None,
            field="TermsFacet(field='fork_version_id', label=_('fork_version_id.label'))",
        ),
    ])
        return section


    def before_model_prepare(self, datatype, *, context, **kwargs):
        if datatype.root.profile not in {"record", "draft"}:
            return
        record = set_default(datatype, "record", {})

        if datatype.root.profile == "draft":
            published_record_datatype: DataType = context["published_record"]
            record.setdefault(
                "base-classes",
                ["invenio_drafts_resources.records.api.Draft{InvenioDraft}"],
            )
            record.setdefault(
                "imports",
                [],
            )
            extra_code = datatype.model.get("extra-code", "")
            record.setdefault("extra-code", extra_code)
            is_record_preset = record.get("class", None)

            # get draft record fields
            draft_record_fields = record.setdefault("fields", {})

            # for each published field, add it to the draft record fields if it is not already there
            published_record_fields = published_record_datatype.definition["record"][
                "fields"
            ]
            for (
                published_field_name,
                published_field,
            ) in published_record_fields.items():
                if published_field_name not in draft_record_fields:
                    draft_record_fields[published_field_name] = published_field

            # null value is used to remove the field from the draft record
            # even if it is present in the published record
            draft_record_fields = {k: v for k, v in draft_record_fields.items() if v}

            super().before_model_prepare(datatype, context=context, **kwargs)
            if not is_record_preset and record["class"][-6:] == "Record":
                record["class"] = record["class"][:-6]
        if datatype.root.profile == "record":
            record.setdefault(
                "base-classes",
                ["invenio_drafts_resources.records.api.Record{InvenioRecord}"],
            )
            super().before_model_prepare(datatype, context=context, **kwargs)
