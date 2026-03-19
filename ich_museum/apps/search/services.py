"""Search service layer using Elasticsearch."""
import logging
import os
from elasticsearch import Elasticsearch, NotFoundError

logger = logging.getLogger(__name__)

ES_URL = os.getenv('ELASTICSEARCH_URL', 'http://localhost:9200')
INDEX_NAME = 'heritage_items'

_es_client = None


def _get_client():
    global _es_client
    if _es_client is None:
        _es_client = Elasticsearch(ES_URL)
    return _es_client


def ensure_index():
    """Create the heritage_items index if it doesn't exist."""
    es = _get_client()
    if es.indices.exists(index=INDEX_NAME):
        return
    es.indices.create(index=INDEX_NAME, body={
        'settings': {
            'analysis': {
                'analyzer': {
                    'ik_smart_analyzer': {
                        'type': 'custom',
                        'tokenizer': 'ik_smart',
                    }
                }
            }
        },
        'mappings': {
            'properties': {
                'name': {'type': 'text', 'analyzer': 'ik_smart_analyzer', 'fields': {'keyword': {'type': 'keyword'}}},
                'name_en': {'type': 'text', 'analyzer': 'standard'},
                'summary': {'type': 'text', 'analyzer': 'ik_smart_analyzer'},
                'summary_en': {'type': 'text', 'analyzer': 'standard'},
                'description': {'type': 'text', 'analyzer': 'ik_smart_analyzer'},
                'description_en': {'type': 'text', 'analyzer': 'standard'},
                'category': {'type': 'keyword'},
                'category_en': {'type': 'keyword'},
                'region': {'type': 'keyword'},
                'region_en': {'type': 'keyword'},
                'status': {'type': 'keyword'},
            }
        }
    })
    logger.info('Created Elasticsearch index: %s', INDEX_NAME)


def sync_item_index(item_id):
    """Sync a heritage item to Elasticsearch index."""
    from apps.heritage.services import get_item_summary
    try:
        es = _get_client()
        data = get_item_summary(item_id)
        if not data or data.get('status') != 'published':
            # Remove from index if not published
            try:
                es.delete(index=INDEX_NAME, id=str(item_id))
            except NotFoundError:
                pass
            return
        es.index(index=INDEX_NAME, id=str(item_id), body=data)
        logger.debug('Synced item %s to ES', item_id)
    except Exception:
        logger.warning('Failed to sync item %s to ES', item_id, exc_info=True)


def remove_item_index(item_id):
    """Remove a heritage item from Elasticsearch index."""
    try:
        es = _get_client()
        es.delete(index=INDEX_NAME, id=str(item_id))
    except NotFoundError:
        pass
    except Exception:
        logger.warning('Failed to remove item %s from ES', item_id, exc_info=True)


def search_items(query, category=None, page=1, page_size=12):
    """Search heritage items. Returns (ids, total)."""
    try:
        es = _get_client()
        must = [{'term': {'status': 'published'}}]
        should = []

        if query:
            should = [
                {'match': {'name': {'query': query, 'boost': 3}}},
                {'match': {'name_en': {'query': query, 'boost': 3}}},
                {'match': {'summary': {'query': query, 'boost': 2}}},
                {'match': {'summary_en': {'query': query, 'boost': 2}}},
                {'match': {'description': {'query': query}}},
                {'match': {'description_en': {'query': query}}},
            ]

        if category:
            must.append({'term': {'category': category}})

        body = {
            'query': {
                'bool': {
                    'must': must,
                    'should': should,
                    'minimum_should_match': 1 if should else 0,
                }
            },
            'from': (page - 1) * page_size,
            'size': page_size,
            '_source': False,
        }

        result = es.search(index=INDEX_NAME, body=body)
        ids = [hit['_id'] for hit in result['hits']['hits']]
        total = result['hits']['total']['value']
        return ids, total
    except Exception:
        logger.warning('ES search failed, falling back to empty results', exc_info=True)
        return [], 0
