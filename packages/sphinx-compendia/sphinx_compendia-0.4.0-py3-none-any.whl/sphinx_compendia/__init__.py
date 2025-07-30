"""
Top-level module.

This is **not** an API.
"""

from __future__ import annotations

from collections import defaultdict
from importlib.metadata import PackageNotFoundError, version
from typing import TYPE_CHECKING

from sphinx.domains import Index as BaseIndex
from sphinx.domains import ObjType
from sphinx.errors import SphinxError
from sphinx.util.logging import getLogger

from sphinx_compendia.domain import BackrefsIndexer, Domain
from sphinx_compendia.i18n import t_

if TYPE_CHECKING:
    from collections.abc import Iterable

    from sphinx.application import Sphinx
    from sphinx.directives import ObjectDescription
    from sphinx.roles import XRefRole


_package_name = "sphinx_compendia"

try:
    __version__ = str(version(_package_name))
except PackageNotFoundError:
    # package is not installed
    __version__ = "(please install the package)"


log = getLogger(__name__)


class SphinxCompendiaError(SphinxError):
    category = "Sphinx-Compendia error"


class Constituent:
    objtype: str
    directive_aliaseses: list[str]
    xrefrole_aliases: list[str]
    directive_class: type[ObjectDescription[str]]
    xrefrole_class: type[XRefRole]
    admissible_parent_objtypes: bool | Iterable[str] | None

    def __init__(  # noqa: PLR0913 # This API needs many paramters
        self,
        objtype: str,
        *,
        xrefrole_aliases: list[str] | None = None,
        directive_aliases: list[str] | None = None,
        xrefrole_class: type[XRefRole] | None = None,
        directive_class: type[ObjectDescription[str]] | None = None,
        admissible_parent_objtypes: bool | Iterable[str] = True,
        **objtype_attrs: None,
    ):
        """
        Provide fine-grained customization for the consituents of a topic.

        Args:
            objtype: In Sphinx, an object type (``objtype``) is a short
                string that identify a kind of documented thing. For instance,
                in the Python domain, a documented class has the ``class``
                objtype.
                |project| uses this string to generate roles and directives
                for your constituent.  It is usually made of lower-case
                letters.
            xrefrole_aliases:
                When cross-referencing a documented constituent, you can
                always use the main generated role
                (``:{topic}:{objtype}:`{target}```).
                This parameters enable to also generate alterative roles,
                which might be useful to shorten the cross-referencing syntax.
                As an example, for a ``location`` constituent, one may
                provide the ``place`` and ``loc`` aliases.
            directive_aliases:
                Directive allias can also be provided.  They all will produce
                the same documented constituent object types.
            directive_class:
                You can change |project| behavior by providing you own
                directive sub-class. See
                :class:`sphinx_compendia.markup.ConstituentDescription`
                for more information about how to efficiently customize
                the directives.
            xrefrole_class:
                You can also provide your own cross-referencing role
                implementation here. See
                :class:`sphinx_compendia.markup.ConstituentReference` for details.
            admissible_parent_objtypes:
                Indicate whether this constituent has any meaning when defined
                within an other constituent. When ``True`` (the default),
                it is ok to use directives under any other constituent directive
                for a give topic.  When a list of strings, only support these
                objtypes as parent directives. When ``False``, forbid nesting.
            **objtype_attrs:
                Undocumented. Reserved for future use.

        """
        from sphinx_compendia.markup import (  # noqa: PLC0415 # Prevent circular import as this is only there to provide a nice API
            ConstituentDescription,
            ConstituentReference,
        )

        self.objtype = objtype.lower()
        self.xrefrole_aliases = xrefrole_aliases if xrefrole_aliases else []
        self.directive_aliases = directive_aliases if directive_aliases else []
        self.directive_class = (
            directive_class if directive_class else ConstituentDescription
        )
        self.xrefrole_class = xrefrole_class if xrefrole_class else ConstituentReference
        self.admissible_parent_objtypes = admissible_parent_objtypes
        self.attrs = objtype_attrs


def make_compendium(  # noqa: PLR0913 # This API needs many paramters
    name: str,
    constituents: Iterable[str | Constituent],
    *,
    display_name: str | None = None,
    index_name: str | None = None,
    index_localname: str | None = None,
    index_shortname: str | None = None,
    index_class: type[BaseIndex] | None = None,
    domain_class: type[Domain] | None = None,
    namespace_separator: str = ".",
    case_sensitive_resolve: bool = True,
    log_unreferenced_signatures: bool = False,
    app: Sphinx | None = None,
) -> type[Domain]:
    """
    Create and optionally register a new topic.

    Args:
        name:
            The name of the topic, which will end up being the generated
            domain name.  All directives and roles uses will need this string
            prepended to it by default.
        constituents:
            Things documented in this topic.  When these are strings, it
            uses all the :class:`sphinx_compendia.Constituent` default behaviors.
            Providing no constituents will result in a useless topic.
        display_name:
            A longer, more descriptive name, used in messages (logs). It
            defaults to the ``name`` with some capital letters.
        index_name:
            An identifier for the generated domain index. It is used when
            generating the index files names. It is also used for a hyperlink
            target for the index. Therefore, users can refer the index
            page using :rst:role:`ref` role and a string which is the combined
            domain name and :paramref:`.index_name`
            (e.g. ``:ref:`world-characterindex```).
            It defaults to ``index``.
        index_localname:
            The section title for the index. It defaults to

            .. code-block:: python

                f"{name.title()} Index"

            Where ``name`` is the topic (domain) name (i.e. :paramref:`.name`).
        index_shortname:
            A short name for the index, for use in the relation bar in HTML
            output.  Can be empty to disable entries in the relation bar.
            It defaults to the same as :paramref:`.index_localname`.
        index_class:
            You can provide your own index implementation here.
        domain_class:
            You can provide your own domain implementation here.
        namespace_separator:
            String to separate part of nested objects under namespaces.
        case_sensitive_resolve:
            Whether references to objects should be case-sensitive.
        log_unreferenced_signatures:
            Whether signature without references should be logged as 'INFO'.
        app:
            The Sphinx application object.  When provided, the topic is
            automatically registered.  You can also register the generated
            topic manually using the
            :meth:`sphinx.application.Sphinx.add_domain` method:

            .. code-block:: python

                topic = make_topic("rule", "House Rules",
                                   ["skill", "spell"])
                app.add_domain(topic)

    Returns:
        A domain class.

    """
    from sphinx_compendia.index import (  # noqa: PLC0415 # In order to provide a clean API
        Index,
    )

    display_name = display_name or name.title()

    index_class = index_class or Index

    generated_index_class = type(
        f"{name.title()}Index",
        (index_class,),
        {
            "name": index_name or "index",
            "localname": index_localname or f"{name.title()} Index",
            "shortname": index_shortname or f"{name.title()} Index",
        },
    )

    indices = [generated_index_class]

    object_types = {}
    directives = {}
    roles = {}
    temp_admissible_parent_objtypes = {}

    for constituent in constituents:
        if not isinstance(constituent, Constituent):
            constituent_object = Constituent(constituent)
        else:
            constituent_object = constituent

        object_types[constituent_object.objtype] = ObjType(
            t_(constituent_object.objtype),
            *[constituent_object.objtype, *constituent_object.xrefrole_aliases],
            **constituent_object.attrs,
        )

        directive_class = type(
            f"{constituent_object.objtype.title()}{constituent_object.directive_class.__name__}",
            (constituent_object.directive_class,),
            {
                "constituent_objtype": constituent_object.objtype,
                "namespace_separator": namespace_separator,
            },
        )

        for directive_aliases in constituent_object.directive_aliases:
            directives[directive_aliases] = directive_class
        directives[constituent_object.objtype] = directive_class

        role_instance = constituent_object.xrefrole_class()
        for xrefrole_alias in constituent_object.xrefrole_aliases:
            roles[xrefrole_alias] = role_instance
        roles[constituent_object.objtype] = role_instance

        temp_admissible_parent_objtypes[constituent_object.objtype] = (
            constituent_object.admissible_parent_objtypes
        )

    admissible_parent_objtypes: dict[str, set[str]] = defaultdict(set)
    for child_type, rule in temp_admissible_parent_objtypes.items():
        if rule is True:
            admissible_parent_objtypes[child_type].update(object_types.keys())
        elif rule is False:
            admissible_parent_objtypes[child_type].clear()
        else:
            admissible_parent_objtypes[child_type] = set(rule if rule else [])

    domain_class = domain_class or Domain

    generated_domain_class = type(
        f"{name.title()}Domain",
        (domain_class,),
        {
            "name": name,
            "label": display_name,
            "directives": directives,
            "roles": roles,
            "indices": indices,
            "initial_data": domain_class.make_initial_data(
                object_types.keys(),
                admissible_parent_objtypes,
                namespace_separator=namespace_separator,
                case_sensitive_resolve=case_sensitive_resolve,
            ),
            "object_types": object_types,
        },
    )

    backrefs_indexer_transform_cls = type(
        f"{name.title()}BackrefsIndexer",
        (BackrefsIndexer,),
        {"index_class": generated_index_class, "domain_name": name},
    )

    if app:
        app.add_domain(generated_domain_class)
        app.add_post_transform(backrefs_indexer_transform_cls)
        if log_unreferenced_signatures:
            app.connect(
                "build-finished",
                generated_domain_class.find_unreferenced_objects  # type: ignore[attr-defined]
            )

    return generated_domain_class
