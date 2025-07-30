#!/usr/bin/env python3

import argparse
import json
import logging
import sys
from pathlib import Path

from sorrydb.agents.json_agent import JsonAgent
from sorrydb.agents.llm_strategy import LLMStrategy


def main():
    parser = argparse.ArgumentParser(description="Solve sorries using LLM.")
    parser.add_argument(
        "--sorry-file",
        type=str,
        required=True,
        help="Path to the sorry JSON file",
    )
    parser.add_argument(
        "--output-file",
        type=str,
        required=True,
        help="Path to the output JSON file",
    )
    parser.add_argument(
        "--model-json",
        type=str,
        default=None,
        help="Path to the model config JSON file (default: None)",
    )
    parser.add_argument(
        "--lean-data",
        type=str,
        default=None,
        help="Directory to store Lean data (default: use temporary directory)",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level (default: INFO)",
    )
    parser.add_argument(
        "--log-file", type=str, help="Log file path (default: output to stdout)"
    )

    args = parser.parse_args()

    # Configure logging
    log_kwargs = {
        "level": getattr(logging, args.log_level),
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    }
    if args.log_file:
        log_kwargs["filename"] = args.log_file
    logging.basicConfig(**log_kwargs)

    logger = logging.getLogger(__name__)

    # Convert file names arguments to Path
    sorry_file = Path(args.sorry_file)
    output_file = Path(args.output_file)
    lean_data = Path(args.lean_data) if args.lean_data else None

    # Load model config if provided
    model_config = None
    if args.model_json:
        try:
            with open(args.model_json) as f:
                model_config = json.load(f)
        except FileNotFoundError as e:
            logger.error(f"Model config file not found: {e}")
            return 1
        except json.JSONDecodeError as e:
            logger.error(f"Invalid model config JSON: {e}")
            return 1

    # Process the sorry JSON file
    try:
        logger.info(f"Solving sorries from: {sorry_file} using llm")
        llm_strategy = LLMStrategy(model_config)
        llm_agent = JsonAgent(llm_strategy, lean_data)
        llm_agent.process_sorries(sorry_file, output_file)
        return 0

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        return 1
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON: {e}")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        logger.exception(e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
