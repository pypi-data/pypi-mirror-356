#!/usr/bin/env python3
"""
Intelligent caching system for Stockholm
Reduces API calls by implementing smart caching strategies
"""

import hashlib
import json
import pickle
import threading
import time
from collections import defaultdict, deque
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple


class CacheManager:
    """Intelligent cache manager with different TTL strategies for different data types"""

    def __init__(self, cache_dir: str = "cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

        # Cache TTL (Time To Live) strategies in minutes
        # These values balance data freshness with API rate limits and performance
        self.cache_ttl = {
            "news": 15,  # News updates every 15 minutes - frequent enough for timely analysis
            "prices": 5,  # Prices update every 5 minutes - near real-time for active trading
            "company_names": 1440,  # Company names cache for 24 hours - rarely change
            "market_data": 10,  # Market indices every 10 minutes - important for market overview
            "policy_news": 30,  # Government news every 30 minutes - less frequent than market news
            "analyst_data": 60,  # Analyst recommendations every hour - change infrequently
            "ticker_info": 240,  # Basic ticker info every 4 hours - fundamental data changes slowly
            "earnings": 1440,  # Earnings data cache for 24 hours - quarterly updates only
        }

        # Request tracking for rate limiting
        self.request_log_file = self.cache_dir / "request_log.json"
        self.load_request_log()

        # Proactive refresh system
        self.refresh_queue = deque()  # Queue of items to refresh
        self.access_counts = defaultdict(int)  # Track access frequency
        self.refresh_callbacks = {}  # Registered refresh functions
        self.refresh_thread = None
        self.refresh_running = False
        self.refresh_lock = threading.Lock()

        # Intelligent cache warming system
        self.warming_callbacks = {}  # Registered warming functions
        self.access_patterns = defaultdict(list)  # Track access sequences
        self.related_data_map = self._build_related_data_map()  # Data relationships

        # Graceful degradation system
        self.graceful_degradation_enabled = True  # Enable serving stale data
        self.max_stale_multiplier = 2.0  # Serve data up to 2x TTL age
        self.pending_refreshes = set()  # Track items being refreshed

    def load_request_log(self):
        """Load request tracking log"""
        try:
            if self.request_log_file.exists():
                with open(self.request_log_file, "r") as f:
                    self.request_log = json.load(f)
            else:
                self.request_log = {}
        except (FileNotFoundError, json.JSONDecodeError, PermissionError):
            self.request_log = {}

    def save_request_log(self):
        """Save request tracking log"""
        try:
            with open(self.request_log_file, "w") as f:
                json.dump(self.request_log, f)
        except (OSError, PermissionError):
            pass

    def track_request(self, api_type: str, endpoint: str):
        """Track API requests for rate limiting analysis"""
        now = datetime.now().isoformat()
        key = f"{api_type}_{endpoint}"

        if key not in self.request_log:
            self.request_log[key] = []

        self.request_log[key].append(now)

        # Keep only last 24 hours of requests
        cutoff = datetime.now() - timedelta(hours=24)
        self.request_log[key] = [
            req for req in self.request_log[key] if datetime.fromisoformat(req) > cutoff
        ]

        self.save_request_log()

    def get_request_stats(self) -> Dict[str, int]:
        """Get request statistics for the last 24 hours"""
        stats = {}
        cutoff = datetime.now() - timedelta(hours=24)

        for key, requests in self.request_log.items():
            recent_requests = [
                req for req in requests if datetime.fromisoformat(req) > cutoff
            ]
            stats[key] = len(recent_requests)

        return stats

    def _get_cache_key(self, data_type: str, identifier: str) -> str:
        """Generate cache key"""
        return f"{data_type}_{hashlib.md5(identifier.encode()).hexdigest()}"

    def _get_cache_file(self, cache_key: str) -> Path:
        """Get cache file path"""
        return self.cache_dir / f"{cache_key}.cache"

    def is_cache_valid(self, data_type: str, identifier: str) -> bool:
        """Check if cached data is still valid"""
        cache_key = self._get_cache_key(data_type, identifier)
        cache_file = self._get_cache_file(cache_key)

        if not cache_file.exists():
            return False

        # Check TTL
        ttl_minutes = self.cache_ttl.get(data_type, 60)
        cutoff_time = datetime.now() - timedelta(minutes=ttl_minutes)

        try:
            file_time = datetime.fromtimestamp(cache_file.stat().st_mtime)
            return file_time > cutoff_time
        except (OSError, ValueError):
            return False

    def is_cache_stale_soon(
        self, data_type: str, identifier: str, threshold: float = 0.8
    ) -> bool:
        """Check if cached data will become stale soon (within threshold % of TTL)"""
        cache_key = self._get_cache_key(data_type, identifier)
        cache_file = self._get_cache_file(cache_key)

        if not cache_file.exists():
            return True  # No cache means it's "stale"

        # Check if we're within threshold % of TTL expiration
        ttl_minutes = self.cache_ttl.get(data_type, 60)
        stale_threshold_minutes = ttl_minutes * threshold
        cutoff_time = datetime.now() - timedelta(minutes=stale_threshold_minutes)

        try:
            file_time = datetime.fromtimestamp(cache_file.stat().st_mtime)
            return file_time <= cutoff_time
        except (OSError, ValueError):
            return True

    def get_cache_age_ratio(self, data_type: str, identifier: str) -> float:
        """Get how much of the TTL has elapsed (0.0 = fresh, 1.0 = expired)"""
        cache_key = self._get_cache_key(data_type, identifier)
        cache_file = self._get_cache_file(cache_key)

        if not cache_file.exists():
            return 1.0  # Fully expired/missing

        ttl_minutes = self.cache_ttl.get(data_type, 60)

        try:
            file_time = datetime.fromtimestamp(cache_file.stat().st_mtime)
            age_minutes = (datetime.now() - file_time).total_seconds() / 60
            return min(age_minutes / ttl_minutes, 1.0)
        except (OSError, ValueError):
            return 1.0

    def get_cached_data(self, data_type: str, identifier: str) -> Optional[Any]:
        """Get cached data with intelligent warming and graceful degradation"""
        # Use graceful degradation by default for better user experience
        return self.get_cached_data_with_graceful_degradation(data_type, identifier)

    def get_cached_data_strict(self, data_type: str, identifier: str) -> Optional[Any]:
        """Get cached data only if valid (strict mode - no stale data)"""
        # Track access for priority calculation
        cache_key = self._get_cache_key(data_type, identifier)
        self.access_counts[cache_key] += 1

        # Track access patterns for intelligent warming
        self._track_access_pattern(data_type, identifier)

        # Trigger intelligent warming for related data
        self._trigger_intelligent_warming(data_type, identifier)

        if not self.is_cache_valid(data_type, identifier):
            return None

        return self._load_cache_data(cache_key)

    def cache_data(self, data_type: str, identifier: str, data: Any) -> None:
        """Cache data"""
        cache_key = self._get_cache_key(data_type, identifier)
        cache_file = self._get_cache_file(cache_key)

        try:
            with open(cache_file, "wb") as f:
                pickle.dump(data, f)
        except Exception as e:
            print(f"⚠️ Failed to cache {data_type} for {identifier}: {e}")

    def get_or_fetch(
        self, data_type: str, identifier: str, fetch_function, *args, **kwargs
    ):
        """Get cached data or fetch new data"""
        # Try cache first
        cached_data = self.get_cached_data(data_type, identifier)
        if cached_data is not None:
            return cached_data, True  # True indicates cache hit

        # Fetch new data
        try:
            new_data = fetch_function(*args, **kwargs)
            self.cache_data(data_type, identifier, new_data)
            self.track_request(data_type, identifier)
            return new_data, False  # False indicates cache miss
        except Exception as e:
            print(f"⚠️ Failed to fetch {data_type} for {identifier}: {e}")
            return None, False

    def batch_get_or_fetch(
        self,
        data_type: str,
        identifiers: List[str],
        fetch_function,
        batch_size: int = 10,
    ):
        """Efficiently handle batch requests with caching"""
        results = {}
        cache_hits = 0
        cache_misses = []

        # Check cache for all identifiers
        for identifier in identifiers:
            cached_data = self.get_cached_data(data_type, identifier)
            if cached_data is not None:
                results[identifier] = cached_data
                cache_hits += 1
            else:
                cache_misses.append(identifier)

        # Fetch missing data in batches
        if cache_misses:
            for i in range(0, len(cache_misses), batch_size):
                batch = cache_misses[i : i + batch_size]
                try:
                    batch_results = fetch_function(batch)

                    # Cache individual results
                    for identifier in batch:
                        if identifier in batch_results:
                            self.cache_data(
                                data_type, identifier, batch_results[identifier]
                            )
                            results[identifier] = batch_results[identifier]
                            self.track_request(data_type, identifier)

                except Exception as e:
                    print(f"⚠️ Batch fetch failed for {data_type}: {e}")

        print(
            f"📊 Cache performance for {data_type}: {cache_hits} hits, {len(cache_misses)} misses"
        )
        return results

    def clear_cache(
        self, data_type: Optional[str] = None, older_than_hours: Optional[int] = None
    ):
        """Clear cache files"""
        if older_than_hours:
            cutoff_time = datetime.now() - timedelta(hours=older_than_hours)

        for cache_file in self.cache_dir.glob("*.cache"):
            should_delete = False

            if data_type:
                # Delete specific data type
                if cache_file.name.startswith(f"{data_type}_"):
                    should_delete = True
            elif older_than_hours:
                # Delete old files
                try:
                    file_time = datetime.fromtimestamp(cache_file.stat().st_mtime)
                    if file_time < cutoff_time:
                        should_delete = True
                except (OSError, ValueError):
                    should_delete = True
            else:
                # Delete all
                should_delete = True

            if should_delete:
                try:
                    cache_file.unlink()
                except OSError:
                    pass

    def _build_related_data_map(self) -> Dict[str, List[str]]:
        """Build a map of related data types for intelligent warming"""
        return {
            "prices": [
                "news",
                "earnings",
                "company_names",
            ],  # When viewing prices, warm news/earnings
            "news": ["prices", "earnings"],  # When viewing news, warm prices/earnings
            "earnings": ["prices", "news"],  # When viewing earnings, warm prices/news
            "market_data": ["policy_news"],  # When viewing market, warm policy
            "policy_news": ["market_data"],  # When viewing policy, warm market
        }

    def register_refresh_callback(self, data_type: str, callback: Callable):
        """Register a callback function for refreshing specific data types"""
        self.refresh_callbacks[data_type] = callback

    def register_warming_callback(self, data_type: str, callback: Callable):
        """Register a callback function for warming specific data types"""
        self.warming_callbacks[data_type] = callback

    def get_cached_data_with_graceful_degradation(
        self, data_type: str, identifier: str
    ) -> Optional[Any]:
        """Get cached data with graceful degradation - serves stale data while refreshing"""
        # Track access for priority calculation
        cache_key = self._get_cache_key(data_type, identifier)
        self.access_counts[cache_key] += 1

        # Track access patterns for intelligent warming
        self._track_access_pattern(data_type, identifier)

        # Trigger intelligent warming for related data
        self._trigger_intelligent_warming(data_type, identifier)

        # Check if data is fresh
        if self.is_cache_valid(data_type, identifier):
            return self._load_cache_data(cache_key)

        # Data is stale - check if graceful degradation is possible
        if self.graceful_degradation_enabled and self._can_serve_stale_data(
            data_type, identifier
        ):
            # Trigger background refresh if not already pending
            if cache_key not in self.pending_refreshes:
                self._trigger_background_refresh(data_type, identifier)

            # Serve stale data
            stale_data = self._load_cache_data(cache_key)
            if stale_data is not None:
                print(
                    f"🟡 Serving stale data for {data_type}:{identifier} while refreshing"
                )
                return stale_data

        # No valid data available
        return None

    def _can_serve_stale_data(self, data_type: str, identifier: str) -> bool:
        """Check if stale data can be served based on age limits"""
        try:
            cache_key = self._get_cache_key(data_type, identifier)
            cache_file = self._get_cache_file(cache_key)

            if not cache_file.exists():
                return False

            # Check if data is within acceptable staleness limits
            ttl_minutes = self.cache_ttl.get(data_type, 60)
            max_stale_minutes = ttl_minutes * self.max_stale_multiplier
            cutoff_time = datetime.now() - timedelta(minutes=max_stale_minutes)

            file_time = datetime.fromtimestamp(cache_file.stat().st_mtime)
            return file_time > cutoff_time

        except (OSError, ValueError):
            return False

    def _trigger_background_refresh(self, data_type: str, identifier: str):
        """Trigger background refresh for stale data"""
        try:
            cache_key = self._get_cache_key(data_type, identifier)

            # Mark as pending refresh
            self.pending_refreshes.add(cache_key)

            # Add to refresh queue with high priority
            with self.refresh_lock:
                priority = 10  # High priority for graceful degradation
                refresh_item = (data_type, identifier, priority)

                # Add to front of queue for immediate processing
                self.refresh_queue.appendleft(refresh_item)

        except Exception:
            pass  # Fail silently

    def _load_cache_data(self, cache_key: str) -> Optional[Any]:
        """Load data from cache file"""
        try:
            cache_file = self._get_cache_file(cache_key)
            with open(cache_file, "rb") as f:
                return pickle.load(f)
        except (OSError, pickle.PickleError, EOFError):
            return None

    def start_proactive_refresh(self):
        """Start the proactive refresh background thread"""
        if self.refresh_running:
            return

        self.refresh_running = True
        self.refresh_thread = threading.Thread(
            target=self._proactive_refresh_loop, daemon=True
        )
        self.refresh_thread.start()

    def stop_proactive_refresh(self):
        """Stop the proactive refresh background thread"""
        self.refresh_running = False
        if self.refresh_thread:
            self.refresh_thread.join(timeout=5)

    def _proactive_refresh_loop(self):
        """Main loop for proactive cache refresh"""
        while self.refresh_running:
            try:
                # Check all cached items for staleness
                self._check_and_queue_stale_items()

                # Process refresh queue
                self._process_refresh_queue()

                # Sleep for 30 seconds before next check
                time.sleep(30)

            except Exception as e:
                print(f"⚠️ Proactive refresh error: {e}")
                time.sleep(60)  # Wait longer on error

    def _check_and_queue_stale_items(self):
        """Check all cache files and queue items that are becoming stale"""
        try:
            cache_files = list(self.cache_dir.glob("*.cache"))

            for cache_file in cache_files:
                # Parse cache key to get data_type and identifier
                cache_key = cache_file.stem
                data_type, identifier = self._parse_cache_key(cache_key)

                if data_type and self.is_cache_stale_soon(
                    data_type, identifier, threshold=0.7
                ):
                    # Add to refresh queue with priority based on access frequency
                    priority = self.access_counts.get(cache_key, 0)
                    self._add_to_refresh_queue(data_type, identifier, priority)

        except Exception as e:
            print(f"⚠️ Error checking stale items: {e}")

    def _parse_cache_key(self, cache_key: str) -> Tuple[Optional[str], Optional[str]]:
        """Parse cache key to extract data_type and identifier"""
        # For now, we'll use a simpler approach - store metadata in cache files
        # or maintain a reverse lookup. For this implementation, we'll check
        # all cache files and determine their type based on TTL patterns

        # Try to determine data type by checking file age against known TTLs
        cache_file = self._get_cache_file(cache_key)
        if not cache_file.exists():
            return None, None

        try:
            file_time = datetime.fromtimestamp(cache_file.stat().st_mtime)
            age_minutes = (datetime.now() - file_time).total_seconds() / 60

            # Match age against TTL patterns to guess data type
            for data_type, ttl in self.cache_ttl.items():
                age_ratio = age_minutes / ttl
                if 0 <= age_ratio <= 1.2:  # Within reasonable range
                    # Use a generic identifier for the data type
                    return data_type, f"item_{cache_key[:8]}"

            # Default to prices if we can't determine
            return "prices", f"item_{cache_key[:8]}"

        except (OSError, ValueError):
            return None, None

    def _add_to_refresh_queue(self, data_type: str, identifier: str, priority: int = 0):
        """Add item to refresh queue with priority"""
        with self.refresh_lock:
            # Avoid duplicates
            item = (data_type, identifier, priority)
            if item not in self.refresh_queue:
                self.refresh_queue.append(item)
                # Sort by priority (higher priority first)
                self.refresh_queue = deque(
                    sorted(self.refresh_queue, key=lambda x: x[2], reverse=True)
                )

    def _process_refresh_queue(self):
        """Process items in the refresh queue"""
        processed = 0
        max_per_cycle = 5  # Limit refreshes per cycle to avoid overwhelming APIs

        while self.refresh_queue and processed < max_per_cycle:
            with self.refresh_lock:
                if not self.refresh_queue:
                    break

                # Handle different queue item formats
                queue_item = self.refresh_queue.popleft()
                if len(queue_item) == 3:
                    data_type, identifier, priority = queue_item
                    is_warming = False
                elif len(queue_item) == 4:
                    # Warming task format: (warming_key, data_type, identifier, priority)
                    warming_key, data_type, identifier, priority = queue_item
                    is_warming = warming_key.startswith("warm_")
                else:
                    continue  # Skip malformed items

            # Execute appropriate callback
            try:
                if is_warming and data_type in self.warming_callbacks:
                    # Execute warming callback
                    self.warming_callbacks[data_type](identifier)
                    print(f"🧠 Intelligently warmed {data_type}:{identifier}")
                elif data_type in self.refresh_callbacks:
                    # Execute refresh callback
                    self.refresh_callbacks[data_type](identifier)

                    # Remove from pending refreshes if this was a graceful degradation refresh
                    cache_key = self._get_cache_key(data_type, identifier)
                    self.pending_refreshes.discard(cache_key)

                    print(f"🔄 Proactively refreshed {data_type}:{identifier}")

                processed += 1

            except Exception as e:
                print(f"⚠️ Failed to process {data_type}:{identifier}: {e}")

            # Small delay between refreshes
            time.sleep(1)

    def _track_access_pattern(self, data_type: str, identifier: str):
        """Track access patterns for intelligent warming"""
        try:
            # Store recent access pattern (last 10 accesses)
            pattern_key = f"{data_type}:{identifier}"
            current_time = time.time()

            # Add current access to pattern
            self.access_patterns[pattern_key].append(current_time)

            # Keep only recent accesses (last 10)
            if len(self.access_patterns[pattern_key]) > 10:
                self.access_patterns[pattern_key] = self.access_patterns[pattern_key][
                    -10:
                ]

        except Exception:
            pass  # Fail silently

    def _trigger_intelligent_warming(self, data_type: str, identifier: str):
        """Trigger intelligent warming of related data"""
        try:
            # Only warm if this is a frequently accessed item
            cache_key = self._get_cache_key(data_type, identifier)
            access_count = self.access_counts.get(cache_key, 0)

            # Trigger warming for frequently accessed items (3+ accesses)
            if access_count >= 3:
                self._warm_related_data(data_type, identifier)

        except Exception:
            pass  # Fail silently

    def _warm_related_data(self, data_type: str, identifier: str):
        """Warm related data based on data relationships"""
        try:
            # Get related data types
            related_types = self.related_data_map.get(data_type, [])

            for related_type in related_types:
                # Check if related data needs warming
                if self._should_warm_related_data(related_type, identifier):
                    self._queue_warming_task(related_type, identifier)

        except Exception:
            pass  # Fail silently

    def _should_warm_related_data(self, data_type: str, identifier: str) -> bool:
        """Check if related data should be warmed"""
        try:
            # Don't warm if data is already fresh
            if self.is_cache_valid(data_type, identifier):
                age_ratio = self.get_cache_age_ratio(data_type, identifier)
                if age_ratio < 0.5:  # Less than 50% of TTL elapsed
                    return False

            # Don't warm if already in warming queue
            warming_key = f"warm_{data_type}_{identifier}"
            if any(item[0] == warming_key for item in self.refresh_queue):
                return False

            return True

        except Exception:
            return False

    def _queue_warming_task(self, data_type: str, identifier: str):
        """Queue a warming task for background execution"""
        try:
            with self.refresh_lock:
                # Add warming task to refresh queue with lower priority
                warming_key = f"warm_{data_type}_{identifier}"
                priority = 1  # Lower priority than regular refresh tasks

                # Add to queue if not already present
                warming_item = (warming_key, data_type, identifier, priority)
                if warming_item not in self.refresh_queue:
                    self.refresh_queue.append(warming_item)

        except Exception:
            pass  # Fail silently

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        # Count warming tasks in queue
        warming_tasks = sum(
            1
            for item in self.refresh_queue
            if len(item) >= 4 and item[0].startswith("warm_")
        )

        stats = {
            "cache_files": len(list(self.cache_dir.glob("*.cache"))),
            "cache_size_mb": sum(
                f.stat().st_size for f in self.cache_dir.glob("*.cache")
            )
            / (1024 * 1024),
            "request_stats": self.get_request_stats(),
            "cache_ttl": self.cache_ttl,
            "refresh_queue_size": len(self.refresh_queue),
            "warming_tasks": warming_tasks,
            "pending_refreshes": len(self.pending_refreshes),
            "graceful_degradation_enabled": self.graceful_degradation_enabled,
            "access_patterns": len(self.access_patterns),
            "most_accessed": dict(
                sorted(self.access_counts.items(), key=lambda x: x[1], reverse=True)[
                    :10
                ]
            ),
        }
        return stats


# Global cache manager instance
cache_manager = CacheManager()
