from zope.schema.vocabulary import SimpleVocabulary

import pytest


class TestVocabColumnAlignments:
    name = "collective.contentsections.ColumnAlignments"

    @pytest.fixture(autouse=True)
    def _vocab(self, get_vocabulary, portal):
        self.vocab = get_vocabulary(self.name, portal)

    def test_vocabulary(self):
        assert self.vocab is not None
        assert isinstance(self.vocab, SimpleVocabulary)

    @pytest.mark.parametrize(
        "token,title",
        [
            ["start", "Start"],
            ["center", "Center"],
            ["end", "End"],
        ],
    )
    def test_column_alignments(self, token, title):
        term = self.vocab.getTerm(token)
        assert title == term.title
