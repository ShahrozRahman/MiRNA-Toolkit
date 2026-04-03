import argparse
import json
import sys
from pathlib import Path
from textwrap import dedent

from . import batch as batch_module
from .pipeline import PipelineConfig, run_end_to_end

EXAMPLES = dedent(
    """
    Examples:
      mirna-toolkit --fastq sample.fastq --reference mirbase.fa --annotation mirbase.gtf
      mirna-toolkit run --fastq sample.fastq --reference mirbase.fa --annotation mirbase.gtf --trim
      mirna-toolkit batch --manifest samples.csv --output-dir batch_runs
      mirna-toolkit help
      mirna-toolkit help run
      mirna-toolkit help batch
    """
).strip()

RUN_HELP = dedent(
    """
    Run a single sample through preprocessing, alignment, quantification, and normalization.

    Required arguments:
      --fastq         Input FASTQ path
      --reference     Reference index or genome directory
      --annotation    Annotation GTF/GFF path

    Useful options:
      --aligner       bowtie | hisat2 | star
      --normalize     tpm | rpm
      --run-qc        Run FastQC before alignment
      --trim          Trim adapters with fastp before alignment
    """
).strip()

BATCH_HELP = dedent(
    """
    Run multiple samples from a CSV or JSON manifest.

    Manifest columns or keys:
      sample_id, fastq_path, reference, annotation, output_dir, aligner,
      normalization_method, threads, run_qc, trim

    Minimal CSV row example:
      sample_id,fastq_path,reference,annotation
      s1,s1.fastq,mirbase.fa,mirbase.gtf
    """
).strip()

HELP_TEXT = dedent(
    f"""
    miRNA-Toolkit command line interface

    Available commands:
      run     Process one sample
      batch   Process multiple samples from a manifest
      help    Show detailed examples and topic-specific usage

    {EXAMPLES}
    """
).strip()


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)

    if not args:
        print(HELP_TEXT)
        return 0

    if args[0] == "help":
        _print_help(args[1] if len(args) > 1 else None)
        return 0

    if args[0] == "batch":
        return _run_batch(args[1:])

    if args[0] == "run":
        return _run_run(args[1:])

    return _run_legacy(args)


def _run_legacy(argv: list[str]) -> int:
    parser = _build_run_parser(prog="mirna-toolkit", description="Run an end-to-end miRNA-Toolkit workflow")
    args = parser.parse_args(argv)
    return _execute_run(args)


def _run_run(argv: list[str]) -> int:
    parser = _build_run_parser(prog="mirna-toolkit run", description="Run an end-to-end miRNA-Toolkit workflow")
    args = parser.parse_args(argv)
    return _execute_run(args)


def _run_batch(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="mirna-toolkit batch",
        description="Run multiple samples from a manifest",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=BATCH_HELP,
    )
    parser.add_argument("--manifest", required=True, help="CSV or JSON manifest path")
    parser.add_argument("--output-dir", default="batch_outputs", help="Base output directory")
    parser.add_argument(
        "--db-versions-json",
        default="",
        help="JSON file mapping database names to versions, for batch metadata",
    )
    args = parser.parse_args(argv)

    db_versions = _load_db_versions(args.db_versions_json)
    result = batch_module.run_batch_workflow(
        args.manifest,
        output_dir=args.output_dir,
        database_versions=db_versions,
    )
    print(result.summary_json_path)
    return 0


def _execute_run(args: argparse.Namespace) -> int:
    db_versions = _load_db_versions(getattr(args, "db_versions_json", ""))

    config = PipelineConfig(
        fastq_path=args.fastq,
        reference=args.reference,
        annotation=args.annotation,
        output_dir=args.output_dir,
        aligner=args.aligner,
        normalization_method=args.normalize,
        threads=args.threads,
        run_qc=args.run_qc,
        trim=args.trim,
    )

    result = run_end_to_end(config, database_versions=db_versions)
    print(result.metadata_path)
    return 0


def _build_run_parser(*, prog: str, description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=prog,
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=RUN_HELP + "\n\n" + EXAMPLES,
    )
    parser.add_argument("--fastq", required=True, help="Input FASTQ path")
    parser.add_argument("--reference", required=True, help="Reference index/path")
    parser.add_argument("--annotation", required=True, help="Annotation GTF/GFF path")
    parser.add_argument("--output-dir", default="outputs", help="Output directory")
    parser.add_argument("--aligner", default="bowtie", choices=["bowtie", "hisat2", "star"])
    parser.add_argument("--normalize", default="tpm", choices=["tpm", "rpm"])
    parser.add_argument("--threads", type=int, default=4)
    parser.add_argument("--run-qc", action="store_true")
    parser.add_argument("--trim", action="store_true")
    parser.add_argument(
        "--db-versions-json",
        default="",
        help="JSON file mapping database names to versions, for run metadata",
    )
    return parser


def _load_db_versions(path_value: str) -> dict[str, str] | None:
    if not path_value:
        return None
    return json.loads(Path(path_value).read_text(encoding="utf-8"))


def _print_help(topic: str | None) -> None:
    if topic == "run":
        print(RUN_HELP)
        print()
        print(EXAMPLES)
        return
    if topic == "batch":
        print(BATCH_HELP)
        print()
        print(EXAMPLES)
        return
    print(HELP_TEXT)


if __name__ == "__main__":
    raise SystemExit(main())
