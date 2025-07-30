import typing

from ...annotation import AnnotationPredicate
from ...version import VersionDescriptor
from .base import CatalogBase
from .base import SearchResult
from agentc_core.record.descriptor import RecordDescriptor


class CatalogChain(CatalogBase):
    """Represents a chain of catalogs, where all catalogs are searched
    during find(), but results from earlier catalogs take precedence."""

    chain: list[CatalogBase]

    def __init__(self, *chain: CatalogBase):
        self.chain = chain if chain is not None else []

    def find(
        self,
        query: str = None,
        name: str = None,
        snapshot: str = None,
        limit: typing.Union[int | None] = 1,
        annotations: AnnotationPredicate = None,
    ) -> list[SearchResult]:
        results = []

        seen = set()  # Keyed by 'source:name'.

        for c in self.chain:
            results_c = c.find(query=query, name=name, snapshot=snapshot, limit=limit, annotations=annotations)

            for x in results_c:
                source_name = str(x.entry.source) + ":" + x.entry.name

                if source_name not in seen:
                    seen.add(source_name)
                    results.append(x)

        if limit > 0:
            results = results[:limit]

        return results

    def __iter__(self) -> typing.Iterator[RecordDescriptor]:
        """Returns unique catalog items after aggregating results from both local,db and removing duplicates."""
        seen = set()  # Keyed by 'source:name'
        for catalog in self.chain:
            catalog_items = list(catalog)
            for item in catalog_items:
                source_name = str(item.source) + ":" + item.name
                if source_name not in seen:
                    seen.add(source_name)
                    yield item

    @property
    def version(self) -> VersionDescriptor:
        return self.chain[0].version
