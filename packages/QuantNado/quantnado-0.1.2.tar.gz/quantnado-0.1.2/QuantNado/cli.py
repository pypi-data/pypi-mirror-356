import argparse
import sys
from pathlib import Path

from loguru import logger

from .core import call_peaks_from_bigwig_dir


def main():
    parser = argparse.ArgumentParser(
        description="Call quantile-based peaks from all bigWig files in a directory."
    )
    parser.add_argument(
        "--bigwig-dir",
        required=True,
        help="Path to directory containing .bw or .bigWig files",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Directory to write output BED files and logs",
    )
    parser.add_argument(
        "--chromsizes",
        required=True,
        help="Path to a chrom.sizes file (tab-delimited with columns: chromosome name and size)",
    )
    parser.add_argument(
        "--blacklist",
        default=None,
        help="Optional BED file with blacklist regions to exclude from analysis",
    )
    parser.add_argument(
        "--tilesize",
        type=int,
        default=128,
        help="Tile size in base pairs for genome tiling (default: 128)",
    )
    parser.add_argument(
        "--quantile",
        type=float,
        default=0.98,
        help="Quantile threshold for peak calling (default: 0.98)",
    )
    parser.add_argument(
        "--merge",
        type=bool,
        default=False,
        help="Merge adjacent/overlapping peak tiles before filtering by length (default: False)",
    )
    parser.add_argument(
        "--tmp-dir",
        default="tmp",
        help="Directory to store temporary files (default: tmp)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging to stderr (level=DEBUG)",
    )
    args = parser.parse_args()

    # Configure logging
    logger.remove()
    log_format = "{time:YYYY-MM-DD HH:mm:ss} [{level}] {message}"
    log_path = Path(args.output_dir) / "quantnado_run.log"
    logger.add(log_path, level="DEBUG", format=log_format)
    logger.add(sys.stderr, level="DEBUG" if args.verbose else "INFO", format=log_format)

    result = call_peaks_from_bigwig_dir(
        bigwig_dir=args.bigwig_dir,
        output_dir=args.output_dir,
        chromsizes_file=args.chromsizes,
        blacklist_file=args.blacklist,
        tilesize=args.tilesize,
        quantile=args.quantile,
        tmp_dir=args.tmp_dir,
    )

    return 0 if result else 1
