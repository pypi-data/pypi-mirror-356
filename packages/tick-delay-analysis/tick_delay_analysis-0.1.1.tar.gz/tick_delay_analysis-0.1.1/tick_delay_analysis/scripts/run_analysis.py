import argparse
import os
from tick_delay_analysis.core import process_all as process_core
from tick_delay_analysis.summary import summarize_all as process_summary

def main():
    parser = argparse.ArgumentParser(description="Run tick delay analysis.")
    parser.add_argument("--mode", type=str, choices=["core", "summary"], required=True,
                        help="Select mode: 'core' to run tick-level delay analysis, 'summary' to generate summary stats.")
    parser.add_argument("--input_dir", type=str, required=True,
                        help="Input directory containing CSV files.")
    parser.add_argument("--output_dir", type=str, required=False,
                        help="Output directory to save results.")

    args = parser.parse_args()

    if args.mode == "core":
        if not args.output_dir:
            raise ValueError("--output_dir must be specified when running in 'core' mode.")
        process_core(args.input_dir, args.output_dir)
    elif args.mode == "summary":
        process_summary(args.input_dir)

if __name__ == "__main__":
    main()
