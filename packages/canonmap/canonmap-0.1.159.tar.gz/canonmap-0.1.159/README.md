# CanonMap

CanonMap is a Python library for generating and managing canonical entity artifacts from various data sources. It provides a streamlined interface for processing data files and generating standardized artifacts that can be used for entity matching and data integration.

## Features

- **Flexible Input Support**: Process data from:
  - CSV/JSON files
  - Directories of data files
  - Pandas DataFrames
  - Python dictionaries

- **Artifact Generation**:
  - Generate canonical entity lists
  - Create database schemas (supports multiple database types)
  - Generate semantic embeddings for entities
  - Clean and standardize field names
  - Process metadata fields

- **Database Support**:
  - DuckDB (default)
  - SQLite
  - BigQuery
  - MariaDB
  - MySQL
  - PostgreSQL

## Installation

```bash
pip install canonmap
```

## Quick Start

```python
from canonmap import (
    CanonMap, 
    ArtifactGenerationRequest, 
    EntityField,
    SemanticField
)

# Initialize CanonMap
canonmap = CanonMap()

# Configure artifact generation
config = ArtifactGenerationRequest(
    input_path="path/to/your/data.csv",
    output_path="path/to/output",
    source_name="my_source",
    table_name="my_table",
    entity_fields=[
        EntityField(table_name="my_table", field_name="name"),
        EntityField(table_name="my_table", field_name="id")
    ],
    semantic_field_objects=[
        SemanticField(table_name="my_table", field_name="description"),
        SemanticField(table_name="my_table", field_name="notes")
    ],
    generate_schema=True,
    generate_embeddings=True
)

# Generate artifacts
results = canonmap.generate(config)
```

## Artifact Generation Example

```python
from canonmap import (
    CanonMap,
    ArtifactGenerationRequest,
    EntityField,
    SemanticField,
    ArtifactGenerationResponse
)

cm = CanonMap()

gen_req = ArtifactGenerationRequest(
    input_path="input",
    output_path="output",
    source_name="football_data",
    entity_fields=[
        EntityField(table_name="passing", field_name="player"),
        EntityField(table_name="rushing", field_name="rusher_name"),
    ],
    semantic_field_objects=[
        SemanticField(table_name="passing", field_name="description"),
        SemanticField(table_name="rushing", field_name="notes"),
    ],
    generate_schema=True,
    save_processed_data=True,
)

resp: ArtifactGenerationResponse = cm.generate(gen_req)
```

## Entity Mapping Example

```python
from canonmap import (
    CanonMap,
    EntityMappingRequest,
    TableFieldFilter,
    EntityMappingResponse
)

cm = CanonMap(artifacts_path="output")

mapping_request = EntityMappingRequest(
    entities=["tim brady", "jake alan"],
    filters=[
        TableFieldFilter(table_name="passing", table_fields=["player"])
    ],
    num_results=3,
)

resp: EntityMappingResponse = cm.map_entities(mapping_request)
```

## Configuration Options

The `ArtifactGenerationRequest` model provides extensive configuration options:

- **Input/Output**:
  - `input_path`: Path to data file/directory or DataFrame/dict
  - `output_path`: Directory for generated artifacts
  - `source_name`: Logical source name
  - `table_name`: Logical table name

- **Directory Processing**:
  - `recursive`: Process subdirectories
  - `file_pattern`: File matching pattern (e.g., "*.csv")
  - `table_name_from_file`: Use filename as table name

- **Entity Processing**:
  - `entity_fields`: List of fields to treat as entities
  - `semantic_field_objects`: List of fields to extract as individual semantic text files
  - `use_other_fields_as_metadata`: Include non-entity fields as metadata

- **Generation Options**:
  - `generate_canonical_entities`: Generate entity list
  - `generate_schema`: Generate database schema
  - `generate_embeddings`: Generate semantic embeddings
  - `save_processed_data`: Save cleaned data
  - `schema_database_type`: Target database type
  - `clean_field_names`: Standardize field names

## Output

The `generate()` method returns a dictionary containing:
- Generated artifacts
- Paths to saved files
- Schema information (if requested)
- Embeddings (if requested)
- Processed data (if requested)
- Semantic text files (if `semantic_field_objects` specified)

### Semantic Text Files

When `semantic_field_objects` is specified, CanonMap creates zip files containing individual text files for each non-null semantic field value:

- **Single table**: `{source}_{table}_semantic_texts.zip`
- **Multiple tables**: `{source}_semantic_texts.zip` (combined)
- **File naming**: `{table_name}_row_{row_index}_{field_name}.txt`
- **Content**: Raw text content from the specified semantic fields

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 