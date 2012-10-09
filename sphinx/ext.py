from sphinx.builders.html import SerializingHTMLBuilder
from sphinx.writers.html import HTMLTranslator, HTMLWriter, admonitionlabels, nodes
import pickle
import docutils.nodes

class BootstrapHTMLTranslator(HTMLTranslator):
    admonition_to_alert = {
        'attention': 'alert',
        'caution':   'alert',
        'danger':    'alert alert-error',
        'error':     'alert alert-error',
        'hint':      'alert alert-info',
        'important': 'alert',
        'note':      'alert alert-info',
        'seealso':   'alert alert-info',
        'tip':       'alert alert-success',
        'warning':   'alert',
    }

    def visit_admonition(self, node, name):
        ''' Map admonition t bootstrap alert boxes.'''
        self.body.append(self.starttag(
            node, 'div', CLASS=self.admonition_to_alert[name]))
        if name and name != 'seealso':
            self.body.append('<h4 class="alert-heading">%s</h4>' % admonitionlabels[name])
        self.set_first_last(node)

class TOCExtractor(docutils.nodes.SparseNodeVisitor):
    def __init__(self, document):
        docutils.nodes.SparseNodeVisitor.__init__(self, document)
        self.nodes = []
        self.parent = dict(title='dummy', childs=self.nodes, parent=None)

    def visit_reference(self, node):
        self.nodes.append(
            dict(title=node.astext(),
                 href=node['refuri'],
                 childs=[],
                 parent=self.parent))

    def visit_bullet_list(self, node):
        if self.nodes:
            self.parent = self.nodes[-1]
            self.nodes = self.nodes[-1]['childs']

    def depart_bullet_list(self, node):
        if self.parent and self.parent['parent']:
            self.nodes = self.parent['parent']['childs']
            self.parent = self.parent['parent']

class BottlepyPickleBuilder(SerializingHTMLBuilder):
    implementation = pickle
    implementation_dumps_unicode = False
    additional_dump_args = (pickle.HIGHEST_PROTOCOL,)
    indexer_format = pickle
    indexer_dumps_unicode = False
    name = 'bottlepy'
    out_suffix = '.pkl'
    globalcontext_filename = 'globalcontext.pkl'
    searchindex_filename = 'searchindex.pkl'

    def get_doc_context(self, docname, body, metatags):
        ctx = SerializingHTMLBuilder.get_doc_context(self, docname, body, metatags)
        ex = TOCExtractor(self.docwriter.document)
        self.env.get_toc_for(docname, self).walkabout(ex)
        ctx['toctree'] = ex.nodes[0]
        return ctx

    def get_target_uri(self, docname, typ=None):
        return docname + '.html'

    def init_translator_class(self):
        self.translator_class = BootstrapHTMLTranslator

def setup(app):
    app.add_builder(BottlepyPickleBuilder)
