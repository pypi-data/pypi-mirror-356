import argparse
import logging
import sys

import yaml

from .actions.filter_endpoints import Method, filter_endpoint
from .actions.filter_paths_by_tags import filter_paths_by_tags
from .actions.filter_schemas import filter_schemas, get_referenced_schemas
from .actions.filter_tags_list import filter_tags_list
from .actions.remove_properties import remove_properties
from .settings import AppConfig


def setup_logging(verbose=False):
    """Configure logging with appropriate level and format."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def main():
    parser = argparse.ArgumentParser(
        description="Modify an OpenAPI specification YAML doc for OpenAI's API."
    )
    parser.add_argument("input_file", help="Path to the input OpenAPI YAML file.")
    parser.add_argument(
        "-c",
        "--config",
        dest="config_file",
        required=True,
        help="Path to the configuration JSON file.",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output_file",
        help="Path to the output file. If not provided, output is written to stdout.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose (DEBUG) logging",
    )
    args = parser.parse_args()

    # Setup logging
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    logger.info("Starting OpenAPI specification modification")
    logger.debug(f"Input file: {args.input_file}")
    logger.debug(f"Config file: {args.config_file}")
    logger.debug(
        f"Output destination: {'stdout' if not args.output_file else args.output_file}"
    )

    # Read config file
    try:
        logger.debug(f"Loading configuration from {args.config_file}")
        config = AppConfig.from_file(args.config_file)
        logger.debug("Successfully loaded configuration")
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        sys.exit(1)

    # Read the input YAML file
    try:
        logger.debug("Reading input YAML file")
        with open(args.input_file, "r") as f:
            yaml_content = f.read()
        logger.debug(f"Successfully read {len(yaml_content)} bytes from input file")
    except Exception as e:
        logger.error(f"Error reading input file: {e}")
        sys.exit(1)

    # Parse YAML
    try:
        logger.debug("Parsing YAML content")
        data = yaml.safe_load(yaml_content)
        logger.debug("Successfully parsed YAML content")
    except Exception as e:
        logger.error(f"Error parsing YAML: {e}")
        sys.exit(1)

    # Remove all 'x-oaiMeta' properties
    if config.properties_to_remove:
        logger.info(
            f"Removing properties: {', '.join(sorted(config.properties_to_remove))}"
        )
        data = remove_properties(data, config.properties_to_remove)

    allowed_tags = config.allowed_tags

    # Filter paths by allowed tags
    logger.info(f"Filtering paths by tags: {', '.join(sorted(allowed_tags))}")
    data = filter_paths_by_tags(data, allowed_tags)
    # Filter top-level tags list
    logger.info("Filtering top-level tags list")
    data = filter_tags_list(data, allowed_tags)

    # Filter specific endpoints based on config
    logger.info("Filtering specific endpoints based on configuration")
    for path, path_filter in config.path_filters.items():
        methods_to_keep = [Method(m.lower()) for m in path_filter.allowed_methods]
        if methods_to_keep:
            logger.debug(
                f"Filtering path '{path}', keeping methods: {[m.upper() for m in path_filter.allowed_methods]}"
            )
        else:
            logger.debug(f"Removing path '{path}'")
        data = filter_endpoint(
            data,
            path,
            methods_to_keep,
        )

    # Remove unreferenced schemas
    if config.options.remove_unreferenced_schemas:
        logger.info("Removing unreferenced schemas")
        referenced_schemas = get_referenced_schemas(data)
        logger.debug(f"Found {len(referenced_schemas)} referenced schemas")
        data = filter_schemas(data, referenced_schemas)

    # Dump YAML
    try:
        logger.debug("Converting modified data back to YAML")
        output_yaml = yaml.safe_dump(data, sort_keys=False, allow_unicode=True)
        logger.debug(f"Generated {len(output_yaml)} bytes of YAML output")
    except Exception as e:
        logger.error(f"Error dumping YAML: {e}")
        sys.exit(1)

    # Write to output file or stdout
    if args.output_file:
        try:
            logger.info(f"Writing output to file: {args.output_file}")
            with open(args.output_file, "w") as f:
                f.write(output_yaml)
            logger.info("Successfully wrote output file")
        except Exception as e:
            logger.error(f"Error writing to output file: {e}")
            sys.exit(1)
    else:
        logger.info("Writing output to stdout")
        print(output_yaml)

    logger.info("OpenAPI specification modification completed")


if __name__ == "__main__":
    main()
