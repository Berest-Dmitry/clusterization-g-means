import string
from PyQt5.uic.Compiler.misc import Literal
from pydantic_xml import attr, BaseXmlModel


class PostClusteringModel(BaseXmlModel):
    title: Literal[string] = attr()
    content: Literal[string] = attr()
    publisher_name: Literal[string] = attr()
    link_url: Literal[string] = attr()
    link_name: Literal[string] = attr()
    geo_tag: Literal[string] = attr()

