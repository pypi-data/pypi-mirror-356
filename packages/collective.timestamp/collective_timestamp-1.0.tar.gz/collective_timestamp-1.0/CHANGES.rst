Changelog
=========


1.0 (2025-06-19)
----------------

- Refactor the `timestamp` utils function to be able to use failover urls and exp. backoff retries.
  [aduchene]
- Add settings to manage failover urls and exp. backoff retries.
  [aduchene]


1.0a2 (2024-10-11)
------------------

- Added `TimeStamper._effective_related_indexes` to factorize the list of
  catalog indexes related to the `effective` functionality.
  Make `TimeStamper.timestamp` return data and timestamp in case it is overrided
  or called from external code.
  [gbastien]


1.0a1 (2024-09-17)
------------------

- Initial release.
  [laulaz]
