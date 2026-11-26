# tests/test_consensus_formatter_3.py

from datetime import datetime, timedelta
from typing import List, Dict

import pytest

from swarmforge.backoff_validator import BackoffValidator
from swarmforge.consensus_stats import ConsensusStats
from swarmforge.string_normalizer import StringNormalizer
from swarmforge.consensus_formatter_3 import ConsensusFormatter

def test_format_consensus_stats():
    # Arrange
    backoff_validator = BackoffValidator()
    string_normalizer = StringNormalizer()
    consensus_stats = ConsensusStats(
        messages=["msg1", "msg2", "msg3"],
        duration_seconds=10.5,
        throughput=2.3,
    )
    consensus_formatter = ConsensusFormatter(backoff_validator, string_normalizer)

    # Act
    result = consensus_formatter.format_consensus_stats(consensus_stats)

    # Assert
    assert "Consensus Stats:" in result
    assert "Messages: 3" in result
    assert "Backoff Validated: True" in result  # assume backoff_validator says they're all valid
    assert "Consensus Duration: 10.50 seconds" in result
    assert "Throughput: 2.30 messages/second" in result

def test_format_consensus_divergence():
    # Arrange
    string_normalizer = StringNormalizer()
    divergences: List[Dict[str, str]] = [
        {"source": "src1", "destination": "dest1"},
        {"source": "src2", "destination": "dest2"},
    ]
    consensus_formatter = ConsensusFormatter(None, string_normalizer)

    # Act
    result = consensus_formatter.format_consensus_divergence(divergences)

    # Assert
    assert "Consensus Divergence:" in result
    assert "  1. src1 -> dest1" in result
    assert "  2. src2 -> dest2" in result

def test_format_consensus_divergence_empty():
    # Arrange
    string_normalizer = StringNormalizer()
    divergences: List[Dict[str, str]] = []
    consensus_formatter = ConsensusFormatter(None, string_normalizer)

    # Act
    result = consensus_formatter.format_consensus_divergence(divergences)

    # Assert
    assert "Consensus Divergence:" in result
    assert "  1. " not in result
