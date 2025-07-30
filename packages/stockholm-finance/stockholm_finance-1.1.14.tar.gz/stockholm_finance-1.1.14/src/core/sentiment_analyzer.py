"""
Sentiment analysis module for Stockholm

Handles sentiment analysis for both market news and government policy news.
"""

import re
from functools import lru_cache

import numpy as np
from textblob import TextBlob

from ..config.config import ANALYSIS_CONFIG, MAJOR_TICKERS, SECTOR_MAPPING
from ..data.data_fetcher import get_ticker_company_name


@lru_cache(maxsize=128)
def get_ticker_sector(ticker):
    """Map tickers to their sectors/industries - cached for performance"""
    return SECTOR_MAPPING.get(ticker, "Other")


@lru_cache(maxsize=256)
def get_cached_company_name(ticker):
    """Get company name for ticker with caching for performance"""
    try:
        return get_ticker_company_name(ticker)
    except Exception:
        return ticker


def detect_ticker_mentions(text, min_confidence=0.5):
    """
    Advanced ticker detection using multiple sophisticated strategies
    Returns a list of tickers found in the text

    Args:
        text: The text to analyze
        min_confidence: Minimum confidence score (0.0-1.0) for ticker inclusion

    Detection strategies:
    1. Parentheses patterns: "Apple (AAPL)", "AAPL)", "(NASDAQ: AAPL)"
    2. Exchange prefixes: "NYSE: AAPL", "NASDAQ: TSLA"
    3. Stock suffixes: "AAPL stock", "TSLA shares"
    4. Company name mapping: "Apple" -> AAPL
    5. All-caps ticker detection with context validation
    6. Financial context requirements for ambiguous tickers
    """
    found_tickers = set()
    text_upper = text.upper()

    # Strategy 1: Parentheses patterns (highest confidence)
    found_tickers.update(_detect_parentheses_tickers(text, text_upper))

    # Strategy 2: Exchange prefixes (high confidence)
    found_tickers.update(_detect_exchange_prefixed_tickers(text, text_upper))

    # Strategy 3: Stock/shares suffixes (high confidence)
    found_tickers.update(_detect_stock_suffix_tickers(text, text_upper))

    # Strategy 4: Company name mapping (medium confidence)
    found_tickers.update(_detect_company_name_tickers(text, text_upper))

    # Strategy 5: All-caps ticker detection with validation (variable confidence)
    found_tickers.update(
        _detect_validated_ticker_symbols(text, text_upper, min_confidence)
    )

    return list(found_tickers)


def _detect_parentheses_tickers(text, text_upper):
    """Detect tickers in parentheses: 'Apple (AAPL)', '(NASDAQ: AAPL)', etc."""
    found_tickers = set()

    # Pattern 1: Company Name (TICKER)
    # Matches: "Apple (AAPL)", "Tesla Inc. (TSLA)", "Microsoft Corporation (MSFT)"
    pattern1 = r"\b[A-Za-z][A-Za-z\s&.,]+\s*\(\s*([A-Z]{1,5})\s*\)"
    matches1 = re.finditer(pattern1, text)
    for match in matches1:
        ticker = match.group(1)
        if _is_valid_ticker_format(ticker):
            found_tickers.add(ticker)

    # Pattern 2: (Exchange: TICKER)
    # Matches: "(NYSE: AAPL)", "(NASDAQ: TSLA)", "(AMEX: GLD)"
    pattern2 = r"\(\s*(?:NYSE|NASDAQ|AMEX|OTC):\s*([A-Z]{1,5})\s*\)"
    matches2 = re.finditer(pattern2, text_upper)
    for match in matches2:
        ticker = match.group(1)
        if _is_valid_ticker_format(ticker):
            found_tickers.add(ticker)

    # Pattern 3: (TICKER) at end of company mentions
    # Matches: "announced today (AAPL)", "reported earnings (TSLA)"
    pattern3 = r"\b(?:announced|reported|said|disclosed|revealed)\s+[^(]*\(\s*([A-Z]{1,5})\s*\)"
    matches3 = re.finditer(pattern3, text_upper)
    for match in matches3:
        ticker = match.group(1)
        if _is_valid_ticker_format(ticker):
            found_tickers.add(ticker)

    return found_tickers


def _detect_exchange_prefixed_tickers(text, text_upper):
    """Detect tickers with exchange prefixes: 'NYSE: AAPL', 'NASDAQ: TSLA'"""
    found_tickers = set()

    # Pattern: Exchange: TICKER (not in parentheses)
    pattern = r"\b(?:NYSE|NASDAQ|AMEX|OTC):\s*([A-Z]{1,5})\b"
    matches = re.finditer(pattern, text_upper)

    for match in matches:
        ticker = match.group(1)
        if _is_valid_ticker_format(ticker):
            found_tickers.add(ticker)

    return found_tickers


def _detect_stock_suffix_tickers(text, text_upper):
    """Detect tickers with stock/shares suffixes: 'AAPL stock', 'TSLA shares'"""
    found_tickers = set()

    # Pattern: TICKER followed by stock-related words
    stock_suffixes = r"\b(STOCK|SHARES|EQUITY|SECURITIES|COMMON)\b"
    pattern = r"\b([A-Z]{1,5})\s+" + stock_suffixes
    matches = re.finditer(pattern, text_upper)

    for match in matches:
        ticker = match.group(1)
        if _is_valid_ticker_format(ticker) and _has_financial_context(
            text_upper, match
        ):
            found_tickers.add(ticker)

    return found_tickers


def _detect_company_name_tickers(text, text_upper):
    """Detect tickers by mapping company names to ticker symbols"""
    found_tickers = set()

    # Enhanced company name patterns with more variations
    company_mappings = {
        "APPLE": "AAPL",
        "APPLE INC": "AAPL",
        "APPLE COMPUTER": "AAPL",
        "MICROSOFT": "MSFT",
        "MICROSOFT CORP": "MSFT",
        "MICROSOFT CORPORATION": "MSFT",
        "AMAZON": "AMZN",
        "AMAZON.COM": "AMZN",
        "AMAZON INC": "AMZN",
        "GOOGLE": "GOOGL",
        "ALPHABET": "GOOGL",
        "ALPHABET INC": "GOOGL",
        "TESLA": "TSLA",
        "TESLA INC": "TSLA",
        "TESLA MOTORS": "TSLA",
        "META": "META",
        "FACEBOOK": "META",
        "META PLATFORMS": "META",
        "NVIDIA": "NVDA",
        "NVIDIA CORP": "NVDA",
        "NVIDIA CORPORATION": "NVDA",
        "AT&T": "T",
        "ATT": "T",
        "AMERICAN TELEPHONE": "T",
        "GENERAL ELECTRIC": "GE",
        "GE": "GE",
        "VISA": "V",
        "VISA INC": "V",
        "CITIGROUP": "C",
        "CITI": "C",
        "CITICORP": "C",
        "DOMINION ENERGY": "D",
        "DOMINION": "D",
        "REALTY INCOME": "O",
        "REALTY INCOME CORP": "O",
        "SOUTHERN COMPANY": "SO",
        "SOUTHERN": "SO",
        "UNITED STATES STEEL": "X",
        "U.S. STEEL": "X",
        "US STEEL": "X",
        "ALCOA": "AA",
        "ALCOA CORP": "AA",
        "JPMORGAN": "JPM",
        "JP MORGAN": "JPM",
        "JPMORGAN CHASE": "JPM",
        "BANK OF AMERICA": "BAC",
        "BOFA": "BAC",
        "WELLS FARGO": "WFC",
        "WELLS FARGO & CO": "WFC",
        "GOLDMAN SACHS": "GS",
        "GOLDMAN": "GS",
        "MORGAN STANLEY": "MS",
        "BERKSHIRE HATHAWAY": "BRK-B",
        "BERKSHIRE": "BRK-B",
        "MASTERCARD": "MA",
        "MASTERCARD INC": "MA",
        "AMERICAN EXPRESS": "AXP",
        "AMEX": "AXP",
        "JOHNSON & JOHNSON": "JNJ",
        "J&J": "JNJ",
        "UNITEDHEALTH": "UNH",
        "UNITED HEALTH": "UNH",
        "PFIZER": "PFE",
        "PFIZER INC": "PFE",
        "ABBOTT": "ABT",
        "ABBOTT LABS": "ABT",
        "WALMART": "WMT",
        "WAL-MART": "WMT",
        "WALMART INC": "WMT",
        "HOME DEPOT": "HD",
        "THE HOME DEPOT": "HD",
        "PROCTER & GAMBLE": "PG",
        "P&G": "PG",
        "COCA-COLA": "KO",
        "COCA COLA": "KO",
        "COKE": "KO",
        "PEPSICO": "PEP",
        "PEPSI": "PEP",
        "MCDONALD'S": "MCD",
        "MCDONALDS": "MCD",
        "NIKE": "NKE",
        "NIKE INC": "NKE",
        "STARBUCKS": "SBUX",
        "STARBUCKS CORP": "SBUX",
        "TARGET": "TGT",
        "TARGET CORP": "TGT",
        "COSTCO": "COST",
        "COSTCO WHOLESALE": "COST",
        "LOWES": "LOW",
        "LOWE'S": "LOW",
        "DISNEY": "DIS",
        "WALT DISNEY": "DIS",
        "THE WALT DISNEY": "DIS",
        "BOEING": "BA",
        "BOEING CO": "BA",
        "CATERPILLAR": "CAT",
        "CATERPILLAR INC": "CAT",
        "EXXON": "XOM",
        "EXXON MOBIL": "XOM",
        "EXXONMOBIL": "XOM",
        "CHEVRON": "CVX",
        "CHEVRON CORP": "CVX",
        "NETFLIX": "NFLX",
        "NETFLIX INC": "NFLX",
        "ADOBE": "ADBE",
        "ADOBE INC": "ADBE",
        "SALESFORCE": "CRM",
        "SALESFORCE.COM": "CRM",
        "ORACLE": "ORCL",
        "ORACLE CORP": "ORCL",
        "INTEL": "INTC",
        "INTEL CORP": "INTC",
        "AMD": "AMD",
        "ADVANCED MICRO DEVICES": "AMD",
    }

    for company_name, ticker in company_mappings.items():
        # Look for company name mentions with word boundaries
        pattern = r"\b" + re.escape(company_name) + r"\b"
        if re.search(pattern, text_upper):
            # Verify it's in a financial context
            if _has_financial_context_for_company(text_upper, company_name):
                found_tickers.add(ticker)

    return found_tickers


def _detect_validated_ticker_symbols(text, text_upper, min_confidence):
    """Detect all-caps ticker symbols with confidence validation"""
    found_tickers = set()

    # Define problematic tickers that need extra validation
    problematic_tickers = {
        "T",
        "D",
        "O",
        "C",
        "V",
        "X",
        "A",
        "F",
        "M",
        "S",
        "R",
        "K",
        "L",
        "P",  # Single letters
        "SO",
        "GE",
        "AA",
        "IT",
        "ON",
        "OR",
        "AN",
        "AT",
        "TO",
        "GO",
        "UP",
        "ALL",  # Common words
    }

    # Financial context keywords
    financial_keywords = {
        "STOCK",
        "SHARES",
        "EARNINGS",
        "REVENUE",
        "PROFIT",
        "LOSS",
        "QUARTERLY",
        "ANNUAL",
        "REPORT",
        "TRADING",
        "PRICE",
        "MARKET",
        "DIVIDEND",
        "ANALYST",
        "UPGRADE",
        "DOWNGRADE",
        "TARGET",
        "NASDAQ",
        "NYSE",
        "S&P",
        "DOW",
        "EXCHANGE",
        "TICKER",
        "CORPORATION",
        "CORP",
        "INC",
        "LTD",
        "LLC",
        "COMPANY",
        "MERGER",
        "ACQUISITION",
        "IPO",
        "BUYBACK",
        "SPLIT",
        "BULL",
        "BEAR",
        "RALLY",
        "DECLINE",
        "SURGE",
        "PLUNGE",
        "ANNOUNCED",
        "REPORTED",
        "RELEASED",
        "DISCLOSED",
    }

    for ticker in MAJOR_TICKERS:
        # Look for ticker as whole word
        pattern = r"\b" + re.escape(ticker) + r"\b"
        matches = list(re.finditer(pattern, text_upper))

        if not matches:
            continue

        # Calculate confidence score
        max_confidence = 0.0
        for match in matches:
            confidence = _calculate_enhanced_ticker_confidence(
                text_upper, match, ticker, financial_keywords, problematic_tickers
            )
            max_confidence = max(max_confidence, confidence)

        # Include ticker if confidence meets threshold
        if max_confidence >= min_confidence:
            found_tickers.add(ticker)

    return found_tickers


def _is_valid_ticker_format(ticker):
    """Check if a string looks like a valid ticker symbol"""
    if not ticker or len(ticker) < 1 or len(ticker) > 5:
        return False

    # Must be all uppercase letters, possibly with hyphens
    if not re.match(r"^[A-Z]+(-[A-Z]+)?$", ticker):
        return False

    # Exclude obvious non-tickers
    excluded = {
        "THE",
        "AND",
        "FOR",
        "ARE",
        "BUT",
        "NOT",
        "YOU",
        "ALL",
        "CAN",
        "HER",
        "WAS",
        "ONE",
        "OUR",
        "HAD",
        "BY",
    }
    if ticker in excluded:
        return False

    return True


def _has_financial_context(text_upper, match, window=100):
    """Check if a ticker mention has financial context nearby"""
    start_pos = match.start()
    end_pos = match.end()

    context_start = max(0, start_pos - window)
    context_end = min(len(text_upper), end_pos + window)
    context = text_upper[context_start:context_end]

    financial_indicators = {
        "STOCK",
        "SHARES",
        "PRICE",
        "TRADING",
        "MARKET",
        "EARNINGS",
        "REVENUE",
        "PROFIT",
        "LOSS",
        "DIVIDEND",
        "ANALYST",
        "UPGRADE",
        "DOWNGRADE",
        "TARGET",
        "NASDAQ",
        "NYSE",
        "EXCHANGE",
        "BULL",
        "BEAR",
        "RALLY",
        "DECLINE",
        "SURGE",
        "PLUNGE",
        "$",
        "%",
        "PERCENT",
        "POINTS",
        "CENTS",
        "DOLLARS",
    }

    return any(indicator in context for indicator in financial_indicators)


def _has_financial_context_for_company(text_upper, company_name, window=150):
    """Check if a company name mention has financial context"""
    # Find company name position
    pattern = r"\b" + re.escape(company_name) + r"\b"
    match = re.search(pattern, text_upper)

    if not match:
        return False

    start_pos = match.start()
    end_pos = match.end()

    context_start = max(0, start_pos - window)
    context_end = min(len(text_upper), end_pos + window)
    context = text_upper[context_start:context_end]

    # Strong financial indicators that clearly indicate stock/financial context
    strong_financial_indicators = {
        "STOCK",
        "SHARES",
        "PRICE",
        "TRADING",
        "MARKET",
        "EARNINGS",
        "REVENUE",
        "PROFIT",
        "LOSS",
        "DIVIDEND",
        "ANALYST",
        "UPGRADE",
        "DOWNGRADE",
        "TARGET",
        "NASDAQ",
        "NYSE",
        "EXCHANGE",
        "QUARTERLY",
        "ANNUAL",
        "MERGER",
        "ACQUISITION",
        "$",
        "%",
        "PERCENT",
        "POINTS",
        "CENTS",
        "DOLLARS",
        "BULL",
        "BEAR",
        "RALLY",
        "DECLINE",
        "SURGE",
        "PLUNGE",
    }

    # Check for strong financial indicators first
    if any(indicator in context for indicator in strong_financial_indicators):
        return True

    # For weaker indicators like "ANNOUNCED", "REPORTED", etc., require additional financial context
    weak_financial_indicators = {
        "ANNOUNCED",
        "REPORTED",
        "RELEASED",
        "DISCLOSED",
        "REPORT",
    }

    # If we find weak indicators, check if they're combined with financial terms
    for weak_indicator in weak_financial_indicators:
        if weak_indicator in context:
            # Look for financial terms near the weak indicator
            weak_indicator_pos = context.find(weak_indicator)
            weak_context_start = max(0, weak_indicator_pos - 50)
            weak_context_end = min(
                len(context), weak_indicator_pos + len(weak_indicator) + 50
            )
            weak_context = context[weak_context_start:weak_context_end]

            # Check if the announcement/report is about financial matters
            financial_terms = {
                "EARNINGS",
                "REVENUE",
                "PROFIT",
                "LOSS",
                "SALES",
                "INCOME",
                "QUARTERLY",
                "ANNUAL",
                "RESULTS",
                "FINANCIAL",
                "FISCAL",
                "DIVIDEND",
                "BUYBACK",
                "GUIDANCE",
                "OUTLOOK",
                "FORECAST",
            }

            if any(term in weak_context for term in financial_terms):
                return True

    return False


def _calculate_enhanced_ticker_confidence(
    text_upper, match, ticker, financial_keywords, problematic_tickers
):
    """Enhanced confidence calculation for ticker mentions"""
    confidence = 0.0

    # Base confidence depends on ticker type
    if ticker not in problematic_tickers:
        confidence = 0.8  # High base confidence for clear tickers
    else:
        confidence = 0.2  # Low base confidence for problematic tickers

    start_pos = match.start()
    end_pos = match.end()

    # Check immediate context for common English usage
    immediate_before = text_upper[max(0, start_pos - 10) : start_pos]
    immediate_after = text_upper[end_pos : min(len(text_upper), end_pos + 10)]

    # Penalize obvious English usage
    if ticker in {"SO", "TO", "OR", "AT", "ON", "AN", "IT", "UP", "GO", "ALL"}:
        if immediate_before.endswith((" ", ",", ".")) and immediate_after.startswith(
            (" ", ",", ".")
        ):
            confidence *= 0.1  # Very low confidence for common words

    # Context window analysis
    context_window = 100
    context_start = max(0, start_pos - context_window)
    context_end = min(len(text_upper), end_pos + context_window)
    context = text_upper[context_start:context_end]

    # Boost for financial keywords
    financial_keyword_count = sum(
        1 for keyword in financial_keywords if keyword in context
    )
    confidence += financial_keyword_count * 0.1

    # Boost for stock-related patterns
    if re.search(r"\$\d+\.?\d*", context):  # Dollar amounts
        confidence += 0.2
    if re.search(r"\d+\.?\d*%", context):  # Percentages
        confidence += 0.2
    if re.search(r"\b(ROSE|FELL|GAINED|LOST|UP|DOWN|HIGHER|LOWER)\b", context):
        confidence += 0.15

    # Boost for exchange mentions
    if re.search(r"\b(NYSE|NASDAQ|AMEX|OTC)\b", context):
        confidence += 0.25

    # Boost for parentheses (already detected separately, but adds confidence)
    if re.search(r"\([^)]*" + re.escape(ticker) + r"[^)]*\)", context):
        confidence += 0.3

    return min(confidence, 1.0)


def _validate_ticker_context(
    text_upper, match, ticker, financial_keywords, company_name_patterns
):
    """
    Validate that a ticker mention appears in a financial context

    Args:
        text_upper: The uppercase text
        match: The regex match object for the ticker
        ticker: The ticker symbol
        financial_keywords: Set of financial context keywords
        company_name_patterns: Dict mapping tickers to common company name variations

    Returns:
        bool: True if the ticker mention appears to be valid
    """
    start_pos = match.start()
    end_pos = match.end()

    # Check for common English usage patterns that should be excluded
    # Look at the immediate context around the ticker
    immediate_before = text_upper[max(0, start_pos - 10) : start_pos]
    immediate_after = text_upper[end_pos : min(len(text_upper), end_pos + 10)]

    # Exclude common English patterns
    if ticker == "SO":
        # "so" as conjunction: "was volatile, so investors"
        if immediate_before.endswith(", ") or immediate_before.endswith(" "):
            if immediate_after.startswith(" ") and not any(
                word in immediate_after.upper() for word in ["STOCK", "SHARES", "CORP"]
            ):
                return False

    # Define context window (characters before and after the ticker)
    context_window = 100
    context_start = max(0, start_pos - context_window)
    context_end = min(len(text_upper), end_pos + context_window)
    context = text_upper[context_start:context_end]

    # Check for financial keywords in the context
    for keyword in financial_keywords:
        if keyword in context:
            return True

    # Check for known company name patterns first (faster than API call)
    if ticker in company_name_patterns:
        for company_name in company_name_patterns[ticker]:
            if company_name in context:
                return True

    # Check for company name mentions (cached for performance)
    company_name = get_cached_company_name(ticker).upper()
    if company_name and company_name != ticker:
        # Look for parts of the company name in the context
        company_words = company_name.split()
        for word in company_words:
            if len(word) > 3 and word in context:  # Skip short words like "INC"
                return True

    # Check for ticker in parentheses pattern: "Company Name (TICKER)"
    parentheses_pattern = r"\([^)]*" + re.escape(ticker) + r"[^)]*\)"
    if re.search(parentheses_pattern, context):
        return True

    # Check for stock price patterns: "$XX.XX", "XX%", "rose", "fell", etc.
    price_patterns = [
        r"\$\d+\.?\d*",  # Dollar amounts
        r"\d+\.?\d*%",  # Percentages
        r"\b(ROSE|FELL|GAINED|LOST|UP|DOWN|HIGHER|LOWER)\b",
        r"\b(POINTS?|PERCENT|CENTS?)\b",
    ]

    for pattern in price_patterns:
        if re.search(pattern, context):
            return True

    return False


def _calculate_ticker_confidence(
    text_upper,
    match,
    ticker,
    financial_keywords,
    company_name_patterns,
    problematic_tickers,
):
    """
    Calculate confidence score for a ticker mention (0.0 to 1.0)

    Args:
        text_upper: The uppercase text
        match: The regex match object for the ticker
        ticker: The ticker symbol
        financial_keywords: Set of financial context keywords
        company_name_patterns: Dict mapping tickers to company name variations
        problematic_tickers: Set of tickers that need extra validation

    Returns:
        float: Confidence score between 0.0 and 1.0
    """
    confidence = 0.0

    # Base confidence depends on ticker type
    if ticker not in problematic_tickers:
        confidence = 0.8  # High base confidence for non-problematic tickers
    else:
        confidence = 0.2  # Low base confidence for problematic tickers

    start_pos = match.start()
    end_pos = match.end()

    # Check for common English usage patterns that reduce confidence
    immediate_before = text_upper[max(0, start_pos - 10) : start_pos]
    immediate_after = text_upper[end_pos : min(len(text_upper), end_pos + 10)]

    # Penalize common English patterns
    if ticker == "SO":
        if immediate_before.endswith(", ") or immediate_before.endswith(" "):
            if immediate_after.startswith(" ") and not any(
                word in immediate_after.upper() for word in ["STOCK", "SHARES", "CORP"]
            ):
                confidence *= 0.1  # Very low confidence for "so" as conjunction

    # Define context window
    context_window = 100
    context_start = max(0, start_pos - context_window)
    context_end = min(len(text_upper), end_pos + context_window)
    context = text_upper[context_start:context_end]

    # Boost confidence for financial keywords
    financial_keyword_count = sum(
        1 for keyword in financial_keywords if keyword in context
    )
    confidence += financial_keyword_count * 0.1  # +0.1 per financial keyword

    # Boost confidence for company name mentions
    if ticker in company_name_patterns:
        for company_name in company_name_patterns[ticker]:
            if company_name in context:
                confidence += 0.3  # Strong boost for company name
                break

    # Also check dynamic company name from yfinance
    try:
        dynamic_company_name = get_cached_company_name(ticker).upper()
        if dynamic_company_name and dynamic_company_name != ticker:
            company_words = dynamic_company_name.split()
            for word in company_words:
                if len(word) > 3 and word in context:
                    confidence += 0.25  # Boost for dynamic company name
                    break
    except Exception:
        pass

    # Boost confidence for parentheses pattern: "Company Name (TICKER)"
    parentheses_pattern = r"\([^)]*" + re.escape(ticker) + r"[^)]*\)"
    if re.search(parentheses_pattern, context):
        confidence += 0.4  # Very strong boost for parentheses pattern

    # Boost confidence for stock price patterns
    price_patterns = [
        r"\$\d+\.?\d*",  # Dollar amounts
        r"\d+\.?\d*%",  # Percentages
        r"\b(ROSE|FELL|GAINED|LOST|UP|DOWN|HIGHER|LOWER)\b",
        r"\b(POINTS?|PERCENT|CENTS?)\b",
    ]

    price_pattern_count = sum(
        1 for pattern in price_patterns if re.search(pattern, context)
    )
    confidence += price_pattern_count * 0.15  # +0.15 per price pattern

    # Cap confidence at 1.0
    return min(confidence, 1.0)


def detect_ticker_mentions_with_confidence(text, min_confidence=0.5):
    """
    Enhanced ticker detection with confidence scores using multiple strategies

    Args:
        text: The text to analyze
        min_confidence: Minimum confidence score for inclusion

    Returns:
        list: List of dicts with 'ticker' and 'confidence' keys
    """
    ticker_confidence_map = {}
    text_upper = text.upper()

    # Strategy 1: Parentheses patterns (highest confidence)
    parentheses_tickers = _detect_parentheses_tickers(text, text_upper)
    for ticker in parentheses_tickers:
        ticker_confidence_map[ticker] = max(ticker_confidence_map.get(ticker, 0), 0.95)

    # Strategy 2: Exchange prefixes (high confidence)
    exchange_tickers = _detect_exchange_prefixed_tickers(text, text_upper)
    for ticker in exchange_tickers:
        ticker_confidence_map[ticker] = max(ticker_confidence_map.get(ticker, 0), 0.90)

    # Strategy 3: Stock/shares suffixes (high confidence)
    suffix_tickers = _detect_stock_suffix_tickers(text, text_upper)
    for ticker in suffix_tickers:
        ticker_confidence_map[ticker] = max(ticker_confidence_map.get(ticker, 0), 0.85)

    # Strategy 4: Company name mapping (medium confidence)
    company_tickers = _detect_company_name_tickers(text, text_upper)
    for ticker in company_tickers:
        ticker_confidence_map[ticker] = max(ticker_confidence_map.get(ticker, 0), 0.75)

    # Strategy 5: Validated ticker symbols (variable confidence)
    validated_tickers = _detect_validated_ticker_symbols(
        text, text_upper, min_confidence
    )
    for ticker in validated_tickers:
        # Calculate detailed confidence for these tickers
        pattern = r"\b" + re.escape(ticker) + r"\b"
        matches = list(re.finditer(pattern, text_upper))

        if matches:
            problematic_tickers = {
                "T",
                "D",
                "O",
                "C",
                "V",
                "X",
                "A",
                "F",
                "M",
                "S",
                "R",
                "K",
                "L",
                "P",
                "SO",
                "GE",
                "AA",
                "IT",
                "ON",
                "OR",
                "AN",
                "AT",
                "TO",
                "GO",
                "UP",
                "ALL",
            }
            financial_keywords = {
                "STOCK",
                "SHARES",
                "EARNINGS",
                "REVENUE",
                "PROFIT",
                "LOSS",
                "QUARTERLY",
                "ANNUAL",
                "REPORT",
                "TRADING",
                "PRICE",
                "MARKET",
                "DIVIDEND",
                "ANALYST",
                "UPGRADE",
                "DOWNGRADE",
                "TARGET",
                "NASDAQ",
                "NYSE",
                "S&P",
                "DOW",
                "EXCHANGE",
                "TICKER",
                "CORPORATION",
                "CORP",
                "INC",
                "LTD",
                "LLC",
                "COMPANY",
                "MERGER",
                "ACQUISITION",
                "IPO",
                "BUYBACK",
                "SPLIT",
                "BULL",
                "BEAR",
                "RALLY",
                "DECLINE",
                "SURGE",
                "PLUNGE",
                "ANNOUNCED",
                "REPORTED",
                "RELEASED",
                "DISCLOSED",
            }

            max_confidence = 0.0
            for match in matches:
                confidence = _calculate_enhanced_ticker_confidence(
                    text_upper, match, ticker, financial_keywords, problematic_tickers
                )
                max_confidence = max(max_confidence, confidence)

            # Only update if this gives higher confidence than other strategies
            if max_confidence >= min_confidence:
                ticker_confidence_map[ticker] = max(
                    ticker_confidence_map.get(ticker, 0), max_confidence
                )

    # Convert to list format and filter by minimum confidence
    ticker_results = []
    for ticker, confidence in ticker_confidence_map.items():
        if confidence >= min_confidence:
            ticker_results.append(
                {"ticker": ticker, "confidence": round(confidence, 3)}
            )

    # Sort by confidence (highest first)
    ticker_results.sort(key=lambda x: x["confidence"], reverse=True)
    return ticker_results


def analyze_sentiment_around_ticker(text, ticker, context_window=50):
    """
    Analyze sentiment in the context around a specific ticker mention

    Args:
        text: The full article text
        ticker: The ticker to analyze sentiment for
        context_window: Number of characters before/after ticker to analyze

    Returns:
        dict with sentiment analysis for this ticker
    """
    text_upper = text.upper()
    ticker_upper = ticker.upper()

    # Find all positions where the ticker is mentioned
    pattern = r"\b" + re.escape(ticker_upper) + r"\b"
    matches = list(re.finditer(pattern, text_upper))

    if not matches:
        return {
            "ticker": ticker,
            "mentioned": False,
            "sentiment_score": 0,
            "sentiment_category": "Neutral",
            "context_snippets": [],
        }

    # Extract context around each mention and analyze sentiment
    context_snippets = []
    sentiment_scores = []

    for match in matches:
        start_pos = max(0, match.start() - context_window)
        end_pos = min(len(text), match.end() + context_window)

        # Get context from original text (preserving case)
        context = text[start_pos:end_pos].strip()
        context_snippets.append(context)

        # Analyze sentiment of this context
        try:
            blob = TextBlob(context)
            sentiment_scores.append(blob.sentiment.polarity)
        except Exception:
            sentiment_scores.append(0)

    # Calculate average sentiment across all mentions
    avg_sentiment = np.mean(sentiment_scores) if sentiment_scores else 0

    # Determine sentiment category
    if avg_sentiment > 0.1:
        category = "Positive"
    elif avg_sentiment < -0.1:
        category = "Negative"
    else:
        category = "Neutral"

    return {
        "ticker": ticker,
        "mentioned": True,
        "sentiment_score": avg_sentiment,
        "sentiment_category": category,
        "context_snippets": context_snippets,
        "mention_count": len(matches),
    }


def analyze_sentiment_batch(news_data):
    """
    Optimized sentiment analysis using TextBlob for batch processing.

    Sentiment Thresholds (standardized across Stockholm):
    - Positive: polarity > 0.1 (clearly positive language)
    - Negative: polarity < -0.1 (clearly negative language)
    - Neutral: -0.1 <= polarity <= 0.1 (balanced or unclear sentiment)

    These thresholds filter out weak sentiment signals and focus on
    articles with clear positive/negative sentiment that could impact markets.

    Args:
        news_data: List of article dictionaries with 'headline' and 'text' fields

    Returns:
        tuple: (sentiment_scores, sentiment_details) for further analysis
    """
    sentiment_scores = []
    sentiment_details = []

    # Sentiment thresholds - these values are used consistently across Stockholm
    POSITIVE_THRESHOLD = 0.1  # Articles clearly positive about markets/companies
    NEGATIVE_THRESHOLD = -0.1  # Articles clearly negative about markets/companies

    for article in news_data:
        try:
            # Combine headline and text for more comprehensive sentiment analysis
            # Headlines often contain the key sentiment, text provides context
            text = f"{article['headline']} {article.get('text', '')}"
            blob = TextBlob(text)
            polarity = (
                blob.sentiment.polarity
            )  # Range: -1.0 (very negative) to +1.0 (very positive)

            sentiment_scores.append(polarity)
            sentiment_details.append(
                {
                    "headline": article["headline"],
                    "polarity": polarity,
                    "category": (
                        "Positive"
                        if polarity > POSITIVE_THRESHOLD
                        else "Negative" if polarity < NEGATIVE_THRESHOLD else "Neutral"
                    ),
                }
            )
        except Exception:
            # Robust error handling: if sentiment analysis fails, default to neutral
            # This prevents crashes from malformed articles or TextBlob issues
            sentiment_scores.append(0)
            sentiment_details.append(
                {
                    "headline": article.get("headline", ""),
                    "polarity": 0,
                    "category": "Neutral",
                }
            )

    return sentiment_scores, sentiment_details


def analyze_multi_ticker_sentiment(news_data):
    """
    Enhanced sentiment analysis that detects multiple ticker mentions
    and analyzes sentiment for each ticker mentioned in each article

    Returns:
        tuple: (sentiment_scores, sentiment_details, multi_ticker_articles)
    """
    sentiment_scores = []
    sentiment_details = []
    multi_ticker_articles = []

    for i, article in enumerate(news_data):
        try:
            text = f"{article['headline']} {article.get('text', '')}"

            # Get overall sentiment (for backward compatibility)
            blob = TextBlob(text)
            overall_polarity = blob.sentiment.polarity

            # Detect all ticker mentions in the article
            mentioned_tickers = detect_ticker_mentions(text)

            # Analyze sentiment for each mentioned ticker
            ticker_sentiments = {}
            for ticker in mentioned_tickers:
                ticker_sentiment = analyze_sentiment_around_ticker(text, ticker)
                ticker_sentiments[ticker] = ticker_sentiment

            # Store overall sentiment (for backward compatibility)
            sentiment_scores.append(overall_polarity)
            sentiment_details.append(
                {
                    "headline": article["headline"],
                    "polarity": overall_polarity,
                    "category": (
                        "Positive"
                        if overall_polarity > 0.1
                        else "Negative" if overall_polarity < -0.1 else "Neutral"
                    ),
                    "mentioned_tickers": mentioned_tickers,
                    "ticker_sentiments": ticker_sentiments,
                }
            )

            # If multiple tickers mentioned, add to multi-ticker articles
            if len(mentioned_tickers) > 1:
                multi_ticker_articles.append(
                    {
                        "article_index": i,
                        "article": article,
                        "mentioned_tickers": mentioned_tickers,
                        "ticker_sentiments": ticker_sentiments,
                        "overall_sentiment": overall_polarity,
                    }
                )

        except Exception:
            sentiment_scores.append(0)
            sentiment_details.append(
                {
                    "headline": article.get("headline", ""),
                    "polarity": 0,
                    "category": "Neutral",
                    "mentioned_tickers": [],
                    "ticker_sentiments": {},
                }
            )

    return sentiment_scores, sentiment_details, multi_ticker_articles


def analyze_cross_ticker_sentiment(multi_ticker_articles):
    """
    Analyze sentiment patterns across tickers in multi-ticker articles

    Returns:
        dict: Analysis of cross-ticker sentiment patterns
    """
    if not multi_ticker_articles:
        return {
            "total_multi_ticker_articles": 0,
            "sentiment_conflicts": [],
            "ticker_pairs": {},
            "summary": "No multi-ticker articles found",
        }

    sentiment_conflicts = []
    ticker_pairs = {}

    for article_data in multi_ticker_articles:
        tickers = article_data["mentioned_tickers"]
        ticker_sentiments = article_data["ticker_sentiments"]
        article = article_data["article"]

        # Check for sentiment conflicts (one ticker positive, another negative)
        positive_tickers = []
        negative_tickers = []
        neutral_tickers = []

        for ticker in tickers:
            if ticker in ticker_sentiments:
                sentiment = ticker_sentiments[ticker]
                if sentiment["sentiment_category"] == "Positive":
                    positive_tickers.append(ticker)
                elif sentiment["sentiment_category"] == "Negative":
                    negative_tickers.append(ticker)
                else:
                    neutral_tickers.append(ticker)

        # Detect conflicts (positive and negative in same article)
        if positive_tickers and negative_tickers:
            sentiment_conflicts.append(
                {
                    "headline": article["headline"],
                    "url": article.get("url", ""),
                    "time_ago": article.get("time_ago", "Unknown"),
                    "positive_tickers": positive_tickers,
                    "negative_tickers": negative_tickers,
                    "neutral_tickers": neutral_tickers,
                    "ticker_sentiments": ticker_sentiments,
                }
            )

        # Track ticker pair co-occurrences
        for i, ticker1 in enumerate(tickers):
            for ticker2 in tickers[i + 1 :]:
                pair_key = (
                    f"{ticker1}-{ticker2}"
                    if ticker1 < ticker2
                    else f"{ticker2}-{ticker1}"
                )

                if pair_key not in ticker_pairs:
                    ticker_pairs[pair_key] = {
                        "count": 0,
                        "articles": [],
                        "sentiment_patterns": [],
                    }

                ticker_pairs[pair_key]["count"] += 1
                ticker_pairs[pair_key]["articles"].append(
                    article["headline"][:60] + "..."
                )

                # Record sentiment pattern for this pair
                sentiment1 = ticker_sentiments.get(ticker1, {}).get(
                    "sentiment_category", "Unknown"
                )
                sentiment2 = ticker_sentiments.get(ticker2, {}).get(
                    "sentiment_category", "Unknown"
                )
                ticker_pairs[pair_key]["sentiment_patterns"].append(
                    f"{ticker1}:{sentiment1}, {ticker2}:{sentiment2}"
                )

    # Sort ticker pairs by frequency
    sorted_pairs = sorted(
        ticker_pairs.items(), key=lambda x: x[1]["count"], reverse=True
    )

    return {
        "total_multi_ticker_articles": len(multi_ticker_articles),
        "sentiment_conflicts": sentiment_conflicts,
        "ticker_pairs": dict(sorted_pairs[:10]),  # Top 10 most common pairs
        "summary": f"Found {len(multi_ticker_articles)} multi-ticker articles with {len(sentiment_conflicts)} sentiment conflicts",
    }


def calculate_market_metrics(sentiment_scores, sentiment_details):
    """Calculate market sentiment metrics efficiently"""
    if not sentiment_scores:
        return {
            "market_mood": "No Data",
            "average_sentiment": 0,
            "positive_percentage": 0,
            "negative_percentage": 0,
            "neutral_percentage": 0,
            "total_articles": 0,
        }

    avg_sentiment = np.mean(sentiment_scores)
    categories = [detail["category"] for detail in sentiment_details]
    total = len(categories)

    positive_pct = (categories.count("Positive") / total) * 100
    negative_pct = (categories.count("Negative") / total) * 100
    neutral_pct = (categories.count("Neutral") / total) * 100

    # Determine market mood
    thresholds = ANALYSIS_CONFIG["sentiment_thresholds"]
    if avg_sentiment > thresholds["very_positive"]:
        market_mood = "Very Positive"
    elif avg_sentiment > thresholds["positive"]:
        market_mood = "Positive"
    elif avg_sentiment > thresholds["negative"]:
        market_mood = "Neutral"
    elif avg_sentiment > thresholds["very_negative"]:
        market_mood = "Negative"
    else:
        market_mood = "Very Negative"

    return {
        "market_mood": market_mood,
        "average_sentiment": avg_sentiment,
        "positive_percentage": positive_pct,
        "negative_percentage": negative_pct,
        "neutral_percentage": neutral_pct,
        "total_articles": total,
    }


def analyze_ticker_sentiment_optimized(news_data, sentiment_details):
    """Optimized ticker sentiment analysis"""
    ticker_sentiment = {}

    # Group articles by ticker
    ticker_articles = {}
    for i, article in enumerate(news_data):
        ticker = article.get("ticker")
        if ticker:
            if ticker not in ticker_articles:
                ticker_articles[ticker] = []
            ticker_articles[ticker].append((article, sentiment_details[i]))

    # Calculate metrics for each ticker
    for ticker, articles_with_sentiment in ticker_articles.items():
        scores = [sentiment["polarity"] for _, sentiment in articles_with_sentiment]
        categories = [sentiment["category"] for _, sentiment in articles_with_sentiment]

        total_articles = len(scores)
        positive_count = categories.count("Positive")
        negative_count = categories.count("Negative")
        neutral_count = categories.count("Neutral")

        avg_sentiment = np.mean(scores)
        sentiment_volatility = np.std(scores) if len(scores) > 1 else 0
        sentiment_consistency = 1 / (1 + sentiment_volatility)
        overall_score = avg_sentiment * sentiment_consistency

        # Find best and worst headlines with timestamps
        best_article = max(articles_with_sentiment, key=lambda x: x[1]["polarity"])[0]
        worst_article = min(articles_with_sentiment, key=lambda x: x[1]["polarity"])[0]

        ticker_sentiment[ticker] = {
            "average_sentiment": avg_sentiment,
            "sentiment_volatility": sentiment_volatility,
            "sentiment_consistency": sentiment_consistency,
            "overall_score": overall_score,
            "total_articles": total_articles,
            "positive_count": positive_count,
            "negative_count": negative_count,
            "neutral_count": neutral_count,
            "positive_percentage": (positive_count / total_articles) * 100,
            "negative_percentage": (negative_count / total_articles) * 100,
            "best_headline": best_article["headline"],
            "best_headline_time": best_article.get("time_ago", "Unknown time"),
            "best_headline_datetime": best_article.get("datetime", "Unknown"),
            "best_headline_url": best_article.get("url", ""),
            "worst_headline": worst_article["headline"],
            "worst_headline_time": worst_article.get("time_ago", "Unknown time"),
            "worst_headline_datetime": worst_article.get("datetime", "Unknown"),
            "worst_headline_url": worst_article.get("url", ""),
        }

    return ticker_sentiment


def analyze_sector_sentiment_optimized(ticker_sentiment):
    """Optimized sector sentiment analysis"""
    sector_sentiment = {}

    # Group tickers by sector
    for ticker, data in ticker_sentiment.items():
        sector = get_ticker_sector(ticker)

        if sector not in sector_sentiment:
            sector_sentiment[sector] = {
                "tickers": [],
                "sentiment_scores": [],
                "total_articles": 0,
                "positive_count": 0,
                "negative_count": 0,
                "neutral_count": 0,
            }

        sector_data = sector_sentiment[sector]
        sector_data["tickers"].append(
            {
                "ticker": ticker,
                "overall_score": data["overall_score"],
                "average_sentiment": data["average_sentiment"],
            }
        )

        # Aggregate counts
        sector_data["total_articles"] += data["total_articles"]
        sector_data["positive_count"] += data["positive_count"]
        sector_data["negative_count"] += data["negative_count"]
        sector_data["neutral_count"] += data["neutral_count"]
        sector_data["sentiment_scores"].append(data["average_sentiment"])

    # Calculate sector metrics
    sector_rankings = []
    for sector, data in sector_sentiment.items():
        if data["sentiment_scores"]:
            avg_sentiment = np.mean(data["sentiment_scores"])
            data["tickers"].sort(key=lambda x: x["overall_score"], reverse=True)

            # Sector strength = average of top 3 performers
            top_performers = data["tickers"][:3]
            sector_strength = np.mean([t["overall_score"] for t in top_performers])

            total_articles = data["total_articles"]
            positive_pct = (
                (data["positive_count"] / total_articles) * 100
                if total_articles > 0
                else 0
            )

            sector_rankings.append(
                {
                    "sector": sector,
                    "average_sentiment": avg_sentiment,
                    "sector_strength": sector_strength,
                    "ticker_count": len(data["tickers"]),
                    "total_articles": total_articles,
                    "positive_percentage": positive_pct,
                    "top_ticker": (
                        data["tickers"][0]["ticker"] if data["tickers"] else "N/A"
                    ),
                    "top_ticker_score": (
                        data["tickers"][0]["overall_score"] if data["tickers"] else 0
                    ),
                }
            )

    return sorted(sector_rankings, key=lambda x: x["sector_strength"], reverse=True)


def rank_tickers_optimized(ticker_sentiment):
    """Optimized ticker ranking - single sort operation"""
    ticker_infos = []

    for ticker, data in ticker_sentiment.items():
        ticker_infos.append(
            {
                "ticker": ticker,
                "average_sentiment": data["average_sentiment"],
                "overall_score": data["overall_score"],
                "total_articles": data["total_articles"],
                "positive_percentage": data["positive_percentage"],
                "negative_percentage": data["negative_percentage"],
                "best_headline": data["best_headline"],
                "best_headline_time": data["best_headline_time"],
                "best_headline_datetime": data["best_headline_datetime"],
                "best_headline_url": data["best_headline_url"],
                "worst_headline": data["worst_headline"],
                "worst_headline_time": data["worst_headline_time"],
                "worst_headline_datetime": data["worst_headline_datetime"],
                "worst_headline_url": data["worst_headline_url"],
            }
        )

    # Return only the best overall ranking (most important)
    return sorted(ticker_infos, key=lambda x: x["overall_score"], reverse=True)


def analyze_market_health_optimized(
    market_data, sentiment_analysis, policy_analysis=None
):
    """
    Optimized market health analysis with policy integration.

    This function combines multiple data sources to generate trading recommendations:
    1. Market Data: Price changes from major indices (SPY, QQQ, DIA, etc.)
    2. Sentiment Analysis: News sentiment from financial articles
    3. Policy Analysis: Government policy sentiment from Fed/regulatory news

    Algorithm:
    - Calculate average market performance from indices
    - Combine market sentiment (70%) with policy sentiment (30%)
    - Generate recommendations based on combined signals

    Market Trend Thresholds:
    - Strong Bullish: >2% average market gain
    - Bullish: 0.5% to 2% average gain
    - Sideways: -0.5% to 0.5% (neutral market)
    - Bearish: -2% to -0.5% average loss
    - Strong Bearish: <-2% average loss

    Recommendation Logic:
    - STRONG BUY: Positive sentiment + strong market gains
    - BUY: Positive sentiment + market gains
    - HOLD: Neutral sentiment + stable market
    - CAUTION: Negative sentiment + market decline
    - SELL: Strong negative sentiment + significant market decline

    Args:
        market_data: Dict of market indices with price changes
        sentiment_analysis: Dict with average sentiment from news
        policy_analysis: Optional dict with policy sentiment

    Returns:
        Dict with recommendation, trend, and supporting metrics
    """
    if not market_data:
        return {"recommendation": "INSUFFICIENT DATA", "market_trend": "Unknown"}

    # Calculate average market performance from all indices
    price_changes = [data["price_change"] for data in market_data.values()]
    avg_market_change = np.mean(price_changes)

    # Market trend classification based on average index performance
    # These thresholds reflect significant market movements that impact trading decisions
    if avg_market_change > 2:
        market_trend = "Strong Bullish"  # Major market rally
    elif avg_market_change > 0.5:
        market_trend = "Bullish"  # Moderate market gains
    elif avg_market_change > -0.5:
        market_trend = "Sideways"  # Neutral/consolidating market
    elif avg_market_change > -2:
        market_trend = "Bearish"  # Moderate market decline
    else:
        market_trend = "Strong Bearish"  # Major market selloff

    # Extract sentiment scores for recommendation algorithm
    sentiment_score = sentiment_analysis.get("average_sentiment", 0)
    policy_score = policy_analysis.get("policy_sentiment", 0) if policy_analysis else 0

    # Combine sentiment and policy with weighted average
    # Market sentiment (70%) + Policy sentiment (30%) = balanced approach
    market_weight = ANALYSIS_CONFIG["market_weight"]  # 0.7
    policy_weight = ANALYSIS_CONFIG["policy_weight"]  # 0.3
    combined_sentiment = sentiment_score * market_weight + policy_score * policy_weight

    # Generate trading recommendations based on combined signals
    # Both sentiment and market performance must align for strong recommendations
    if combined_sentiment > 0.1 and avg_market_change > 1:
        recommendation = "STRONG BUY"  # Strong positive sentiment + strong market
    elif combined_sentiment > 0.05 and avg_market_change > 0:
        recommendation = "BUY"  # Positive sentiment + positive market
    elif combined_sentiment > -0.05 and avg_market_change > -1:
        recommendation = "HOLD"  # Neutral sentiment + stable market
    elif combined_sentiment > -0.1 and avg_market_change > -2:
        recommendation = "CAUTION"  # Negative sentiment + declining market
    else:
        recommendation = "SELL"  # Strong negative sentiment + weak market

    # Add policy influence annotation for context
    policy_influence = ""
    if policy_analysis and abs(policy_score) > 0.05:
        if policy_score > 0.1:
            policy_influence = " (Policy Supportive)"  # Fed/gov policies favor markets
        elif policy_score < -0.1:
            policy_influence = " (Policy Headwinds)"  # Fed/gov policies concern markets
        else:
            policy_influence = " (Policy Neutral)"  # Mixed policy signals

    return {
        "recommendation": recommendation + policy_influence,
        "market_trend": market_trend,
        "average_market_change": avg_market_change,
        "combined_sentiment": combined_sentiment,
        "policy_influence": policy_score,
    }
