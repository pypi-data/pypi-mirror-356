from __future__ import annotations

import sys
from collections import defaultdict
from typing import TYPE_CHECKING, Any, TypeVar

from sphinx.domains import Domain as _Domain
from sphinx.domains import Index, IndexEntry
from sphinx.transforms.post_transforms import ReferencesResolver, SphinxPostTransform
from sphinx.util.logging import getLogger
from sphinx.util.nodes import make_refnode

from sphinx_compendia.i18n import t__
from sphinx_compendia.sphinxapi import SphinxDomainObjectDescription
from sphinx_compendia.store import CompendiumData, CompendiumObject, Ref

if TYPE_CHECKING:
    from collections.abc import Iterable

    from docutils.nodes import Element, Node, reference
    from docutils.parsers.rst import Directive
    from sphinx import addnodes
    from sphinx.application import Sphinx
    from sphinx.builders import Builder
    from sphinx.environment import BuildEnvironment
    from sphinx.roles import XRefRole
    from sphinx.util.typing import RoleFunction


if TYPE_CHECKING or sys.version_info < (3, 8, 0):
    from typing_extensions import TypedDict
else:
    from typing import TypedDict

log = getLogger(__name__)


D = TypeVar("D", bound="Domain")


class DomainData(TypedDict, total=False):
    version: int
    topic_data: CompendiumData


class Domain(_Domain):
    """
    Tie together  roles, directives, and indices, among other things.
    """

    name: str
    label: str
    roles: dict[str, RoleFunction | XRefRole]
    directives: dict[str, type[Directive]]
    indices: list[type[Index]]
    initial_data: DomainData  # type: ignore[assignment] # We control initial data, let's hope for the best.

    @classmethod
    def make_initial_data(
        cls,
        objtypes: Iterable[str],
        admissible_parent_objtypes: dict[str, set[str]],
        *,
        namespace_separator: str = ".",
        case_sensitive_resolve: bool = True,
    ) -> DomainData:
        return {
            "topic_data": CompendiumData.initial_data(
                objtypes,
                admissible_parent_objtypes,
                namespace_separator=namespace_separator,
                case_sensitive_resolve=case_sensitive_resolve,
            )
        }

    @property
    def _store(self) -> CompendiumData:
        guard = self.data["topic_data"]
        if not isinstance(guard, CompendiumData):
            raise TypeError(guard)

        return guard

    @property
    def resolve_case_sensitivity(self) -> bool:
        return self._store.resolve_case_sensitivity

    def note_constituent_signature(  # noqa: PLR0913 # Too many arguments
        self,
        objtype: str,
        objtype_alias: str,
        object_id: str,
        anchor: str,
        signature: str,
        namespace: list[str],
        signode: addnodes.desc_signature,
    ) -> None:
        object_description = SphinxDomainObjectDescription(
            anchor,
            signature,
            objtype,
            self.env.docname,
            anchor,
            1,
        )
        self._store.add_object(
            objtype,
            objtype_alias,
            object_id,
            object_description,
            namespace,
            signode,
        )

    def get_compendium_objects(
        self, docnames: Iterable[str] | None = None
    ) -> dict[CompendiumObject, list[SphinxDomainObjectDescription]]:
        result = {}
        for compendium_object in self._store.compendium_objects.values():
            object_descriptions = self._store.object_descriptions[
                compendium_object.object_id
            ]
            if docnames is not None:
                result[compendium_object] = [
                    object_description
                    for object_description in object_descriptions
                    if object_description.docname in docnames
                ]
            else:
                result[compendium_object] = self._store.object_descriptions[
                    compendium_object.object_id
                ]
        return result

    def get_refs(self, object_description: SphinxDomainObjectDescription) -> list[Ref]:
        return self._store.signature_references[object_description]

    def get_objects(self) -> Iterable[SphinxDomainObjectDescription]:
        """
        Return an iterable of "object descriptions".

        See Also:
             Parent method :meth:`sphinx.domains.Domain.get_objects`.

        Returns:
            Object descriptions are tuples with six items.
            See :class:`.sphinxapi.SphinxDomainObjectDescription`.

        """
        yield from self._store.find_object_descriptions()

    def resolve_xref(  # noqa: PLR0913 # Too many arguments
        self,
        env: BuildEnvironment,  # noqa: ARG002 # This method is inherited
        fromdocname: str,
        builder: Builder,
        reference_type: str,
        target: str,
        node: addnodes.pending_xref,
        contnode: Element,
    ) -> reference | None:
        """
        Resolve the pending_xref *node* with the given *reference_type* and *target*.

        Args:
            env:
                Current Sphinx build environment.
            fromdocname:
                Document name where the cross-reference was used.
            builder:
                Current Sphinx builder.
            reference_type:
                Reference type name. Basically, the reference role name.
            target:
                Looked up object identifier.
            node:
                Document node for the xref.
            contnode:
                The markup content of the cross-reference.

        If no resolution can be found, ``None`` can be returned;
        the xref node will then given to the ``missing-reference`` event,
        and if that yields no resolution, replaced by contnode.

        Returns:
            A reference node or None if no reference could be resolved.

        """
        resolved = self._resolve_xref(target, reference_type)

        if not resolved:
            return None

        if len(resolved) > 1:
            candidates = " or ".join(
                f":{self._make_rolename(object_description)}:`{target}` "
                f"from {object_description.docname}"
                for _, object_description in resolved
            )
            log.warning(
                t__(
                    "more than one target found for "
                    "'%s' cross-reference %r: could be %s"
                ),
                reference_type,
                target,
                candidates,
                location=node,
            )

        compendium_object, object_description = resolved[0]
        refnode = self._make_refnode(builder, contnode, fromdocname, object_description)
        self._backref_xref(node, object_description)
        return refnode

    def resolve_any_xref(  # noqa: PLR0913 # This method is inherited
        self,
        env: BuildEnvironment,  # noqa: ARG002 # This method is inherited
        fromdocname: str,
        builder: Builder,
        target: str,
        node: addnodes.pending_xref,  # noqa: ARG002 # This method is inherited
        contnode: Element,
    ) -> list[tuple[str, reference]]:
        """
        Resolve the pending_xref *node* with the given *target*.

        Args:
            env:
                Current Sphinx build environment.
            fromdocname:
                Document name where the cross-reference was used.
            builder:
                Current Sphinx builder.
            target:
                Looked up object identifier.
            node:
                Document node for the xref.
            contnode:
                The markup content of the cross-reference.

        Returns:
            The method must return a list (potentially empty) of tuples
            ``("domain:role", newnode)``, where ``"domain:role"`` is the
            name of a role that could have created the same reference,
            e.g. ``'py:func'``. ``newnode`` is what :meth:`resolve_xref`
            would return.

        """
        return [
            (
                self._make_rolename(object_description),
                self._make_refnode(builder, contnode, fromdocname, object_description),
            )
            for _, object_description in self._resolve_xref(target)
        ]

    def _backref_xref(
        self,
        node: addnodes.pending_xref,
        object_description: SphinxDomainObjectDescription,
    ) -> None:
        self._store.add_backref(
            object_description, self.env.docname, node["ids"][0], node.astext()
        )

    def _resolve_xref(
        self,
        target: str,
        reference_type: str | None = None,
    ) -> list[tuple[CompendiumObject, SphinxDomainObjectDescription]]:
        try:
            objtypes = list(
                self.objtypes_for_role(reference_type, [])
                if reference_type is not None
                else self.object_types.keys()
            )
            return list(self._store.find(objtypes, target))
        except KeyError:
            return []

    def _make_refnode(
        self,
        builder: Builder,
        contnode: Node,
        fromdocname: str,
        obj_description: SphinxDomainObjectDescription,
    ) -> reference:
        return make_refnode(
            builder,
            fromdocname,
            obj_description.docname,
            obj_description.anchor,
            contnode,
            obj_description.dispname,
        )

    def _make_rolename(self, object_description: SphinxDomainObjectDescription) -> str:
        return f"{self.name}:{self.role_for_objtype(object_description.type)}"

    @classmethod
    def find_unreferenced_objects(cls, app: Sphinx, _: Exception) -> None:
        domain = app.env.domains[cls.name]
        grouped: dict[
            CompendiumObject, list[SphinxDomainObjectDescription]
        ] = defaultdict(
            list
        )
        compendium_objects = domain.get_compendium_objects()  # type: ignore[attr-defined]
        for compendium_object, objects in compendium_objects.items():
            for object_description in objects:
                references = domain.get_refs(object_description)  # type: ignore[attr-defined]
                if not references:
                    grouped[compendium_object].append(
                        object_description
                    )

        for compendium_object, object_descriptions in grouped.items():
            object_as_str = (
                f":{compendium_object.objtype_alias}:"
                f"`{compendium_object.primary_display_name}`"
            )
            unreferenced = [o.dispname for o in object_descriptions]
            log.info(
                "Documented object %s as unreferenced "
                "signatures that could be removed: %s.",
                object_as_str, unreferenced
            )


class BackrefsIndexer(SphinxPostTransform):
    default_priority = ReferencesResolver.default_priority + 1

    index_class: type[Index]
    domain_name: str

    def is_supported(self) -> bool:
        return super().is_supported() and hasattr(self.app.builder, "domain_indices")

    def run(self, **kwargs: Any) -> None:  # noqa: ANN401,ARG002 # This method is inherited
        """
        Regenerate domain index entries for a document.

        This happens near the end of processing a given document. This class
        need to be extended by providing a domain name and index class to
        be able to recreate the index instance and regenerate the entries.

        See Also:
            It is extended in the compendia creation process. See
            :func:`sphinx_compendia.make_compendium`.

        Notes:
            This is a workaround for a limitation in Sphinx API: the domain
            indices are generated *before* cross-references are resolved.
            See :ref:`known-issues` for details.

        Args:
            **kwargs: We don't use these arguments.

        """
        domain_indices = getattr(self.app.builder, "domain_indices", [])

        # Find the domain index we are rebuilding
        index_number = 0
        for (
            _index_name,
            index_class,
            _original_entries_for_char,
            _collapse,
        ) in domain_indices:
            if index_class == self.index_class:
                break
            index_number += 1
        else:
            return

        index = index_class(self.env.domains[self.domain_name])

        # Generate again the index
        regenerated, _ = index.generate([self.env.docname])

        new_entries_for_char = self._replace_entries(
            _original_entries_for_char, regenerated
        )

        # Change the dict into the sorted list of tuples expected
        resorted = sorted(new_entries_for_char.items(), key=index.sort_key)

        # Replace the regenerated index
        domain_indices[index_number] = (
            _index_name,
            index_class,
            resorted,
            _collapse,
        )

    def _replace_entries(
        self,
        original_entries_for_char: list[tuple[str, list[IndexEntry]]],
        regenerated: list[tuple[str, list[IndexEntry]]],
    ) -> dict[str, list[IndexEntry]]:
        # Use a dict instead of list of tuples expected
        new_entries_for_char = defaultdict(list, regenerated)
        current_docname = self.env.docname
        # Merge with entries not in this docname
        for character, entries in original_entries_for_char:
            new_entries_for_char[character].extend(
                entry for entry in entries if current_docname != entry.docname
            )
        return new_entries_for_char
