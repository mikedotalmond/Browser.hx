#
# Renders a single IDL file into Haxe

import itertools
import re

from idlnode import *

haxe_idl_types = {
    "boolean": "Bool",
    "byte": "Int",
    "char": "Int",
    "signed char": "Int",
    "unsigned char": "Int",
    "octet": "Int",
    "short": "Int",
    "unsigned short": "Int",
    "int": "Int",
    "unsigned int": "Int",
    "long": "Int", # Float?
    "unsigned long": "Int", # Float?
    "long long": "Int", # Float?
    "unsigned long long": "Int", # Float?
    "float": "Float",
    "double": "Float",
    "void": "Void",

    "any": "Dynamic",
    "custom": "Dynamic",
    # "Date": "Float",
    "DOMObject": "Dynamic",
    "DOMString": "String",
    "DOMTimeStamp": "Int", # Float?
    "Dictionary": "Dynamic",
    "object": "Dynamic",

    "Array": "Array<Dynamic>",
    "ObjectArray": "Array<Dynamic>",
    "sequence": "Array<Dynamic>",
    "MutationRecordArray": "Array<MutationRecord>",

    # Where did these go?
    "PositionOptions": "Dynamic",
    "SerializedScriptValue": "Dynamic",
    "TimeoutHandler": "Void->Void",
    "CompareHow": "Int",

    # Temporary maybe?
    "Acceleration": "DeviceAcceleration",
    "RotationRate": "DeviceRotationRate",
}

haxe_keywords = [
    "callback",
    "continue",
    "default",
    "override",
]

# Used to generate typed shortcut methods in Document
html_elements = {
    "AnchorElement": "a",
    "AppletElement": "applet",
    "AreaElement": "area",
    "AudioElement": "audio",
    "BaseElement": "base",
    "BaseFontElement": "basefont",
    "BodyElement": "body",
    "BRElement": "br",
    "ButtonElement": "button",
    "CanvasElement": "canvas",
    "ContentElement": "content",
    "DataListElement": "datalist",
    "DetailsElement": "details",
    "DirectoryElement": "dir",
    "DivElement": "div",
    "DListElement": "dl",
    # "Element",
    "EmbedElement": "embed",
    "FieldSetElement": "fieldset",
    "FontElement": "font",
    "FormElement": "form",
    "FrameElement": "frame",
    "FrameSetElement": "frameset",
    "HeadElement": "head",
    # "HeadingElement"
    "HRElement": "hr",
    "HtmlElement": "html",
    "IFrameElement": "iframe",
    "ImageElement": "img",
    "InputElement": "input",
    "KeygenElement": "keygen",
    "LabelElement": "label",
    "LegendElement": "legend",
    "LIElement": "li",
    "LinkElement": "link",
    "MapElement": "map",
    "MarqueeElement": "marquee",
    "MediaElement": "media",
    "MenuElement": "menu",
    "MetaElement": "meta",
    "MeterElement": "meter",
    "ModElement": "mod",
    "ObjectElement": "object",
    "OListElement": "ol",
    "OptGroupElement": "optgroup",
    "OptionElement": "option",
    "OutputElement": "output",
    "ParagraphElement": "p",
    "ParamElement": "param",
    "PreElement": "pre",
    "ProgressElement": "progress",
    "QuoteElement": "quote",
    "ScriptElement": "script",
    "SelectElement": "select",
    "ShadowElement": "shadow",
    "SourceElement": "source",
    "SpanElement": "span",
    "StyleElement": "style",
    "TableCaptionElement": "caption",
    "TableCellElement": "td",
    "TableColElement": "col",
    "TableElement": "table",
    "TableRowElement": "tr",
    "TableSectionElement": "thead",
    "TextAreaElement": "textarea",
    "TitleElement": "title",
    "TrackElement": "track",
    "UListElement": "ul",
    # "UnknownElement",
    "VideoElement": "video",
}

def to_haxe(id):
    """Converts an IDL type name to Haxe."""
    if id.endswith("..."):
        # TODO(bruno): Support varargs somehow. Probably by emitting a few @:overloads
        id = id[:-3]

    match = re.match(r"(?:sequence<(\w+)>|(\w+)\[\])$", id)
    if match:
        return "Array<%s>" % to_haxe(match.group(1) or match.group(2))

    match = re.match(r"HTML(.+)Element", id)
    if match:
        id = match.group(1)+"Element"

    if id in haxe_idl_types:
        return haxe_idl_types.get(id)
    return strip_vendor(id)

def array_access(interface):
    """Returns the type to use for ArrayAccess, or None."""
    if "IndexedGetter" in interface.ext_attrs:
        for op in interface.operations:
            if op.id == "item":
                return op.type.id
    elif "TypedArray" in interface.ext_attrs:
        return interface.ext_attrs["TypedArray"]
    return None

def constructable(interface):
    """Returns whether the interface has a constructor."""
    return set(["CustomConstructor", "V8CustomConstructor", "Constructor",
        "NamedConstructor", "ConstructorTemplate"]) & set(interface.ext_attrs)

def escape_keyword(id):
    """Escapes a Haxe keyword."""
    return id+"_" if id in haxe_keywords else id

def strip_vendor(id):
    """Strips vendor prefixes (webkit) from an id."""
    id = re.sub(r"^WebKit", "", id)
    id = re.sub(r"^WEBKIT_", "", id)
    id = re.sub(r"^onwebkit", "on", id)
    id = re.sub(r"^initWebKit", "init", id) # Used in some Events
    if id.startswith("webkit"):
        id = re.sub(r"^webkit", "", id)
        id = id[0].lower() + id[1:]
    return id

def strip_vendor_fields(nodes, remove=True):
    for node in nodes:
        stripped = strip_vendor(node.id)
        if stripped != node.id:
            if remove:
                exists = False
                for x in nodes:
                    if x.id == stripped:
                        exists = True
                if exists:
                    nodes.remove(node)
                    continue
            node.id = stripped

def is_callback(node):
    return "Callback" in node.ext_attrs \
        or node.id == "EventListener" \
        or node.id == "MediaQueryListListener"

def render(db, idl_node, mdn_js, mdn_css, header=None):
    output = []
    indent_stack = []
    EventTarget = db.GetInterface("EventTarget")

    def begin_indent():
        indent_stack.append("    ")
    def end_indent():
        indent_stack.pop()

    def sort(nodes):
        return sorted(nodes, key=lambda node: node.id)

    def get_parent(interface):
        if interface.parents:
            return db.GetInterface(interface.parents[0].type.id)
        if "EventTarget" in interface.ext_attrs:
            return EventTarget
        return None

    def defined_in_parent(interface, id):
        """Whether an id is already defined in an interface's parents"""
        parent = get_parent(interface)
        if parent:
            if parent.attributes:
                for attribute in parent.attributes:
                    if attribute.id == id:
                        return True
            if parent.operations:
                for operation in parent.operations:
                    if operation.id == id:
                        return True
            return defined_in_parent(parent, id)
        return False

    def wln(node=None):
        """Writes the given node and adds a new line."""
        w(node)
        output.append("\n")

    def wsp(node):
        """Writes the given node and adds a space if there was output."""
        mark = len(output)
        w(node)
        if mark != len(output):
            w(" ")

    def w_doc(text):
        text = text.strip()
        if text != "":
            wln("/** %s */" % text)

    def w(node, list_separator=None):
        """Writes the given node.

        Args:
            node -- a string, IDLNode instance or a list of such.
            list_separator -- if provided, and node is a list,
                list_separator will be written between the list items.
        """
        if node is None:
            return

        elif isinstance(node, str) or isinstance(node, unicode):
            if output and output[-1].endswith("\n"):
                # Auto-indent.
                output.extend(indent_stack)
            output.append(node)

        elif isinstance(node, list):
            for i in range(0, len(node)):
                if i > 0:
                    w(list_separator)
                w(node[i])

        elif isinstance(node, IDLFile):
            w(node.modules)
            w(node.interfaces)

        elif isinstance(node, IDLModule):
            w(node.interfaces)
            w(node.typeDefs)

        elif isinstance(node, IDLInterface):
            class_doc = None
            if node.id in mdn_js:
                class_doc = mdn_js[node.id]
                if "summary" in class_doc:
                    w_doc("<br><br>\n".join([
                        class_doc["summary"],
                        "Documentation for this class was provided by <a href=\"%s\">MDN</a>." % class_doc["srcUrl"]
                    ]))

            def w_member_doc(node):
                docs = []
                if hasattr(node, "raises") and node.raises:
                    docs += ["Throws %s." % to_haxe(node.raises.id)]
                if hasattr(node, "get_raises") and node.get_raises:
                    docs += ["Getter throws %s." % to_haxe(node.get_raises.id)]
                if hasattr(node, "set_raises") and node.set_raises:
                    docs += ["Setter throws %s." % to_haxe(node.set_raises.id)]
                if class_doc and class_doc["members"]:
                    for member in class_doc["members"]:
                        if member["name"] == node.id:
                            docs = [member["help"]] + docs
                            break
                w_doc(" ".join(docs))

            def w_constructor_doc():
                if class_doc and "constructor" in class_doc:
                    w_doc(class_doc["constructor"])

            def w_members(members):
                for member in members:
                    w_member_doc(member)
                    wln(member)

            if is_callback(node):
                # Generate a function typedef if this is a callback
                callback = node.operations[0]
                if callback.arguments:
                    arguments = " -> ".join([to_haxe(x.type.id) for x in callback.arguments])
                else:
                    arguments = "Void"
                w("typedef %s = %s -> %s;" % (node.id, arguments, to_haxe(callback.type.id)))
                return

            interface_name = node.ext_attrs["InterfaceName"] if "InterfaceName" in node.ext_attrs else node.id
            wln("@:native(\"%s\")" % strip_vendor(interface_name))
            w("extern class %s" % to_haxe(node.id))
            strip_vendor_fields(node.constants)
            strip_vendor_fields(node.attributes)
            strip_vendor_fields(node.operations, False)

            inherits = []
            parent = get_parent(node)
            if parent:
                inherits.append("extends %s" % to_haxe(parent.id))
            if len(node.parents) > 1:
                print("Omitting excess superclasses from %s" % node.id)
            array_type = array_access(node)
            if array_type:
                inherits.append("implements ArrayAccess<%s>" % to_haxe(array_type))
            if inherits:
                w(" " + ", ".join(inherits))

            wln()
            wln("{")
            begin_indent()
            if node.constants:
                w_members(sort(node.constants))
            if node.attributes:
                attributes = sort([x for x in node.attributes if not defined_in_parent(node, x.id)])
                if "ExtendsDOMGlobalObject" in node.ext_attrs:
                    # Omit class contructors from the global object
                    w_members([x for x in attributes if not x.type.id.endswith("Constructor")])
                else:
                    w_members(attributes)
            if node.id == "CSSStyleDeclaration":
                for prop in sorted(mdn_css):
                    w_doc(mdn_css[prop])
                    # Convert to camel case
                    prop = "".join([x[0].upper()+x[1:] for x in prop.split("-")])
                    prop = prop[0].lower() + prop[1:] # Re-lowercase the first word
                    wln("var " + prop + " (default,null) :String;")
                    wln()
            if constructable(node):
                constructors = []
                if "ConstructorTemplate" in node.ext_attrs:
                    template = node.ext_attrs["ConstructorTemplate"]
                    if template == "Event":
                        constructors += [
                            ["type :String", "canBubble :Bool = true", "cancelable :Bool = true"],
                        ]
                    elif template == "TypedArray":
                        array_type = to_haxe(node.ext_attrs["TypedArray"])
                        constructors += [
                            ["array :ArrayBufferView"],
                            ["array :Array<"+array_type+">"],
                            ["buffer :Array<"+array_type+">", "?byteOffset :Int", "?length :Int"],
                            ["length :Int"],
                        ]
                    else:
                        raise TypeError("Unrecognized ConstructorTemplate for " + node.id)
                elif "ConstructorParameters" in node.ext_attrs:
                    c = []
                    for ii in range(int(node.ext_attrs["ConstructorParameters"])):
                        c += ["?arg%s :Dynamic" % ii]
                    constructors += [c]
                else:
                    constructors += [[]]
                w_constructor_doc()
                for ii, c in enumerate(constructors):
                    args = ", ".join(c)
                    if ii < len(constructors)-1:
                        wln("@:overload(function (%s) :Void {})" % args)
                    else:
                        wln("function new (%s) :Void;" % args)
                wln()
            if node.operations:
                operations = sort([x for x in node.operations if not defined_in_parent(node, x.id)])
                for id, group in itertools.groupby(operations, lambda node: node.id):
                    group = list(group)
                    ll = len(group)
                    if ll > 1:
                        w_member_doc(group[0])
                        for ii, overload in enumerate(group):
                            if ii < ll-1:
                                w("@:overload(function (")
                                w(overload.arguments, ", ")
                                wln(") :%s {})" % to_haxe(overload.type.id))
                            else:
                                wln(overload)
                    else:
                        wln(group[0])
            if node.id == "HTMLDocument":
                for type, tag_name in html_elements.iteritems():
                    w_doc("A typed shortcut for createElement(\"%s\")." % tag_name)
                    wln("public inline function create%s () :%s return cast createElement(\"%s\")" % (
                        type, type, tag_name))
            end_indent()
            wln("}")

        elif isinstance(node, IDLAttribute):
            stripped = strip_vendor(node.id)
            escaped = escape_keyword(stripped)
            attr_type = to_haxe(node.type.id)
            w("var %s " % escaped)
            if escaped != stripped:
                # TODO(bruno): Switch over to Haxe 3 property syntax
                wln("(get_%s,%s) :%s;" % (escaped, "null" if node.is_read_only else "set_"+escaped, attr_type))
                wln("private inline function get_%s () :%s {" % (escaped, attr_type))
                begin_indent()
                wln("return untyped this[\"%s\"];" % stripped)
                end_indent()
                wln("}")
                if not node.is_read_only:
                    wln("private inline function set_%s (x :%s) :%s {" % (escaped, attr_type, attr_type))
                    begin_indent()
                    wln("return untyped this[\"%s\"] = x;" % stripped)
                    end_indent()
                    wln("}")
            else:
                if node.is_read_only:
                    w("(default,null) ")
                wln(":%s;" % to_haxe(node.type.id))

        elif isinstance(node, IDLConstant):
            wln("static inline var %s :%s = %s;" % (escape_keyword(strip_vendor(node.id)),
                to_haxe(node.type.id), node.value))

        elif isinstance(node, IDLOperation):
            stripped = strip_vendor(node.id)
            escaped = escape_keyword(stripped)
            return_type = to_haxe(node.type.id)
            if node.is_static:
                w("static ")
            if escaped != stripped:
                w("private inline function %s (" % escaped)
                w(node.arguments, ", ")
                wln(") :%s {" % return_type)
                begin_indent()
                if return_type != "Void":
                    w("return ")
                wln("(untyped this[\"%s\"])(%s);" % (stripped,
                    ", ".join([escape_keyword(strip_vendor(arg.id)) for arg in node.arguments])))
                end_indent()
                wln("}")
            else:
                w("function %s (" % escaped)
                w(node.arguments, ", ")
                wln(") :%s;" % return_type)

        elif isinstance(node, IDLArgument):
            if "Optional" in node.ext_attrs and node.ext_attrs["Optional"] is None:
                w("?")
            w("%s :%s" % (escape_keyword(strip_vendor(node.id)), to_haxe(node.type.id)))

        else:
            raise TypeError("Expected str or IDLNode but %s found" %
                type(node))

    if header:
        wln(header)
    w(idl_node)
    return "".join(output)
