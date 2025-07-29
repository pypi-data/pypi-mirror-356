from collections.abc import Iterable
from http import HTTPStatus
from logging import getLogger

from wowool.common.pipeline.objects import UUID
from wowool.document import Document
from wowool.document.analysis.document import AnalysisDocument
from wowool.document.document_interface import DocumentInterface
from wowool.document.serialize import serialize

from wowool.portal.client.portal import Portal


logger = getLogger(__name__)

PipelineSteps = str | list[str | dict | UUID]


class Pipeline:
    """
    :class:`Pipeline` is a class used to process your documents.
    """

    def __init__(self, steps: PipelineSteps, portal: Portal | None = None):
        """
        Initialize a Pipeline instance

        :param steps: A list of steps to process the document. Each step can be a string, a dictionary, or a UUID object.
        :param portal: Connection to the Portal server

        :return: An initialized pipeline
        :rtype: :class:`Pipeline`
        """
        self._portal = portal or Portal()
        self._steps = steps  # _parse_steps(steps)

    @property
    def steps(self):
        return self._steps

    def process(
        self,
        document: DocumentInterface | str,
        id: str | None = None,
        metadata: dict | None = None,
        **request_kwargs,
    ) -> AnalysisDocument:
        """
        Functor to process one document. For example:

        .. literalinclude:: init_pipeline_context.py
            :language: python

        :param document: Input document to process. This includes support for one of the :ref:`InputProviders <py_eot_wowool_io_input_providers>`
        :type document: Either a ``str`` or :class:`Document <wowool.document.Document>`, :class:`InputProvider <wowool.io.InputProvider>`
        :param id: The ID you wish to associate with the document. By default, if a file is passed, the file's name is used. Similarly, if a string is passed, a hash of the string is used
        :type id: ``str``
        :param kwargs: additional for the requests library


        :return: :class:`Document <wowool.document.Document>` an instance is returned
        """
        input_document = Document(id=id, data=document, metadata=metadata or {}) if isinstance(document, str) else document
        input_document_raw = serialize(input_document)
        analysis_document_raw = self._portal._service.post(
            url="pipelines/process",
            status_code=HTTPStatus.OK,
            data={
                "pipeline": self.steps,
                "document": input_document_raw,
            },
            **request_kwargs,
        )
        analysis_document = AnalysisDocument.from_dict(analysis_document_raw)
        return analysis_document

    def process_batch(self, documents: Iterable[DocumentInterface | str], **request_kwargs) -> list[AnalysisDocument]:
        """
        Functor to process a batch of documents. For example:

        .. literalinclude:: init_pipeline_context.py
            :language: python

        :param data: Input data to process. This includes support for one of the :ref:`InputProviders <py_eot_wowool_io_input_providers>`
        :param kwargs: additional kw arguments for the requests library

        :return: A ``list`` of :class:`Document <wowool.document.Document>` instances is returned.
        """
        input_documents = [Document(data=document) if isinstance(document, str) else document for document in documents]
        input_documents_raw = [serialize(doc) for doc in input_documents]
        analysis_documents_raw = self._portal._service.post(
            url="pipelines/process/batch",
            status_code=HTTPStatus.OK,
            data={
                "pipeline": self.steps,
                "documents": input_documents_raw,
            },
            **request_kwargs,
        )
        analysis_documents = [AnalysisDocument.from_dict(analysis_document_raw) for analysis_document_raw in analysis_documents_raw]
        return analysis_documents

    def __call__(self, document_or_documents, **kwargs) -> AnalysisDocument | list[AnalysisDocument]:
        return (
            self.process_batch(document_or_documents, **kwargs)
            if isinstance(document_or_documents, Iterable)
            else self.process(document_or_documents, **kwargs)
        )

    def __eq__(self, other: object):
        if not isinstance(other, Pipeline):
            return False
        return self.steps == other.steps

    def __repr__(self):
        return f"""wowool.portal.Pipeline(steps="{self.steps}")"""
