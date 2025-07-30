from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING, NamedTuple, Self, TypeVar

from sphinx.util.logging import getLogger

from sphinx_compendia.i18n import t__

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable, Iterator

    from sphinx import addnodes

    from sphinx_compendia.sphinxapi import SphinxDomainObjectDescription

log = getLogger(__name__)


class CompendiumObject(NamedTuple):
    """
    Store documented domain objects in a Sphinx domain data.
    """

    object_id: str
    """
    Identify this object.
    """

    objtype: str
    """
    Constituent typename this object represents.
    """

    objtype_alias: str
    """
    The directive name this constituent was documented with.
    """

    primary_display_name: str
    """
    Human readable name for this object, the first signature from its directive.
    """


TD = TypeVar("TD", bound="CompendiumData")


class Ref(NamedTuple):
    dispname: str
    docname: str
    anchor: str


class CompendiumData(NamedTuple):
    object_descriptions: dict[str, list[SphinxDomainObjectDescription]]
    compendium_objects: dict[str, CompendiumObject]
    objtype_selectors: dict[str, dict[str, set[str]]]
    signature_references: dict[SphinxDomainObjectDescription, list[Ref]]
    admissible_parent_objtypes: dict[str, set[str]]
    children: dict[str, set[str]]
    namespaces: dict[tuple[str, str], str]
    namespace_separator: str = "."
    resolve_case_sensitivity: bool = True

    @classmethod
    def initial_data(
        cls,
        objtypes: Iterable[str],
        admissible_parent_objtypes: dict[str, set[str]],
        *,
        namespace_separator: str = ".",
        case_sensitive_resolve: bool = True,
    ) -> Self:
        return cls(
            defaultdict(list),
            {},
            {objtype: defaultdict(set) for objtype in objtypes},
            defaultdict(list),
            admissible_parent_objtypes,
            defaultdict(set),
            {},
            namespace_separator,
            case_sensitive_resolve,
        )

    def add_object(  # noqa: PLR0913 # A lot of arguments here
        self,
        objtype: str,
        objtype_alias: str,
        object_id: str,
        object_description: SphinxDomainObjectDescription,
        namespace: list[str],
        signode: addnodes.desc_signature,
    ) -> None:
        full_namespace = [*namespace, object_description.dispname]

        if object_id not in self.compendium_objects:
            new_namespace = self.namespace_separator.join(full_namespace)
            if (objtype, new_namespace) in self.namespaces:
                log.warning(
                    t__("object with namespace %s already documented"),
                    new_namespace,
                    location=signode,
                )
            self.compendium_objects[object_id] = CompendiumObject(
                object_id, objtype, objtype_alias, object_description.dispname
            )
            self.namespaces[(objtype, new_namespace)] = object_id

        if len(full_namespace) > 1:
            for parent_compendium_object, _ in self.find(
                self.admissible_parent_objtypes[objtype],
                self.namespace_separator.join(full_namespace[0:-1]),
            ):
                self.children[parent_compendium_object.object_id].add(object_id)

        self.object_descriptions[object_id].append(object_description)

        selector = object_description.dispname
        selector = selector if self.resolve_case_sensitivity else selector.lower()

        self.objtype_selectors[objtype][selector].add(object_id)

    def add_backref(
        self,
        object_description: SphinxDomainObjectDescription,
        docname: str,
        anchor: str,
        display_name: str,
    ) -> None:
        self.signature_references[object_description].append(
            Ref(display_name, docname, anchor)
        )

    def find_object_descriptions(
        self,
    ) -> Iterable[SphinxDomainObjectDescription]:
        for object_descriptions in self.object_descriptions.values():
            yield from object_descriptions

    def find(
        self, objtypes: Iterable[str], target: str
    ) -> Iterator[tuple[CompendiumObject, SphinxDomainObjectDescription]]:
        target = target if self.resolve_case_sensitivity else target.lower()

        *_, terminal_selector = target.split(self.namespace_separator)

        for compendium_object in self._find_compendium_objects(objtypes, target):
            for object_description in self.object_descriptions[
                compendium_object.object_id
            ]:
                candidate_label = (
                    object_description.dispname
                    if self.resolve_case_sensitivity
                    else object_description.dispname.lower()
                )
                if terminal_selector == candidate_label:
                    yield compendium_object, object_description

    def _find_compendium_objects(
        self, objtypes: Iterable[str], target: str
    ) -> Iterable[CompendiumObject]:
        *parent_selectors, terminal_selector = target.split(self.namespace_separator)

        filter_ = self._make_filter(parent_selectors)

        for objtype in objtypes:
            for object_id in self.objtype_selectors[objtype][terminal_selector]:
                compendium_object = self.compendium_objects[object_id]
                if not filter_(compendium_object):
                    continue
                yield compendium_object

    def _make_filter(
        self, parent_selectors: list[str]
    ) -> Callable[[CompendiumObject], bool]:
        if parent_selectors:
            _filter = self._make_parent_filter(parent_selectors)

        else:

            def _filter(compendium_object: CompendiumObject) -> bool:  # noqa: ARG001
                return True

        return _filter

    def _make_parent_filter(
        self, parent_selectors: list[str]
    ) -> Callable[[CompendiumObject], bool]:
        def _filter(compendium_object: CompendiumObject) -> bool:
            parent_objtypes = self.objtype_selectors.keys()
            for parent_compendium_object, _ in self.find(
                parent_objtypes, self.namespace_separator.join(parent_selectors)
            ):
                if (
                    compendium_object.object_id
                    in self.children[parent_compendium_object.object_id]
                ):
                    return True
            return False

        return _filter
