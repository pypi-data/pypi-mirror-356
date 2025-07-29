# File: api/routes/generation.py

from fastapi import APIRouter, Depends, HTTPException
from canonmap import CanonMap, ArtifactGenerationRequest, ArtifactGenerationResponse
from api.utils.get_canonmap import get_canonmap

router = APIRouter(tags=["generation"])


@router.post(
    "/generate-artifacts/",
    response_model=ArtifactGenerationResponse,
    summary="Generate artifacts (schema, embeddings, canonical entities, etc.)"
)
async def generate_artifacts(
    request: ArtifactGenerationRequest,
    canonmap: CanonMap = Depends(get_canonmap)
):
    """
    Generate artifacts from input data.
    """
    try:
        entity_fields = (
            [ef.model_dump() for ef in request.entity_fields]
            if request.entity_fields else None
        )

        config = ArtifactGenerationRequest(
            input_path=request.input_path,
            output_path=request.output_path,
            source_name=request.source_name,
            table_name=request.table_name,
            normalize_table_names=True,
            recursive=request.recursive,
            file_pattern=request.file_pattern or "*.csv",
            table_name_from_file=request.table_name_from_file,
            entity_fields=entity_fields,
            semantic_fields=request.semantic_fields,
            use_other_fields_as_metadata=request.use_other_fields_as_metadata,
            num_rows=request.num_rows,
            generate_canonical_entities=request.generate_canonical_entities,
            generate_schema=request.generate_schema,
            generate_embeddings=request.generate_embeddings,
            save_processed_data=request.save_processed_data,
            schema_database_type=request.schema_database_type,
            clean_field_names=request.clean_field_names,
            verbose=request.verbose
        )

        result = canonmap.generate(config=config)
        if result is None:
            raise HTTPException(status_code=500, detail="Pipeline returned no result.")
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))