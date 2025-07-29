"""
Extract command module.

Handles the 'extract' command for extracting data from documents.
"""

import os
import sys
import json
import click
from pathlib import Path

from invocr.utils.logger import get_logger
from invocr.formats.pdf import extract_invoice_data
from ..common import load_yaml_config

logger = get_logger(__name__)


@click.command(name='extract')
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
@click.option('-c', '--config', 'config_file', type=click.Path(exists=True),
              help='Path to YAML configuration file')
@click.option('-d', '--decision-tree', is_flag=True, help='Use multi-level decision tree for extraction')
@click.option('-o', '--ocr', is_flag=True, help='Use OCR for text extraction')
@click.option('-l', '--languages', help='OCR languages (e.g., en,pl,de)')
@click.option('-v', '--verbose', is_flag=True, help='Enable verbose output')
def extract_command(input_file, output_file, config_file, decision_tree, ocr, languages, verbose):
    """Extract data from document to structured format"""
    try:
        # Load configuration if provided
        config = None
        if config_file:
            config = load_yaml_config(config_file)
            
            # Use config values if command-line options not provided
            if not decision_tree and 'extraction' in config and 'decision_tree' in config['extraction']:
                decision_tree = config['extraction']['decision_tree']
                
            if not ocr and 'extraction' in config and 'use_ocr' in config['extraction']:
                ocr = config['extraction']['use_ocr']
                
            if not languages and 'extraction' in config and 'languages' in config['extraction']:
                languages = ','.join(config['extraction']['languages'])
        
        # Parse languages
        lang_list = None
        if languages:
            lang_list = [lang.strip() for lang in languages.split(',')]
        
        # Extract data - this is a placeholder that will be replaced with
        # more advanced extraction logic using the decision tree and extractors
        invoice_data = extract_invoice_data(
            input_file,  # For now, this is not the correct API, but we'll fix in integration
            rules=None   # Will be replaced with proper extractor selection
        )
        
        # Write output to file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(invoice_data, f, indent=2, default=str)
            
        logger.info(f"Successfully extracted data from {input_file} to {output_file}")
        
    except Exception as e:
        logger.error(f"Extraction error: {str(e)}")
        if verbose:
            import traceback
            logger.error(traceback.format_exc())
        sys.exit(1)
