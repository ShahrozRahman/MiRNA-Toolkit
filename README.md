# miRNA-Toolkit

miRNA-Toolkit is a Python-native library for end-to-end miRNA analysis, including preprocessing, alignment, quantification, target prediction, disease association, and visualization.

Install name: `mirna-toolkit`
Import name: `mirna_toolkit`

## Features

- I/O support for FASTQ, FASTA, BAM, and GTF/GFF-oriented workflows.
- Wrappers for FastQC, fastp, Bowtie, HISAT2, and STAR (small-RNA mode).
- Quantification and normalization (TPM, RPM, DESeq2-style size factors).
- Target prediction (seed match + RNAhybrid-style scoring + external connectors).
- Disease association integration (HMDD, miRCancer) and network export.
- Visualization utilities for interaction networks, heatmaps, volcano plots, and pathway enrichment plots.
- Optional ML utilities for classification, feature ranking, and explainability.
- End-to-end reproducible workflow runner (`pipeline.run_end_to_end`) and CLI (`mirna-toolkit`).
- Manifest-based batch workflow for multiple samples (`batch.run_batch_workflow`).
- Retry-aware HTTP connectors with configurable strict mode for robust integrations.

## Installation

```bash
pip install mirna-toolkit
```

For local development:

```bash
pip install -e .
```

Optional extras:

```bash
pip install -e .[full,dev]
```

## Quick Start

```python
from mirna_toolkit import alignment, quantification, prediction, disease, visualization

bam_file = alignment.bowtie.align("sample.fastq", reference="mirbase.fa")
counts = quantification.counts.from_bam(bam_file, annotation="mirbase.gtf")
normalized = quantification.normalization.tpm(counts)

targets = prediction.targetscan_api.get_targets("hsa-miR-21")
assoc = disease.hmdd.get_associations("hsa-miR-21")

fig = visualization.networks.plot_mirna_targets("hsa-miR-21", targets)
fig.show()
```

## End-to-End Pipeline

```python
from mirna_toolkit.pipeline import PipelineConfig, run_end_to_end

config = PipelineConfig(
	fastq_path="sample.fastq",
	reference="mirbase_index",
	annotation="mirbase.gtf",
	output_dir="run_001",
	aligner="bowtie",
	normalization_method="tpm",
	run_qc=True,
	trim=True,
)

result = run_end_to_end(config, database_versions={"miRBase": "22.1", "TargetScan": "8.0"})
print(result.metadata_path)
```

## CLI

```bash
mirna-toolkit --fastq sample.fastq --reference mirbase_index --annotation mirbase.gtf --output-dir run_001 --aligner bowtie --normalize tpm --run-qc --trim
```

Helpful CLI topics:

```bash
mirna-toolkit help
mirna-toolkit help run
mirna-toolkit help batch
```

## Batch Workflow

Manifest example (`samples.csv`):

```csv
sample_id,fastq_path,reference,annotation,run_qc,trim
s1,s1.fastq,mirbase_index,mirbase.gtf,true,true
s2,s2.fastq,mirbase_index,mirbase.gtf,false,false
```

Run it with:

```bash
mirna-toolkit batch --manifest samples.csv --output-dir batch_runs
```

## Reproducibility

Use `mirna_toolkit.utils.versioning.DatabaseVersionTracker` to record exact versions/releases of external databases used in analyses.

## Status

This repository provides a production-ready scaffold with working core APIs and wrappers. External command wrappers require the corresponding tools (for example, `bowtie`, `fastqc`, `fastp`) to be installed and available on `PATH`.
