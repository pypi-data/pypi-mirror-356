from typing import Sequence, Optional, List, Tuple

from sphinx.domains import Domain
from sphinx.util.docutils import SphinxDirective
from sphinx.util import logging
from sphinx import addnodes

from docutils import nodes
from docutils.parsers.rst import directives

from systemrdl.node import Node, RegNode, AddressableNode, SignalNode, RootNode
from systemrdl.rdltypes.references import PropertyReference
from systemrdl.source_ref import FileSourceRef, DetailedFileSourceRef

from ..utils import lookup_rdl_node, FieldList, Table, alpha_from_int

from ..markdown.render import render_to_docutils


logger = logging.getLogger(__name__)

def link_to_option(argument) -> str:
    return directives.choice(argument, ("html", "doc"))

class RDLDocNodeDirective(SphinxDirective):
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False


    option_spec = {
        "wrap-section": directives.flag, "no-wrap-section": directives.flag,
        "link-to": link_to_option,
    }

    @property
    def target(self) -> str:
        return self.arguments[0]

    @property
    def domain(self) -> Domain:
        return self.env.get_domain("rdl")

    def run(self) -> Sequence[nodes.Node]:
        # Resolve options
        if "no-wrap-section" in self.options:
            self.options["wrap-section"] = False
        elif "wrap-section" in self.options:
            self.options["wrap-section"] = True
        else:
            self.options["wrap-section"] = self.config.peakrdl_doc_wrap_section

        # Try to lookup node
        relative_to_path: Optional[str] = self.env.ref_context.get("rdl:relative-to")
        rdl_node = lookup_rdl_node(self.target, relative_to_path)
        if rdl_node is None:
            logger.warning(
                "RDL target not found: %s",
                self.target,
                location=self.get_location(),
            )
            return []

        # Generate content
        return self.make_rdl_node_doc(rdl_node)

    #---------------------------------------------------------------------------
    # General Utilities
    #---------------------------------------------------------------------------
    def get_rdl_xref(self, rdl_node: Node, text: Optional[str] = None) -> addnodes.pending_xref:
        """
        Given an RDL node, create a pending xref docutils object.
        """
        xref = addnodes.pending_xref(
            refdoc=self.env.docname,
            refdomain="rdl",
            reftype="", # TODO: do i care about this?
            reftarget=rdl_node.get_path(array_suffix="", empty_array_suffix=""),
            refwarn=False, # Don't emit a warning if can't be linked
        )
        self.set_source_info(xref)

        target_type: Optional[str] = self.options.get("link-to")
        if target_type:
            xref["rdl:target-type"] = target_type

        if text is None:
            text = rdl_node.inst_name
        xref += nodes.inline(text=text, classes=["xref"])
        return xref

    def get_rdl_desc(self, rdl_node: Node) -> nodes.paragraph:
        """
        Given an RDL node, get its description and pass it though markdown processing
        """
        desc = rdl_node.get_property("desc") or ""

        src_ref = rdl_node.inst.property_src_ref.get("desc", rdl_node.inst.inst_src_ref)
        if isinstance(src_ref, FileSourceRef):
            path = src_ref.path
        else:
            path = "UNKNOWN"

        # Note: Computing the line number for EVERY src ref may be time consuming
        # I may want to remove this in the future
        if isinstance(src_ref, DetailedFileSourceRef):
            line = src_ref.line
        else:
            line = 0

        desc_nodes = render_to_docutils(desc, path, line)

        p = nodes.paragraph()
        p.extend(desc_nodes)
        return p

    def stringify_array_dims(self, dims: List[int]) -> str:
        return "".join([f"[{dim}]" for dim in dims])

    def get_info_header(self, rdl_node: AddressableNode) -> nodes.field_list:
        """
        Build the node doc's summary header objects
        """
        fl = FieldList()

        # Build crumbtrail
        crumbtrail = nodes.paragraph()
        current_node = rdl_node
        path_nodes: List[Tuple[int, AddressableNode]] = []
        i = 0
        iterator_idx = 0
        while True:
            path_nodes.append((i, current_node))
            i += 1
            if isinstance(current_node.parent, RootNode):
                break
            current_node = current_node.parent
        path_nodes.reverse()
        for i, path_node in path_nodes:
            if i == 0:
                crumbtrail.append(nodes.inline(text=path_node.inst_name))
            else:
                crumbtrail.append(self.get_rdl_xref(path_node))

            if path_node.array_dimensions:
                dims_str = ""
                for _ in path_node.array_dimensions:
                    dims_str += f"[{alpha_from_int(iterator_idx)}]"
                    iterator_idx += 1
                crumbtrail.append(nodes.inline(text=dims_str))

            if i != 0:
                # Is not last
                crumbtrail.append(nodes.inline(text="."))
        fl.add_row("Path", crumbtrail)

        # Build absolute address formula
        abs_addr_str = f"{rdl_node.raw_absolute_address:#x}"
        iterator_idx = 0
        for _, path_node in path_nodes:
            if path_node.array_dimensions:
                if len(path_node.array_dimensions) == 1:
                    # Is single-dimensional node.
                    abs_addr_str += f" + {alpha_from_int(iterator_idx)}*{path_node.array_stride:#x}"
                else:
                    # Equation is more complex
                    mults = ""
                    dim_parts = []
                    for i, dim in reversed(list(enumerate(path_node.array_dimensions))):
                        dim_parts.append(f"{mults}{alpha_from_int(iterator_idx + i)}")
                        mults = f"{dim}*{mults}"
                    dim_parts_joined = " + ".join(reversed(dim_parts))
                    abs_addr_str += f" + ({dim_parts_joined}) * {path_node.array_stride:#x}"
                iterator_idx += len(path_node.array_dimensions)
        fl.add_row("Absolute Address", abs_addr_str)

        if rdl_node.array_dimensions:
            fl.add_row("Array Dimensions", str(rdl_node.array_dimensions))
            fl.add_row("Array Stride", f"{rdl_node.array_stride:#x}")

        return fl.as_node()

    #---------------------------------------------------------------------------
    def make_rdl_node_doc(self, rdl_node: Node) -> Sequence[nodes.Element]:
        if isinstance(rdl_node, RegNode):
            doc_nodes = self.make_rdl_reg_doc(rdl_node)
        elif isinstance(rdl_node, AddressableNode):
            doc_nodes = self.make_rdl_grouplike_doc(rdl_node)
        else:
            logger.warning(
                "Cannot generate doc content for %s components: %s",
                type(rdl_node.inst).__name__.lower(),
                self.target,
                location=self.get_location(),
            )
            return []

        if self.options["wrap-section"]:
            ref_id = rdl_node.get_path(array_suffix="", empty_array_suffix="")
            heading = nodes.section()
            heading.attributes["ids"] = [ref_id]
            # TODO: Include RDL name in title if it was set.
            heading.append(nodes.title(text=rdl_node.inst_name))
            heading.extend(doc_nodes)
            doc_nodes = [heading]

            # information about this doc node's location it in the domain
            self.domain.data["rdl_docnodes"][ref_id] = self.env.docname
        return doc_nodes


    def make_rdl_reg_doc(self, rdl_node: RegNode) -> Sequence[nodes.Element]:
        # Info Field List Header
        fl = self.get_info_header(rdl_node)

        # Description
        desc_paragraph = self.get_rdl_desc(rdl_node)

        # Field Table
        table = Table(["Bits", "Identifier", "Access", "Reset", "Name"])
        for field in reversed(rdl_node.fields()):
            # Is actual field
            if field.width == 1:
                bitrange = f"[{field.lsb}]"
            else:
                bitrange = f"[{field.msb}:{field.lsb}]"

            access = field.get_property("sw").name
            onread = field.get_property("onread")
            onwrite = field.get_property("onwrite")
            if onread:
                access += f", {onread.name}"
            if onwrite:
                access += f", {onwrite.name}"

            reset_value = field.get_property("reset")
            if reset_value is None:
                reset = "-"
            elif isinstance(reset_value, int):
                reset = f"{reset_value:#x}"
            elif isinstance(reset_value, PropertyReference):
                reset = self.get_rdl_xref(reset_value.node) + "->" + reset_value.name
            elif isinstance(reset_value, SignalNode):
                reset = reset_value.get_path()
            else:
                reset = self.get_rdl_xref(reset_value)

            table.add_row([
                bitrange,
                field.inst_name,
                access,
                reset,
                field.get_property("name", default="-"),
            ])

        # Field descriptions
        def_list = nodes.definition_list()
        for field in reversed(rdl_node.fields()):
            desc = field.get_property("desc")
            if not desc:
                continue

            dli = nodes.definition_list_item()
            def_list.append(dli)

            dl_term = nodes.term(text = field.inst_name)
            dl_def = nodes.definition()
            dl_def_p = self.get_rdl_desc(field)
            dl_def.append(dl_def_p)

            dli.append(dl_term)
            dli.append(dl_def)

        return [fl, desc_paragraph, table.as_node(), def_list]


    def make_rdl_grouplike_doc(self, rdl_node: AddressableNode) -> Sequence[nodes.Element]:
        # Info Field List Header
        fl = self.get_info_header(rdl_node)

        # Description
        desc_paragraph = self.get_rdl_desc(rdl_node)

        # Child table
        table = Table(["Offset", "Identifier", "Name"])
        for child in rdl_node.children():
            if not isinstance(child, AddressableNode):
                continue

            offset = f"{child.raw_address_offset:#x}"

            if child.array_dimensions:
                text = child.inst_name + self.stringify_array_dims(child.array_dimensions)
                identifier = self.get_rdl_xref(child, text)
            else:
                identifier = self.get_rdl_xref(child)

            table.add_row([
                offset,
                identifier,
                child.get_property("name", default="-"),
            ])

        return [fl, desc_paragraph, table.as_node()]
