from pybtex.plugin import find_plugin
from pybtex.style.formatting import BaseStyle, toplevel
from pybtex.style.formatting.unsrt import pages
from pybtex.style.template import (field, first_of, href, join, names, optional, optional_field, sentence, tag, node,
                                   words, FieldIsMissing)


date = words[optional_field('month'), field('year')]


@node
def first_name(children, context, role, **kwargs):
    """Return formatted names."""

    assert not children

    try:
        persons = context['entry'].persons[role]
    except KeyError:
        raise FieldIsMissing(role, context['entry'])

    style = context['style']
    formatted_name = style.format_first_name(persons[0], style.abbreviate_names)
    return join(**kwargs)[formatted_name].format_data(context)


class GOSTStyle(BaseStyle):
    abbreviate_names = True

    def __init__(self, min_crossrefs=2, **kwargs):
        self.format_name = find_plugin('pybtex.style.names', 'plain')().format
        self.format_first_name = find_plugin('pybtex.style.names', 'lastfirst')().format
        self.format_labels = find_plugin('pybtex.style.labels', None)().format_labels

        self.sort = find_plugin('pybtex.style.sorting', None)().sort
        self.min_crossrefs = min_crossrefs

    @staticmethod
    def format_doi(e):
        return join['[', href[join['https://doi.org/', field('doi', raw=True)], 'doi'], ']']

    def get_article_template(self, e):
        template = toplevel[
            first_name('author'),
            field('title'), '/',
            names('author', sep=', '), '//',
            sentence(sep='. – ')[
                tag('em')[field('journal')],
                date,
                optional[join[words['V.', field('volume')],
                              optional[words[', Is.', field('number')]],
                              optional[words['. – P.', pages]]]]],
            sentence(sep=' ')[optional[self.format_doi(e)],
                              optional[join['(', field('note'), ')']]]
        ]
        return template
