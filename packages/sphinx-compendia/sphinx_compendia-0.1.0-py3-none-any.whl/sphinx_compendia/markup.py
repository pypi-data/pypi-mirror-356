from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar, Generic, TypeVar

from docutils import nodes
from sphinx import addnodes
from sphinx.directives import ObjectDescription
from sphinx.roles import XRefRole
from sphinx.util import logging
from sphinx.util.nodes import make_id

from sphinx_compendia import SphinxCompendiaError
from sphinx_compendia.sphinxapi import SphinxGeneralIndexEntry

if TYPE_CHECKING:
    from docutils.nodes import Element, Node, system_message
    from sphinx.addnodes import desc_signature
    from sphinx.environment import BuildEnvironment

    from sphinx_compendia.domain import Domain

log = logging.getLogger(__name__)


class ConstituentDescription(ObjectDescription[str]):
    """
    Capture the definition of a constituent within a directive.

    A constituent can have more than one name, all of which can be used
    for cross-referencing.

    Example:
        Given the directive's name is ``character`` within the ``world``
        domain,

        .. code-block:: rst

            .. world:character:: Gardakan
                Lord Gardakan
                Gardy

                A mighty paladin!

        This character will

        *   Be available for cross-referencing with the ``:world:character:``
            role (see :class:`~ConstituentReference`)

        *   Be listed in the ``world`` domain index
            (see :class:`sphinx_compendia.index.Index`)

        *   Be listed in the general index.

    """

    has_content = True
    required_arguments = 1

    constituent_objtype: ClassVar[str]

    namespace_separator: ClassVar[str]

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401 # We simply don't care about the types.
        super().__init__(*args, **kwargs)
        self.namespace: RefContextStack[str] = RefContextStack(self.env, "namespace")

    def handle_signature(self, sig: str, signode: addnodes.desc_signature) -> str:
        """
        Parse the signature into nodes and append them to the signature node.

        More specifically, ``handle_signature`` implements parsing the
        signatures of the directive and passes on the constituent's name
        and type to its superclass while providing the nodes used for
        displaying the signatures (names).

        For instance, given the following directive definition

        .. code-block:: rst

            .. world:character:: Guy McMaskface
                Guy McFace

                Some description of Guy.

        then ``Guy McMaskface`` and ``Guy McFace`` will be passed as the
        `sig` parameter in subsequent calls.

        .. hint:: Subclasses should consider re-implementing this method
            with caution.  Consider overriding

            *   :meth:`~make_primary_signature_nodes`
            *   :meth:`~make_secondary_signature_nodes`

            instead.

        Args:
            sig:
                The signature, ``Guy McMaskface`` from the the example above.
            signode:
                The signature document node.  It acts like the `term` part
                of a glossary entry.

                Given the example above, then the signode is a RestructuredText
                node that will be extended to represented with the following
                pseudo-HTML:

                .. code-block:: html

                    <dl class="world character">
                      <dt id="world-chracter-Guy-McMaskface">
                        Guy McMaskface
                      </dt>
                      <dt id="world-character-Guy-McFace">
                        Guy Mcface
                      </dt>
                      <dd>
                        <p>
                          Some description of Guy.
                        </p>
                      </dd>
                    </dl>

        Returns:
            We return a nice unique url friendly anchor name.

            The return value should be a value that identifies the constituent.
            It is passed to :meth:`add_target_and_index()` unchanged,
            and otherwise only used to skip duplicates.

        """
        identifier = make_id(self.env, self.state.document, self.name, sig)

        if not self.names:
            signode.extend(self.make_primary_signature_nodes(sig))
            self.namespace.push(sig)
        else:
            signode.extend(self.make_secondary_signature_nodes(sig))

        return identifier

    def after_content(self) -> None:
        self.namespace.pop()

    def make_primary_signature_nodes(self, sig: str) -> list[nodes.Element]:
        """
        Generate the appropriate nodes for rendering the primary name signature.

        Args:
            sig: The signature as a string.

        Returns:
            Docutils node for displaying the primary name signature.

        """
        localized_objtype = (
            self.get_topic_domain().object_types[self.objtype].lname.title()
        )

        return [
            addnodes.desc_annotation(
                self.objtype,
                "",
                nodes.Text(localized_objtype),
            ),
            addnodes.desc_sig_space(),
            addnodes.desc_name(text=sig),
        ]

    def make_secondary_signature_nodes(self, sig: str) -> list[nodes.Element]:
        """
        Generate the appropriate nodes for rendering the other name signatures.

        Args:
            sig: The signature as a string.

        Returns:
            Docutils node for displaying the alternate name signatures.

        """
        return [
            addnodes.desc_sig_punctuation(
                "—",
                "—",
            ),
            addnodes.desc_sig_space(),
            addnodes.desc_name(text=sig),
        ]

    def add_target_and_index(
        self, anchor: str, sig: str, signode: addnodes.desc_signature
    ) -> None:
        """
        Add cross-reference IDs and entries to indices, if applicable.

        This method will add this character name to the domain database
        (hence to the domain index) and to the general index.

        .. hint:: Subclasses should consider re-implementing this method
            with caution since it is responsible for registering this
            constituent's description to the domain data, and this API is
            not stable yet.

        Example:
            Using the following usages of this directive

            .. code-block:: rst

                .. world:character:: Guy McMaskface
                    Guy McFace

                    Some description of Guy.

                .. world:location:: Docktown

                    Some description of the city of Docktown.

            This method would be called once per signature, which means
            three (3) times, on two separate instances, the one named
            ``character`` and the one named ``location``.

        Args:
            anchor:
                The identifying name of this character name as returned by
                :meth:`~handle_signature`.  This name can act as a valid
                URL fragment (after the ``#`` part), an anchor, unique
                within a document.
            sig:
                One signature, which is the object name we are indexing.

                In the above example, both ``Guy McFace`` and
                ``Guy McMaskface``  will be passed
                as the `sig` parameter in separate invocations.
            signode:
                The signature document node as generated in
                :meth:`~handle_signature`.

        """
        # Not exactly sure how this works
        signode["ids"].append(anchor)
        self.state.document.note_explicit_target(signode)

        # First, register this object to the domain
        self.note_constituent_signature(anchor, sig, signode)
        # Then, add index entries for it
        generalindex_entry = SphinxGeneralIndexEntry(
            entrytype="single",
            entryname=sig,
            targetid=anchor,
            mainname=sig,
            key=None,
        )
        inode = addnodes.index(entries=[generalindex_entry])
        self.indexnode.append(inode)

    def get_topic_domain(self) -> Domain:
        """
        Get the underlying domain for this constituent's topic.

        Returns:
            Type-hinted domain.

        """
        return self.env.domains[self.domain]  # type: ignore[return-value,index] # the domain name may be null, the domain object may be anything. Let's hope everything is ok.

    def note_constituent_signature(
        self, anchor: str, signature: str, signode: addnodes.desc_signature
    ) -> None:
        domain = self.get_topic_domain()

        object_id = self.names[0]
        objtype = self.objtype

        return domain.note_constituent_signature(
            objtype,
            self.name,
            object_id,
            anchor,
            signature,
            self.namespace.stack[:-1],
            signode,
        )

    @property
    def objtype(self) -> str:
        """
        The objtype for documented constituents for this directive.

        The parent class behavior is to set this property based on the
        directive name.  In order to enable the possibility to have
        different directive names creating the same objtype, we override
        this property to have it always return the same objtype disregarding
        the directive name.  In other words, setting this property is a
        no op, does nothing.

        Returns:
            The objtype for documented constituent with this directive.

        """
        return self.constituent_objtype

    @objtype.setter
    def objtype(self, value: Any) -> None:  # noqa: ANN401 # Implementation should be flexible enough here
        pass

    _toc_entry_name_yielded: ClassVar[set[str]] = set()

    def make_toc_entry(self, sig_node: desc_signature) -> str | None:
        """
        Given a signature, make a ToC entry (o not).
        """
        fullname = self.namespace_separator.join(self.namespace.stack)

        if fullname in self._toc_entry_name_yielded:
            return None

        self._toc_entry_name_yielded.add(fullname)

        *parents, name = sig_node["_toc_parts"]

        config = self.env.app.config

        if config.toc_object_entries_show_parents == "domain":
            entry = f"{self.domain}:{name} ({self.objtype})"
        if config.toc_object_entries_show_parents == "hide":
            entry = f"{name} ({self.objtype})"
        if config.toc_object_entries_show_parents == "all":
            entry = f"{self.domain}:{fullname} ({self.objtype})"

        return entry

    def _object_hierarchy_parts(self, sig_node: desc_signature) -> tuple[str, ...]:  # noqa: ARG002
        return tuple(self.namespace.stack)

    def _toc_entry_name(self, sig_node: desc_signature) -> str:
        entry_or_not = self.make_toc_entry(sig_node)

        return entry_or_not or ""


class ConstituentReference(XRefRole):
    """
    Define a constistuent reference role.

    These references are added to the general index.
    """

    def process_link(
        self,
        env: BuildEnvironment,
        refnode: Element,
        has_explicit_title: bool,  # noqa: FBT001 # This method is inherited
        title: str,
        target: str,
    ) -> tuple[str, str]:
        """
        Process link for a given cross-reference role.

        See Also:
            The parent class method docstring is something like

                Called after parsing title and target text, and creating
                the reference node (given in *refnode*).  This method can
                alter the reference node and must return a new (or the same)
                ``(title, target)`` tuple.

        Args:
            env:
                Sphinx build environment.
            refnode:
                The created referenced node, which can be altered here.
            has_explicit_title:
                An explicit title in a role is when a display string is
                provided as part of the role's interpreted text. For example

                .. code-block: rst

                    :ref:`Here is an explicit title<some-reference-target>`

                would diplay an hyperlink to ``some-reference-target`` with
                ``Here is an explicit title`` as the link text.

                This value is also available as a instance member with the
                same name (``self.has_explicit_title``).
            title:
                The link title.
            target:
                The link target identifier.

        Returns:
            Title and target strings.

        """
        title, target = super().process_link(
            env, refnode, has_explicit_title, title, target
        )
        namespace: RefContextStack[str] = RefContextStack(env, "namespace")

        if target.startswith("."):
            newtarget = ".".join(
                part for part in [".".join(namespace.stack), target[1:]] if part
            )
            if target.endswith("."):
                newtarget += "."
            target = newtarget

        return title, target

    def result_nodes(
        self,
        document: nodes.document,
        env: BuildEnvironment,  # noqa: ARG002 # This method is inherited
        node: Element,
        is_ref: bool,  # noqa: FBT001,ARG002 # This method is inherited
    ) -> tuple[list[Node], list[system_message]]:
        """
        Add general index nodes just before returning the finished xref nodes.

        .. hint:: Subclasses should consider re-implementing this method
            with caution since it is responsible for registering this
            constituent's cross-reference to the domain data, and this API
            is not stable yet.

        Args:
            document:
                Source document where this ref was defined.
            env:
                Current Sphinx build environment.
            node:
                This role's node.
            is_ref:
                True when this is the reference node, else it's the content
                node.

        Returns:
            Not sure what the second item of this tuple should be.

        """
        anchor = make_id(self.env, document, "sphinx_compendia#backrefs", self.rawtext)
        node["ids"].append(anchor)
        document.set_id(node)
        self._note_general_index(node)
        return [node], []

    def _note_general_index(self, node: Element) -> None:
        entry = SphinxGeneralIndexEntry(
            entrytype="single",
            entryname=self.target,
            targetid=node["ids"][0],  # targetid=self.rawtext,
            mainname=node.attributes.get("refdoc", ""),
            key=None,
        )
        inode = addnodes.index(entries=[entry])
        node.append(inode)


T = TypeVar("T")


class RefContextStack(Generic[T]):
    def __init__(self, env: BuildEnvironment, key: str):
        """
        Provide a stack-like data structure in the build environment.

        The idea behind this is to share some data between directives and
        role implementations.  We use a stack to help support implementations
        that enable specific features when directives are nested within
        each other.

        Examples:
            >>> class StubEnvironment:
            ...     ref_context = {}
            >>> env = StubEnvironment()
            >>> namespace: RefContextStack[str] = RefContextStack(env, "namespace")
            >>> namespace.stack
            []
            >>> namespace.push("foo")
            >>> namespace.stack
            ['foo']
            >>> namespace.push("bar")
            >>> namespace.stack
            ['foo', 'bar']
            >>> namespace.peek()
            'bar'
            >>> namespace.stack
            ['foo', 'bar']
            >>> namespace.pop()
            'bar'
            >>> namespace.stack
            ['foo']
            >>> namespace.pop()
            'foo'
            >>> None == namespace.pop()
            True

        Args:
            env:
                The build environment is the container for this reference
                context stack.
            key:
                We store our stack under a certain key.

        """
        self.env = env
        self.key = key

    @property
    def stack(self) -> list[T]:
        stack = self.env.ref_context.setdefault(self.key, [])
        if isinstance(stack, list):
            return stack
        msg = f"ref_context for '{self.key}' was of unexpected type '{type(stack)}'."
        raise SphinxCompendiaError(msg)

    def push(self, value: T) -> None:
        self.stack.append(value)

    def peek(self) -> T | None:
        if self.stack:
            return self.stack[-1]
        return None

    def pop(self) -> T | None:
        try:
            return self.stack.pop()
        except IndexError:
            return None
