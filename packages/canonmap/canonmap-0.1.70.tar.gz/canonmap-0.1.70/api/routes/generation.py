# File: api/routes/generation.py

from fastapi import APIRouter, HTTPException
from canonmap import CanonMap
from canonmap.models.artifact_generation_request import ArtifactGenerationRequest
from canonmap.models.artifact_generation_response import ArtifactGenerationResponse as GenerateResponse
from api.models.artifact_generation_request_api import ArtifactGenerationRequestAPI

router = APIRouter(tags=["generation"])


@router.post("/generate-artifacts/", response_model=GenerateResponse)
async def generate_artifacts(request: ArtifactGenerationRequestAPI):
    """
    Generate artifacts from input data.
    Supports both single file and multi-table processing.
    """
    try:
        # Convert API model to internal model-compatible format
        entity_fields_converted = (
            [ef.model_dump() for ef in request.entity_fields]
            if request.entity_fields else None
        )

        config = ArtifactGenerationRequest(
            input_path=request.input_path,
            output_path=request.output_path,
            source_name=request.source_name,
            table_name=request.table_name,
            entity_fields=entity_fields_converted,
            semantic_fields=request.semantic_fields,
            use_other_fields_as_metadata=request.use_other_fields_as_metadata,
            num_rows=request.num_rows,
            generate_canonical_entities=request.generate_canonical_entities,
            generate_schema=request.generate_schema,
            generate_embeddings=request.generate_embeddings,
            save_processed_data=request.save_processed_data,
            schema_database_type=request.schema_database_type,
            clean_field_names=request.clean_field_names,
            verbose=request.verbose,
            # Add new multi-table processing fields
            recursive=request.recursive,
            file_pattern=request.file_pattern,
            table_name_from_file=request.table_name_from_file
        )

        canonmap = CanonMap()
        result = canonmap.generate(config=config)
        if result is None:
            raise HTTPException(status_code=500, detail="Pipeline returned no result.")
        import logging
        logging.info(f"RESULT: {result}")
        return result

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))