---
title: "Full-Text Search Engines (Elasticsearch, Meilisearch, Typesense)"
description: "Compare Elasticsearch, Meilisearch, and Typesense for full-text search capabilities, performance, ease of use, and deployment models."
date: 2026-05-11
board: database
url: https://dingjiu1989-hue.github.io/en/database/full-text-search.html
---

# Full-Text Search Engines (Elasticsearch, Meilisearch, Typesense)

The Need for Full-Text Search   
Standard database `LIKE` queries do not scale. They require full table scans, do not understand relevance ranking, and cannot handle typo tolerance, stemming, or faceted search. Dedicated search engines solve these problems with inverted indexes, relevance scoring, and specialized query parsing.   
How Search Engines Work   
An inverted index maps terms to the documents containing them:   

    Document 1: "The quick brown fox"

    Document 2: "The lazy dog"

    Inverted Index:

    "the"   -> [Doc1, Doc2]

    "quick" -> [Doc1]

    "brown" -> [Doc1]

    "fox"   -> [Doc1]

    "lazy"  -> [Doc2]

    "dog"   -> [Doc2]

When searching for "brown fox," the engine finds documents containing both terms and ranks them by relevance.   
Search Engine Comparison   
| Feature | Elasticsearch | Meilisearch | Typesense | |---------|--------------|-------------|-----------| | Setup complexity | High | Low | Low | | Query language | Query DSL (JSON) | Simple search parameters | Simple API | | Relevance tuning | BM25, custom scripts | Built-in (good defaults) | Built-in (good defaults) | | Typo tolerance | Via fuzzy queries | Built-in (excellent) | Built-in (excellent) | | Faceted search | Excellent | Good | Good | | Geospatial search | Excellent | Limited | Built-in | | Scalability | Very high | Moderate | High | | Resource usage | High (Java JVM) | Low (Rust) | Low (C++) | | Managed service | Elastic Cloud | Meilisearch Cloud | Typesense Cloud |   
Elasticsearch   
Indexing Data   

    // Create index with mapping

    PUT /articles

    {

      "settings": {

        "analysis": {

          "analyzer": {

            "custom_analyzer": {

              "type": "standard",

              "stopwords": "_english_"

            }

          }

        }

      },

      "mappings": {

        "properties": {

          "title": {

            "type": "text",

            "analyzer": "custom_analyzer",

            "fields": {

              "keyword": { "type": "keyword" }

            }

          },

          "content": { "type": "text" },

          "author": { "type": "keyword" },

          "tags": { "type": "keyword" },

          "published_at": { "type": "date" },

          "views": { "type": "integer" }

        }

      }

    }

    // Index a document

    POST /articles/_doc/1

    {

      "title": "Database Indexing Strategies",

      "content": "A comprehensive guide to indexing...",

      "author": "alice",

      "tags": ["database", "performance"],

      "published_at": "2026-05-11",

      "views": 1200

    }

Searching   

    // Full-text search with relevance

    GET /articles/_search

    {

      "query": {

        "bool": {

          "must": [

            {

              "multi_match": {

                "query": "database indexing performance",

                "fields": ["title^3", "content^1"],  // Title is 3x more important

                "type": "best_fields"

              }

            }

          ],

          "filter": [

            { "term": { "author": "alice" } },

            { "range": { "views": { "gte": 100 } } }

          ]

        }

      },

      "sort": [

        { "_score": "desc" },

        { "published_at": "desc" }

      ],

      "from": 0,

      "size": 20,

      "aggs": {

        "by_tag": {

          "terms": { "field": "tags" }

        }

      }

    }

    from elasticsearch import Elasticsearch

    es = Elasticsearch(['https://localhost:9200'])

    results = es.search(

        index='articles',

        query={

            'multi_match': {

                'query': 'database indexing',

                'fields': ['title^3', 'content']

            }

        },

        aggs={'by_tag': {'terms': {'field': 'tags'}}},

        size=20

    )

    for hit in results['hits']['hits']:

        print(f"{hit['_score']:.2f}: {hit['_source']['title']}")

    # Facet results

    for bucket in results['aggregations']['by_tag']['buckets']:

        print(f"{bucket['key']}: {bucket['doc_count']} articles")

Meilisearch   
Meilisearch focuses on developer experience with sensible defaults and instant typo-tolerant search.   
Setup   

    docker run -it --rm \

        -p 7700:7700 \

        -v $(pwd)/meili_data:/meili_data \

        getmeili/meilisearch:v1.6 \

        --master-key=MASTER_KEY

Indexing and Search   

    const { MeiliSearch } = require('meilisearch');

    const client = new MeiliSearch({

        host: 'http://localhost:7700',

        apiKey: 'MASTER_KEY',

    });

    // Index documents

    const index = client.index('articles');

    await index.addDocuments([

        {

            id: 1,

            title: "Database Indexing Strategies",

            content: "A comprehensive guide...",

            tags: ["database", "performance"],

            views: 1200

        }

    ]);

    // Configure searchable attributes

    await index.updateSearchableAttributes(['title', 'content']);

    await index.updateSortableAttributes(['views', 'published_at']);

    await index.updateFilterableAttributes(['tags', 'author']);

    // Search (typo tolerance built-in)

    const results = await index.search('database indexing', {

        limit: 20,

        filter: 'views > 100',

        sort: ['views:desc']

    });

Typesense   
Typesense is a fast, typo-tolerant search engine written in C++.   
Setup   

    # docker-compose.yml

    version: '3'

    services:

      typesense:

        image: typesense/typesense:27.0

        ports:

          - "8108:8108"

        environment:

          TYPESENSE_API_KEY: "xyz"

          TYPESENSE_DATA_DIR: /data

        volumes:

          - ./typesense-data:/data

Indexing and Search   

    import typesense

    client = typesense.Client({

        'nodes': [{'host': 'localhost', 'port': '8108', 'protocol': 'http'}],

        'api_key': 'xyz',

    })

    # Create collection (schema)

    client.collections.create({

        'name': 'articles',

        'fields': [

            {'name': 'title', 'type': 'string'},

            {'name': 'content', 'type': 'string'},

            {'name': 'tags', 'type': 'string[]', 'facet': True},

            {'name': 'views', 'type': 'int32'},

            {'name': 'published_at', 'type': 'int64'},

        ],

        'default_sorting_field': 'views'

    })

    # Index documents

    client.collections['articles'].documents.create({

        'id': '1',

        'title': 'Database Indexing Strategies',

        'content': 'A comprehensive guide...',

        'tags': ['database', 'performance'],

        'views': 1200,

        'published_at': 1715385600

    })

    # Search

    results = client.collections['articles'].documents.search({

        'q': 'database indexing',

        'query_by': 'title,content',

        'filter_by': 'views:>100',

        'sort_by': 'views:desc',

        'facet_by': 'tags',

        'per_page': 20

    })

When to Use Which   
| Scenario | Recommended | |----------|-------------| | Complex analytics with search | Elasticsearch | | Simple, fast search out of the box | Meilisearch | | Low-latency search on limited hardware | Typesense | | Log analysis and observability | Elasticsearch (ELK stack) | | E-commerce product search | Meilisearch or Typesense | | Geo-search and aggregations | Elasticsearch | | Typo-tolerant search for user-facing features | Meilisearch | | Large-scale (100M+ documents) | Elasticsearch |   
Summary   
Full-text search engines are essential for applications that need more than simple SQL LIKE queries. Elasticsearch offers the most features and scalability at the cost of operational complexity. Meilisearch provides the best developer experience with instant typo tolerance and sensible defaults. Typesense offers excellent performance with minimal resource usage. Choose based on your scale, feature requirements, and operational capacity: start with Meilisearch or Typesense for typical web applications and move to Elasticsearch when you need advanced analytics or larger scale.
