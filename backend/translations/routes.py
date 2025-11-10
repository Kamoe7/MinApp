from flask import Blueprint, jsonify
import time
from config import Config
from utils.database import get_connection


translations_bp = Blueprint(
    'translations', __name__, url_prefix='/api/translations')
# cache memory
translations_cache = {}
cache_timestamp = {}
CACHE_DURATIONS = 300


@translations_bp.route('/<lang>', methods=['GET'])
def get_translations(lang):
    if lang not in ['sv', 'en']:
        return jsonify({'error': 'Not Valid language'}), 400
    try:
        current_time = time.time()
        if lang in translations_cache and lang in cache_timestamp:
            if current_time - cache_timestamp[lang] < CACHE_DURATIONS:
                print(f"reuturn cache transt for :{lang}")
                return jsonify(translations_cache[lang])

        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT key, sv ,en FROM translations')
        translations = cur.fetchall()
        cur.close()
        conn.close()

        result = {}
        for row in translations:
            result[row['key']] = row[lang]

        translations_cache[lang] = result
        cache_timestamp[lang] = current_time
        print(f"sending {len(result)} translations for lang: {lang}")
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@translations_bp.route('/<lang>/<page>', methods=['GET'])
def get_page_translations(lang, page):
    if lang not in ['sv', 'en']:
        return jsonify({'error': 'Invalid lang'}), 400

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            ' SELECT key,sv,en FROM translations WHERE page = %s', (page))
        translations = cur.fetchall()
        cur.close()
        conn.close()

        result = {}
        for row in translations:
            result[row['key']] = row[lang]

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': 'str(e)'}), 500
