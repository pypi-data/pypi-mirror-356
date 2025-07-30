import logging
import uuid
from typing import Dict, List, Optional

import argilla as rg
import pandas as pd
import pandera as pa
from llama_index.embeddings.openai import OpenAIEmbedding
from tqdm import tqdm

from extralit.convert.json_table import df_to_json
from extralit.extraction.models.paper import PaperExtraction
from extralit.extraction.models.response import ResponseResults

_LOGGER = logging.getLogger(__name__)


def create_extraction_records(
    paper_extractions: Dict[str, PaperExtraction],
    papers: pd.DataFrame,
    responses: Optional[Dict[str, ResponseResults]] = None,
    dataset: rg.Dataset = None,
    metadata: Optional[Dict[str, str]] = None
) -> List[rg.Record]:
    """
    Push the extractions to the Argilla Dataset.

    Args:
        paper_extractions: Dict[str, PaperExtraction], required
            The extractions for each paper.
        papers: pd.DataFrame, required
            The papers dataframe.
        responses: Dict[str, ResponseResults], optional
            The responses for each paper.
        dataset: rg.Dataset, default=None
            The Argilla dataset.
        metadata: Dict[str,str], default=None
            Additional metadata to add to the records.

    Returns:
        List[rg.Record]
    """
    records = []
    for ref, extractions in paper_extractions.items():
        paper = papers.loc[[ref]].iloc[0]

        ### metadata ###
        metadata = metadata or {}
        metadata['reference'] = ref
        if paper.get('id'):
            metadata['doc_id'] = str(paper['id'])
        if paper.get('pmid') is not None and str(paper['pmid']).strip():
            metadata['pmid'] = paper['pmid']
        if paper.get('doi'):
            metadata['doi'] = paper['doi']

        schema_order = extractions.schemas.ordering
        for schema_name, extraction in extractions.items():
            schema = extractions.schemas[schema_name]
            if extraction is None or extraction.empty:
                _LOGGER.warning(f'No {schema_name} extraction for {ref}, generating an empty table.')
                extraction = generate_empty_extraction(schema, size=2)

            ### fields ###
            fields = {
                'extraction': df_to_json(
                    extraction, schema, drop_columns=['publication_ref', 'Group'],
                    metadata={'reference': ref}),
            }

            ref_url = f'datasets/{dataset.id}'
            nav_df = pd.DataFrame(
                [[
                    f'[Step {i}]({ref_url}?_page={i}&_metadata=reference.{ref})' \
                    if step != schema_name else f'Step {i} (here)' \
                    for i, step in enumerate(schema_order, start=1)]],
                columns=schema_order,
                index=pd.Index(['Navigate to']))
            fields['metadata'] = f'Paper: {ref}\n' + nav_df.to_markdown(index=True)

            # Retrieve most relevant context
            if responses and ref in responses and schema_name in responses[ref].items:
                nodes_df = responses[ref].items[schema_name].get_nodes_info()
                nodes_df.drop(columns=nodes_df.columns.difference(['relevance', 'header', 'page_number', 'text']),
                            errors='ignore', inplace=True)
                fields['context'] = nodes_df \
                    .style.background_gradient(axis=1, subset=['relevance'], cmap='RdYlGn') \
                    .to_html(index=False, na_rep='')

            record = rg.Record(
                fields=fields,
                metadata={**metadata, 'type': schema_name},
            )
            records.append(record)

    return records


def create_publication_records(
    papers: pd.DataFrame,
    schema: pa.DataFrameSchema,
    dataset: rg.Dataset,
    embed_model='text-embedding-3-large',
) -> List[rg.Record]:
    """
    Push the publications to the Argilla Dataset.
    """
    assert papers.index.name == 'reference', f"The given dataframe must have index name as 'reference', given {papers.index.name}"
    records = []
    question_names = [q.name for q in dataset.settings.questions]

    embed_models = {}
    if embed_model:
        for vector_field in dataset.settings.vectors:
            embed_models[vector_field.name] = OpenAIEmbedding(
                model=embed_model, dimensions=vector_field.dimensions or 1024)

    for reference, paper in tqdm(papers.iterrows()):
        metadata = {
            'reference': paper.name,
        }

        field_names = [f.name for f in dataset.settings.fields]
        publication_metadata = {k: v for k, v in paper.to_dict().items() \
                              if k in field_names}
        metadata.update(publication_metadata)
        publication_metadata = pd.Series(publication_metadata, name=paper.name)

        fields = {
            **{k: v for k, v in paper.to_dict().items() \
               if k in field_names and not pd.isna(v)},
        }
        if 'metadata' in field_names:
            fields['metadata'] = publication_metadata.to_frame().to_html(index=True)

        vectors = {
            name: model.get_text_embedding(fields[name]) \
            for name, model in embed_models.items() \
            if name in fields and fields[name].strip()
        }

        # Create suggestions
        suggestions = []
        for field in schema.columns:
            if field in question_names and field in paper and paper[field] is not None:
                suggestions.append(
                    rg.Suggestion(
                        question_name=field.lower(),
                        value=str(paper[field]),
                        agent="human"
                    )
                )

        record = rg.Record(
            fields=fields,
            metadata={k: v for k, v in metadata.items() if not pd.isna(v)},
            suggestions=suggestions,
            vectors=vectors,
        )
        records.append(record)

    return records


def generate_empty_extraction(schema: pa.DataFrameSchema, size=2) -> pd.DataFrame:
    default_value = ['NA'] * size
    df = pd.DataFrame.from_dict({col: default_value \
                                 for i, col in enumerate(schema.columns) if i < 5})

    if isinstance(schema.index, pa.MultiIndex):
        index_names = []
        index_prefixes = []
        for index in schema.index.indexes:
            index_names.append(index.name)
            str_startswith_check = next(check for check in index.checks if check.name == 'str_startswith')
            index_prefixes.append(str_startswith_check.statistics['string'])
        index = pd.MultiIndex.from_tuples(
            [tuple(f'{prefix}{i+1}' for prefix in index_prefixes) for i in range(size)],
            names=index_names)
    elif schema.index:
        str_startswith_check = next(check for check in schema.index.checks if check.name == 'str_startswith')
        prefix = str_startswith_check.statistics['string']
        index = pd.Index([f'{prefix}{i+1}' for i in range(size)], name=schema.index.name if schema.index else None)
    else:
        index = None

    if index is not None:
        df = df.set_index(index)

    return df
