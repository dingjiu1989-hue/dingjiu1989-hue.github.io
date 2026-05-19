---
title: "Full-Text Search in PostgreSQL: tsvector, tsquery, GIN Indexes"
description: "Learn full-text search in PostgreSQL using tsvector, tsquery, and GIN indexes. Understand ranking, stemming, and when to use PostgreSQL vs Elasticsearch."
date: 2026-04-06
board: database
url: https://dingjiu1989-hue.github.io/en/database/full-text-search-postgresql.html
---

# Full-Text Search in PostgreSQL: tsvector, tsquery, GIN Indexes

## Full-Text Search in PostgreSQL: tsvector, tsquery, GIN Indexes

### Full-Text Search in PostgreSQL: tsvector, tsquery, GIN Indexes

#### Full-Text Search in PostgreSQL: tsvector, tsquery, GIN Indexes

#### Full-Text Search in PostgreSQL: tsvector, tsquery, GIN Indexes

#### Full-Text Search in PostgreSQL: tsvector, tsquery, GIN Indexes

#### Full-Text Search in PostgreSQL: tsvector, tsquery, GIN Indexes

#### Full-Text Search in PostgreSQL: tsvector, tsquery, GIN Indexes

#### Full-Text Search in PostgreSQL: tsvector, tsquery, GIN Indexes

#### Full-Text Search in PostgreSQL: tsvector, tsquery, GIN Indexes

#### Full-Text Search in PostgreSQL: tsvector, tsquery, GIN Indexes

#### Full-Text Search in PostgreSQL: tsvector, tsquery, GIN Indexes

#### Full-Text Search in PostgreSQL: tsvector, tsquery, GIN Indexes

#### Full-Text Search in PostgreSQL: tsvector, tsquery, GIN Indexes

#### Full-Text Search in PostgreSQL: tsvector, tsquery, GIN Indexes

#### Full-Text Search in PostgreSQL: tsvector, tsquery, GIN Indexes

Full-Text Search in PostgreSQL: tsvector, tsquery, GIN Indexes 

PostgreSQL's full-text search (FTS) provides built-in text search capabilities without external dependencies. While not as feature-rich as Elasticsearch or Meilisearch, it handles a large class of search needs efficiently. 

The FTS Pipeline 

Full-text search in PostgreSQL follows this flow: 

  * **Parsing** : Break text into tokens (lexemes).



2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Normalization** : Convert tokens to a standard form via a dictionary (stemming, stop words). 3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Indexing** : Store the normalized tokens in a `tsvector`. 4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Querying** : Match a `tsquery` against the `tsvector` using a GIN index. 

tsvector and tsquery 

tsvector 

A `tsvector` is a sorted list of distinct lexemes with positional information: 

SELECT to_tsvector('english',

'The quick brown fox jumps over the lazy dog');

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- 'brown':3 'dog':9 'fox':4 'jump':5 'lazy':8 'quick':2

Notice "jumps" became "jump" (stemming), and "the", "over" are removed (stop words). 

tsquery 

A `tsquery` represents a search query: 

SELECT to_tsquery('english', 'fox & dog');

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- 'fox' & 'dog'

SELECT to_tsquery('english', 'jump | run');

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- 'jump' | 'run'

SELECT to_tsquery('english', '!cat');

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- !'cat'

SELECT to_tsquery('english', 'quick <-> brown');

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- 'quick' <-> 'brown' (adjacency: quick followed by brown)

Basic Search 

SELECT title, body

FROM articles

WHERE to_tsvector('english', body) @@ to_tsquery('english', 'database & performance');

Creating a Search Column 

For production use, store the `tsvector` in a generated column to avoid repeated conversion: 

ALTER TABLE articles

ADD COLUMN search_vector tsvector

GENERATED ALWAYS AS (

to_tsvector('english', coalesce(title, '') || ' ' || coalesce(body, ''))

) STORED;

CREATE INDEX idx_articles_search ON articles USING GIN (search_vector);

Now queries become: 

SELECT title, body

FROM articles

WHERE search_vector @@ to_tsquery('english', 'postgresql & indexing');

Search Ranking 

PostgreSQL offers ranking functions to sort results by relevance: 

SELECT title,

ts_rank(search_vector, query) AS rank

FROM articles,

to_tsquery('english', 'postgresql & performance') AS query

WHERE search_vector @@ query

ORDER BY rank DESC

LIMIT 20;

`ts_rank` considers term frequency (TF) and inverse document frequency (IDF). A variant `ts_rank_cd` uses cover density, which rewards terms that appear close together: 

SELECT title,

ts_rank_cd(search_vector, query) AS rank

FROM articles, to_tsquery('english', 'database & indexing') AS query

WHERE search_vector @@ query

ORDER BY rank DESC;

Highlighting 

SELECT title,

ts_headline('english', body, query,

'StartSel=, StopSel=') AS highlighted

FROM articles, to_tsquery('english', 'performance & tuning') AS query

WHERE search_vector @@ query;

Multi-Column and Weighted Search 

Assign different weights to columns for ranking: 

ALTER TABLE articles ADD COLUMN search_weighted tsvector

GENERATED ALWAYS AS (

setweight(to_tsvector('english', coalesce(title, '')), 'A') ||

setweight(to_tsvector('english', coalesce(body, '')), 'B')

) STORED;

CREATE INDEX idx_articles_weighted ON articles USING GIN (search_weighted);

The weight function `ts_rank` can use these weights: 

SELECT title,

ts_rank('{0.1, 0.2, 0.4, 1.0}', search_weighted, query) AS rank

FROM articles, to_tsquery('english', 'indexing') AS query

WHERE search_weighted @@ query

ORDER BY rank DESC;

Dictionaries and Custom Configurations 

PostgreSQL supports multiple text search dictionaries: 

  * `english_stem`: Snowball stemmer for English.

  * `simple`: Lowercase conversion only.

  * `unaccent`: Remove diacritics (requires extension).

  * `thesaurus`: Synonym expansion.




Create a custom configuration: 

CREATE TEXT SEARCH CONFIGURATION my_search (COPY = english);

CREATE TEXT SEARCH DICTIONARY my_thesaurus (

TEMPLATE = thesaurus,

DICTFILE = 'my_thesaurus.ths'

);

ALTER TEXT SEARCH CONFIGURATION my_search

ALTER MAPPING FOR asciiword

WITH my_thesaurus, english_stem;

SELECT to_tsvector('my_search', 'The database is performing well');

PostgreSQL vs Elasticsearch 

| Aspect | PostgreSQL FTS | Elasticsearch | |--------|---------------|---------------| | Setup | Built-in, no extra service | Separate cluster, JVM | | Index freshness | Real-time within transaction | Near-real-time (refresh interval) | | Ranking | TF-IDF based | BM25, learning-to-rank | | Faceted search | GROUP BY with tsvector | Dedicated aggregation API | | Scale | Single node + replicas | Distributed by design | | Fuzzy search | pg_trgm extension | Built-in fuzzy matching | | Language support | 20+ languages via Snowball | 40+ language analyzers | | Query syntax | @@ tsquery operator | JSON-based Query DSL | 

Performance Tuning 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Analyze GIN index usage

SELECT relname, seq_scan, idx_scan

FROM pg_stat_all_indexes

WHERE indexrelname = 'idx_articles_search';

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Track search index size

SELECT pg_size_pretty(pg_indexes_size('articles'));

For large datasets (millions of documents), consider: 

  * Partial indexes for recent documents if search is time-sensitive:



CREATE INDEX idx_recent_search ON articles USING GIN (search_vector)

WHERE published_at > now() - interval '30 days';

  * Partitioning the table by date and creating GIN indexes per partition.

  * Using `pg_trgm` for prefix/similarity matching as a complement to FTS:




CREATE INDEX idx_articles_title_trgm ON articles USING GIN (title gin_trgm_ops);

SELECT * FROM articles WHERE title % 'databas'; -- similarity search

PostgreSQL full-text search is adequate for the majority of applications: documentation sites, blog search, e-commerce product search, and knowledge bases. Consider dedicated search engines only when you need fuzzy matching, faceted aggregation across millions of documents, or distributed search at scale.

**See also:** [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [B-Tree, Hash, GiST, GIN: Index Type Selection Guide](</en/database/database-index-types.html>), [Stored Procedures vs Functions: When to Use, Languages, Security](</en/database/stored-procedures.html>).

**See also:** [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [Index Maintenance: Bloat, Rebuild, Reindex, and Fillfactor Tuning](</en/database/index-maintenance.html>), [Stored Procedures vs Functions: When to Use, Languages, Security](</en/database/stored-procedures.html>)

**See also:** [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [Index Maintenance: Bloat, Rebuild, Reindex, and Fillfactor Tuning](</en/database/index-maintenance.html>), [Stored Procedures vs Functions: When to Use, Languages, Security](</en/database/stored-procedures.html>)

**See also:** [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [Index Maintenance: Bloat, Rebuild, Reindex, and Fillfactor Tuning](</en/database/index-maintenance.html>), [Stored Procedures vs Functions: When to Use, Languages, Security](</en/database/stored-procedures.html>)

**See also:** [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [Index Maintenance: Bloat, Rebuild, Reindex, and Fillfactor Tuning](</en/database/index-maintenance.html>), [Stored Procedures vs Functions: When to Use, Languages, Security](</en/database/stored-procedures.html>)

**See also:** [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [Index Maintenance: Bloat, Rebuild, Reindex, and Fillfactor Tuning](</en/database/index-maintenance.html>), [Stored Procedures vs Functions: When to Use, Languages, Security](</en/database/stored-procedures.html>)
