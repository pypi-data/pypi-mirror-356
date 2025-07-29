# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Helper functions for the Cost Explorer MCP server."""

import boto3
import os
import re
import sys
from datetime import datetime
from loguru import logger
from typing import Any, Dict, Optional, Tuple


# Configure Loguru logging
logger.remove()
logger.add(sys.stderr, level=os.getenv('FASTMCP_LOG_LEVEL', 'WARNING'))

# Global client cache
_cost_explorer_client = None


def get_cost_explorer_client():
    """Get Cost Explorer client with proper session management and caching.

    Returns:
        boto3.client: Configured Cost Explorer client (cached after first call)
    """
    global _cost_explorer_client

    if _cost_explorer_client is None:
        try:
            # Read environment variables dynamically
            aws_region = os.environ.get('AWS_REGION', 'us-east-1')
            aws_profile = os.environ.get('AWS_PROFILE')

            if aws_profile:
                _cost_explorer_client = boto3.Session(
                    profile_name=aws_profile, region_name=aws_region
                ).client('ce')
            else:
                _cost_explorer_client = boto3.Session(region_name=aws_region).client('ce')
        except Exception as e:
            logger.error(f'Error creating Cost Explorer client: {str(e)}')
            raise

    return _cost_explorer_client


def validate_date_format(date_str: str) -> Tuple[bool, str]:
    """Validate that a date string is in YYYY-MM-DD format and is a valid date.

    Args:
        date_str: The date string to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check format with regex
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
        return False, f"Date '{date_str}' is not in YYYY-MM-DD format"

    # Check if it's a valid date
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True, ''
    except ValueError as e:
        return False, f"Invalid date '{date_str}': {str(e)}"


def format_date_for_api(date_str: str, granularity: str) -> str:
    """Format date string appropriately for AWS Cost Explorer API based on granularity.

    Args:
        date_str: Date string in YYYY-MM-DD format
        granularity: The granularity (DAILY, MONTHLY, HOURLY)

    Returns:
        Formatted date string appropriate for the API call
    """
    if granularity.upper() == 'HOURLY':
        # For hourly granularity, AWS expects datetime format
        # Convert YYYY-MM-DD to YYYY-MM-DDTHH:MM:SSZ
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        return dt.strftime('%Y-%m-%dT00:00:00Z')
    else:
        # For DAILY and MONTHLY, use the original date format
        return date_str


def validate_date_range(
    start_date: str, end_date: str, granularity: Optional[str] = None
) -> Tuple[bool, str]:
    """Validate date range with format and logical checks.

    Args:
        start_date: The start date string in YYYY-MM-DD format
        end_date: The end date string in YYYY-MM-DD format
        granularity: Optional granularity to check specific constraints

    Returns:
        Tuple of (is_valid, error_message)
    """
    # Validate start date format
    is_valid_start, error_start = validate_date_format(start_date)
    if not is_valid_start:
        return False, error_start

    # Validate end date format
    is_valid_end, error_end = validate_date_format(end_date)
    if not is_valid_end:
        return False, error_end

    # Validate date range logic
    start_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_dt = datetime.strptime(end_date, '%Y-%m-%d')
    if start_dt > end_dt:
        return False, f"Start date '{start_date}' cannot be after end date '{end_date}'"

    # Validate granularity-specific constraints
    if granularity and granularity.upper() == 'HOURLY':
        # HOURLY granularity supports maximum 14 days
        date_diff = (end_dt - start_dt).days
        if date_diff > 14:
            return (
                False,
                f'HOURLY granularity supports a maximum of 14 days. Current range is {date_diff} days ({start_date} to {end_date}). Please use a shorter date range.',
            )

    return True, ''


def get_dimension_values(
    key: str, billing_period_start: str, billing_period_end: str
) -> Dict[str, Any]:
    """Get available values for a specific dimension."""
    # Validate date range (no granularity constraint for dimension values)
    is_valid, error_message = validate_date_range(billing_period_start, billing_period_end)
    if not is_valid:
        return {'error': error_message}

    try:
        ce = get_cost_explorer_client()
        response = ce.get_dimension_values(
            TimePeriod={'Start': billing_period_start, 'End': billing_period_end},
            Dimension=key.upper(),
        )
        dimension_values = response['DimensionValues']
        values = [value['Value'] for value in dimension_values]
        return {'dimension': key.upper(), 'values': values}
    except Exception as e:
        logger.error(
            f'Error getting dimension values for {key.upper()} ({billing_period_start} to {billing_period_end}): {e}'
        )
        return {'error': str(e)}


def get_tag_values(
    tag_key: str, billing_period_start: str, billing_period_end: str
) -> Dict[str, Any]:
    """Get available values for a specific tag key."""
    # Validate date range (no granularity constraint for tag values)
    is_valid, error_message = validate_date_range(billing_period_start, billing_period_end)
    if not is_valid:
        return {'error': error_message}

    try:
        ce = get_cost_explorer_client()
        response = ce.get_tags(
            TimePeriod={'Start': billing_period_start, 'End': billing_period_end},
            TagKey=tag_key,
        )
        tag_values = response['Tags']
        return {'tag_key': tag_key, 'values': tag_values}
    except Exception as e:
        logger.error(
            f'Error getting tag values for {tag_key} ({billing_period_start} to {billing_period_end}): {e}'
        )
        return {'error': str(e)}


def validate_match_options(match_options: list, filter_type: str) -> Dict[str, Any]:
    """Validate MatchOptions based on filter type.

    Args:
        match_options: List of match options to validate
        filter_type: Type of filter ('Dimensions', 'Tags', 'CostCategories')

    Returns:
        Empty dictionary if valid, or an error dictionary
    """
    if filter_type == 'Dimensions':
        valid_options = ['EQUALS', 'CASE_SENSITIVE']
    elif filter_type in ['Tags', 'CostCategories']:
        valid_options = ['EQUALS', 'ABSENT', 'CASE_SENSITIVE']
    else:
        return {'error': f'Unknown filter type: {filter_type}'}

    for option in match_options:
        if option not in valid_options:
            return {
                'error': f"Invalid MatchOption '{option}' for {filter_type}. Valid values are: {valid_options}"
            }

    return {}


def validate_expression(
    expression: Dict[str, Any], billing_period_start: str, billing_period_end: str
) -> Dict[str, Any]:
    """Recursively validate the filter expression.

    Args:
        expression: The filter expression to validate
        billing_period_start: Start date of the billing period
        billing_period_end: End date of the billing period

    Returns:
        Empty dictionary if valid, or an error dictionary
    """
    # Validate date range (no granularity constraint for filter validation)
    is_valid, error_message = validate_date_range(billing_period_start, billing_period_end)
    if not is_valid:
        return {'error': error_message}

    try:
        if 'Dimensions' in expression:
            dimension = expression['Dimensions']
            if (
                'Key' not in dimension
                or 'Values' not in dimension
                or 'MatchOptions' not in dimension
            ):
                return {
                    'error': 'Dimensions filter must include "Key", "Values", and "MatchOptions".'
                }

            # Validate MatchOptions for Dimensions
            match_options_result = validate_match_options(dimension['MatchOptions'], 'Dimensions')
            if 'error' in match_options_result:
                return match_options_result

            dimension_key = dimension['Key']
            dimension_values = dimension['Values']
            valid_values_response = get_dimension_values(
                dimension_key, billing_period_start, billing_period_end
            )
            if 'error' in valid_values_response:
                return {'error': valid_values_response['error']}
            valid_values = valid_values_response['values']
            for value in dimension_values:
                if value not in valid_values:
                    return {
                        'error': f"Invalid value '{value}' for dimension '{dimension_key}'. Valid values are: {valid_values}"
                    }

        if 'Tags' in expression:
            tag = expression['Tags']
            if 'Key' not in tag or 'Values' not in tag or 'MatchOptions' not in tag:
                return {'error': 'Tags filter must include "Key", "Values", and "MatchOptions".'}

            # Validate MatchOptions for Tags
            match_options_result = validate_match_options(tag['MatchOptions'], 'Tags')
            if 'error' in match_options_result:
                return match_options_result

            tag_key = tag['Key']
            tag_values = tag['Values']
            valid_tag_values_response = get_tag_values(
                tag_key, billing_period_start, billing_period_end
            )
            if 'error' in valid_tag_values_response:
                return {'error': valid_tag_values_response['error']}
            valid_tag_values = valid_tag_values_response['values']
            for value in tag_values:
                if value not in valid_tag_values:
                    return {
                        'error': f"Invalid value '{value}' for tag '{tag_key}'. Valid values are: {valid_tag_values}"
                    }

        if 'CostCategories' in expression:
            cost_category = expression['CostCategories']
            if (
                'Key' not in cost_category
                or 'Values' not in cost_category
                or 'MatchOptions' not in cost_category
            ):
                return {
                    'error': 'CostCategories filter must include "Key", "Values", and "MatchOptions".'
                }

            # Validate MatchOptions for CostCategories
            match_options_result = validate_match_options(
                cost_category['MatchOptions'], 'CostCategories'
            )
            if 'error' in match_options_result:
                return match_options_result

        logical_operators = ['And', 'Or', 'Not']
        logical_count = sum(1 for op in logical_operators if op in expression)

        if logical_count > 1:
            return {
                'error': 'Only one logical operator (And, Or, Not) is allowed per expression in filter parameter.'
            }

        if logical_count == 0 and len(expression) > 1:
            return {
                'error': 'Filter parameter with multiple expressions require a logical operator (And, Or, Not).'
            }

        if 'And' in expression:
            if not isinstance(expression['And'], list):
                return {'error': 'And expression must be a list of expressions.'}
            for sub_expression in expression['And']:
                result = validate_expression(
                    sub_expression, billing_period_start, billing_period_end
                )
                if 'error' in result:
                    return result

        if 'Or' in expression:
            if not isinstance(expression['Or'], list):
                return {'error': 'Or expression must be a list of expressions.'}
            for sub_expression in expression['Or']:
                result = validate_expression(
                    sub_expression, billing_period_start, billing_period_end
                )
                if 'error' in result:
                    return result

        if 'Not' in expression:
            if not isinstance(expression['Not'], dict):
                return {'error': 'Not expression must be a single expression.'}
            result = validate_expression(
                expression['Not'], billing_period_start, billing_period_end
            )
            if 'error' in result:
                return result

        if not any(
            k in expression for k in ['Dimensions', 'Tags', 'CostCategories', 'And', 'Or', 'Not']
        ):
            return {
                'error': 'Filter Expression must include at least one of the following keys: "Dimensions", "Tags", "CostCategories", "And", "Or", "Not".'
            }

        return {}
    except Exception as e:
        return {'error': f'Error validating expression: {str(e)}'}


def validate_group_by(group_by: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Validate the group_by parameter.

    Args:
        group_by: The group_by dictionary to validate

    Returns:
        Empty dictionary if valid, or an error dictionary
    """
    try:
        if (
            group_by is None
            or not isinstance(group_by, dict)
            or 'Type' not in group_by
            or 'Key' not in group_by
        ):
            return {'error': 'group_by must be a dictionary with "Type" and "Key" keys.'}

        if group_by['Type'].upper() not in ['DIMENSION', 'TAG', 'COST_CATEGORY']:
            return {
                'error': 'Invalid group Type. Valid types are DIMENSION, TAG, and COST_CATEGORY.'
            }

        return {}
    except Exception as e:
        return {'error': f'Error validating group_by: {str(e)}'}
