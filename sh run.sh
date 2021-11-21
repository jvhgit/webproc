Help on method search in module elasticsearch._async.client:

sseeaarrcchh(body=None, index=None, doc_type=None, params=None, headers=None) method of elasticsearch._async.client.AsyncElasticsearch instance
    Returns results matching a query.
    `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/search-search.html>`_
    
    :arg body: The search definition using the Query DSL
    :arg index: A comma-separated list of index names to search; use
        `_all` or empty string to perform the operation on all indices
    :arg doc_type: A comma-separated list of document types to
        search; leave empty to perform the operation on all types
    :arg _source: True or false to return the _source field or not,
        or a list of fields to return
    :arg _source_excludes: A list of fields to exclude from the
        returned _source field
    :arg _source_includes: A list of fields to extract and return
        from the _source field
    :arg allow_no_indices: Whether to ignore if a wildcard indices
        expression resolves into no concrete indices. (This includes `_all`
        string or when no indices have been specified)
    :arg allow_partial_search_results: Indicate if an error should
        be returned if there is a partial search failure or timeout  Default:
        True
    :arg analyze_wildcard: Specify whether wildcard and prefix
        queries should be analyzed (default: false)
    :arg analyzer: The analyzer to use for the query string
    :arg batched_reduce_size: The number of shard results that
        should be reduced at once on the coordinating node. This value should be
        used as a protection mechanism to reduce the memory overhead per search
        request if the potential number of shards in the request can be large.
        Default: 512
    :arg ccs_minimize_roundtrips: Indicates whether network round-
        trips should be minimized as part of cross-cluster search requests
        execution  Default: true
    :arg default_operator: The default operator for query string
        query (AND or OR)  Valid choices: AND, OR  Default: OR
    :arg df: The field to use as default where no field prefix is
        given in the query string
    :arg docvalue_fields: A comma-separated list of fields to return
        as the docvalue representation of a field for each hit
    :arg expand_wildcards: Whether to expand wildcard expression to
        concrete indices that are open, closed or both.  Valid choices: open,
        closed, hidden, none, all  Default: open
    :arg explain: Specify whether to return detailed information
        about score computation as part of a hit
    :arg from_: Starting offset (default: 0)
    :arg ignore_throttled: Whether specified concrete, expanded or
        aliased indices should be ignored when throttled
    :arg ignore_unavailable: Whether specified concrete indices
        should be ignored when unavailable (missing or closed)
    :arg lenient: Specify whether format-based query failures (such
        as providing text to a numeric field) should be ignored
    :arg max_concurrent_shard_requests: The number of concurrent
        shard requests per node this search executes concurrently. This value
        should be used to limit the impact of the search on the cluster in order
        to limit the number of concurrent shard requests  Default: 5
    :arg pre_filter_shard_size: A threshold that enforces a pre-
        filter roundtrip to prefilter search shards based on query rewriting if
        the number of shards the search request expands to exceeds the
        threshold. This filter roundtrip can limit the number of shards
        significantly if for instance a shard can not match any documents based
        on its rewrite method ie. if date filters are mandatory to match but the
        shard bounds and the query are disjoint.
    :arg preference: Specify the node or shard the operation should
        be performed on (default: random)
    :arg q: Query in the Lucene query string syntax
    :arg request_cache: Specify if request cache should be used for
        this request or not, defaults to index level setting
    :arg rest_total_hits_as_int: Indicates whether hits.total should
        be rendered as an integer or an object in the rest search response
    :arg routing: A comma-separated list of specific routing values
    :arg scroll: Specify how long a consistent view of the index
        should be maintained for scrolled search
    :arg search_type: Search operation type  Valid choices:
        query_then_fetch, dfs_query_then_fetch
    :arg seq_no_primary_term: Specify whether to return sequence
        number and primary term of the last modification of each hit
    :arg size: Number of hits to return (default: 10)
    :arg sort: A comma-separated list of <field>:<direction> pairs
    :arg stats: Specific 'tag' of the request for logging and
        statistical purposes
    :arg stored_fields: A comma-separated list of stored fields to
        return as part of a hit
    :arg suggest_field: Specify which field to use for suggestions
    :arg suggest_mode: Specify suggest mode  Valid choices: missing,
        popular, always  Default: missing
    :arg suggest_size: How many suggestions to return in response
    :arg suggest_text: The source text for which the suggestions
        should be returned
    :arg terminate_after: The maximum number of documents to collect
        for each shard, upon reaching which the query execution will terminate
        early.
    :arg timeout: Explicit operation timeout
    :arg track_scores: Whether to calculate and return scores even
        if they are not used for sorting
    :arg track_total_hits: Indicate if the number of documents that
        match the query should be tracked
    :arg typed_keys: Specify whether aggregation and suggester names
        should be prefixed by their respective types in the response
    :arg version: Specify whether to return document version as part
        of a hit
