# miRNA-Toolkit Architecture

## Modules

- `mirna_toolkit.io`: File adapters, conversion wrappers, and data download connectors.
- `mirna_toolkit.alignment`: Bowtie/HISAT2/STAR wrappers for small-RNA alignments.
- `mirna_toolkit.quantification`: BAM read counting, normalization, and novel miRNA candidate discovery.
- `mirna_toolkit.prediction`: Seed matching, thermodynamic proxy scoring, external target APIs, score fusion.
- `mirna_toolkit.disease`: HMDD/miRCancer association access and export utilities.
- `mirna_toolkit.visualization`: Plotly/network-based visual analytics.
- `mirna_toolkit.ml`: Optional machine-learning pipelines and explainability.
- `mirna_toolkit.utils`: Logging, config, plugin registration, and reproducibility metadata.
- `mirna_toolkit.pipeline`: End-to-end run orchestration with artifact and metadata export.
- `mirna_toolkit.cli`: Command-line entry point for reproducible workflow execution.

## Reproducibility Notes

Store all external database versions used during an analysis through `DatabaseVersionTracker` and export to JSON with each run.
External HTTP connectors are retry-enabled and support strict/non-strict error handling via shared utilities.

## Performance Notes

- Core functions are vectorized where possible.
- Wrappers rely on compiled external tools for large read datasets.
- ML and BAM parsing extras are optional to keep base install lightweight.
