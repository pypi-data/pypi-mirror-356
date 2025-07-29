"""Tests for the common models."""

from typing import Any

from semantic_scholar.models.common import (
    CitationStyles,
    Embedding,
    FieldsOfStudy,
    Journal,
    OpenAccessPdf,
    PublicationVenue,
    Tldr,
)


class TestOpenAccessPdf:
    """Tests for the OpenAccessPdf model."""

    def test_real_response(self, mock_server_paper_response: dict[str, Any]):
        sample_response = mock_server_paper_response["openAccessPdf"]

        pdf = OpenAccessPdf.model_validate(sample_response)

        assert pdf.url == "https://example.org/papers/p123456/open-access.pdf"
        assert pdf.status == "GREEN"


class TestEmbedding:
    """Tests for the Embedding model."""

    def test_real_response(self, mock_server_paper_response: dict[str, Any]):
        sample_response = mock_server_paper_response["embedding"]

        embedding = Embedding.model_validate(sample_response)

        assert embedding.model == "sample-embedding-model@v1.0"
        assert embedding.vector == [0.1, -0.2, 0.3, -0.4, 0.5]


class TestTldr:
    """Tests for the Tldr model."""

    def test_real_response(self, mock_server_paper_response: dict[str, Any]):
        sample_response = mock_server_paper_response["tldr"]

        tldr = Tldr.model_validate(sample_response)

        assert tldr.model == "tldr-model@v1.0"
        assert tldr.text == "This paper introduces a new approach to machine learning that improves accuracy."


class TestPublicationVenue:
    """Tests for the PublicationVenue model."""

    def test_real_response(self, mock_server_paper_response: dict[str, Any]):
        sample_response = mock_server_paper_response["publicationVenue"]

        venue = PublicationVenue.model_validate(sample_response)

        assert venue.id == "v123456"
        assert venue.name == "International Conference on Machine Learning"
        assert venue.type == "conference"
        assert venue.alternate_names == ["ICML", "Intl. Conf. on ML"]
        assert venue.url == "https://example.org/conferences/icml"


class TestJournal:
    """Tests for the Journal model."""

    def test_real_response(self, mock_server_paper_response: dict[str, Any]):
        sample_response = mock_server_paper_response["journal"]

        journal = Journal.model_validate(sample_response)

        assert journal.name == "Journal of Artificial Intelligence Research"
        assert journal.volume == "42"
        assert journal.pages == "123-145"


class TestCitationStyles:
    """Tests for the CitationStyles model."""

    def test_real_response(self, mock_server_paper_response: dict[str, Any]):
        sample_response = mock_server_paper_response["citationStyles"]

        styles = CitationStyles.model_validate(sample_response)

        assert (
            styles.bibtex
            == "@article{smith2018advances, title={Advances in Machine Learning Theory}, author={Smith, Jane}}"
        )


class TestS2FieldsOfStudy:
    """Tests for the S2FieldsOfStudy model."""

    def test_real_response(self, mock_server_paper_response: dict[str, Any]):
        sample_response = mock_server_paper_response["s2FieldsOfStudy"][0]

        field = FieldsOfStudy.model_validate(sample_response)

        assert isinstance(field, FieldsOfStudy)
        assert field.category == "Computer Science"
        assert field.source == "external"

    def test_missing_all_fields(self):
        """Test that all fields are optional.

        This test prevents regressions in the model validation, because the
        semantic scholar API occasionally has missing data for arbitrary fields
        in the s2FieldsOfStudy response.
        """
        # Works with empty dict since all fields are now optional
        field = FieldsOfStudy.model_validate({})
        assert field.category is None
        assert field.source is None

        # Works with only category
        field = FieldsOfStudy.model_validate({"category": "Computer Science"})
        assert field.category == "Computer Science"
        assert field.source is None

        # Works with only source
        field = FieldsOfStudy.model_validate({"source": "external"})
        assert field.category is None
        assert field.source == "external"

        # Works with null values
        field = FieldsOfStudy.model_validate({"category": None, "source": None})
        assert field.category is None
        assert field.source is None
