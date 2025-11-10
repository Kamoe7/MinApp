from flask import Blueprint, jsonify, request
import psycopg
from psycopg.rows import dict_row
from utils.database import get_connection
from middleware.auth import token_required

pricelist_bp = Blueprint('pricelist', __name__, url_prefix='/api/pricelist')


@pricelist_bp.route('', methods=['GET'])
@token_required
def get_pricelist(current_user):
    """Get all pricelist items -"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('''
            SELECT id, product_name, description, price, currency 
            FROM pricelist 
            ORDER BY id
        ''')
        items = cur.fetchall()
        cur.close()
        conn.close()

        return jsonify([dict(item) for item in items]), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch pricelist'}), 500



@pricelist_bp.route('/products', methods=['GET'])
@token_required
def get_products(current_user):
    """Get all products with optional search filters  """
    search_article = request.args.get('search_article', '')
    search_product = request.args.get('search_product', '')
    limit = request.args.get('limit', 100, type=int)
    offset = request.args.get('offset', 0, type=int)

    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM products WHERE 1=1"
        params = []

        if search_article:
            query += " AND article_no ILIKE %s"
            params.append(f"%{search_article}%")

        if search_product:
            query += " AND product_service ILIKE %s"
            params.append(f"%{search_product}%")

        query += " ORDER BY id LIMIT %s OFFSET %s"
        params.extend([limit, offset])

        cursor.execute(query, params)
        products = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify([dict(p) for p in products])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@pricelist_bp.route('/products/<int:product_id>', methods=['GET'])
@token_required
def get_product(current_user, product_id):
    """Get single product by ID """
    try:
        conn = get_connection()
        cursor = conn.cursor(row_factory=dict_row)
        cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        product = cursor.fetchone()
        cursor.close()
        conn.close()

        if not product:
            return jsonify({"error": "Product not found"}), 404

        return jsonify(dict(product))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@pricelist_bp.route('/products', methods=['POST'])
@token_required
def create_product(current_user):
    """Create new product  """
    data = request.get_json()

    required_fields = ['article_no', 'product_service',
                       'in_price', 'price', 'unit', 'in_stock', 'description']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor(row_factory=dict_row)

        cursor.execute("""
            INSERT INTO products (article_no, product_service, in_price, price, unit, in_stock, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING *
        """, (
            data['article_no'],
            data['product_service'],
            data['in_price'],
            data['price'],
            data['unit'],
            data['in_stock'],
            data['description']
        ))

        new_product = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify(dict(new_product)), 201

    except psycopg.IntegrityError:
        return jsonify({"error": "Article number already exists"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@pricelist_bp.route('/products/<int:product_id>', methods=['PUT'])
@token_required
def update_product(current_user, product_id):
    """Update existing  product """
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor(row_factory=dict_row)

        # Build dynamic update query
        update_fields = []
        params = []

        allowed_fields = ['article_no', 'product_service',
                          'in_price', 'price', 'unit', 'in_stock', 'description']
        for field in allowed_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                params.append(data[field])

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        params.append(product_id)

        query = f"""
            UPDATE products 
            SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
            RETURNING *
        """

        cursor.execute(query, params)
        updated_product = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()

        if not updated_product:
            return jsonify({"error": "Product not found"}), 404

        return jsonify(dict(updated_product))

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@pricelist_bp.route('/products/<int:product_id>/field', methods=['PATCH'])
@token_required
def update_product_field(current_user, product_id):
    """Update a single field of a product (for inline editing)"""
    field = request.args.get('field')
    value = request.args.get('value')

    print(f"=== UPDATE REQUEST ===")
    print(f"Product ID: {product_id}")
    print(f"Field: {field}")
    print(f"Value: {value}")
    print(f"Value type: {type(value)}")

    if not field or value is None:
        print("ERROR: Missing field or value")
        return jsonify({"error": "Field and value are required"}), 400
    #prevent injection
    allowed_fields = {
        'article_no': 'article_no',
        'product_service': 'product_service',
        'in_price': 'in_price',
        'price': 'price',
        'unit': 'unit',
        'in_stock': 'in_stock',
        'description': 'description'
    }

    if field not in allowed_fields:
        print(f"ERROR: Invalid field: {field}")
        return jsonify({"error": f"Invalid field. Allowed: {list(allowed_fields.keys())}"}), 400

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(row_factory=dict_row)

        column_name = allowed_fields[field]
        print(f"Column name: {column_name}")

        # Build query based on field type
        if field in ['in_price', 'price']:
            print("Using NUMERIC cast")
            query = f"""
                UPDATE products 
                SET {column_name} = CAST(%s AS NUMERIC), updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                RETURNING *
            """
        elif field == 'in_stock':
            print("Using INTEGER cast")
            query = f"""
                UPDATE products 
                SET {column_name} = CAST(%s AS INTEGER), updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                RETURNING *
            """
        else:
            print("Using TEXT (no cast)")
            query = f"""
                UPDATE products 
                SET {column_name} = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                RETURNING *
            """

        print(f"Query: {query}")
        print(f"Parameters: ({value}, {product_id})")

        cursor.execute(query, (value, product_id))
        updated_product = cursor.fetchone()

        print(f"Rows affected: {cursor.rowcount}")

        if not updated_product:
            print("ERROR: Product not found")
            if cursor:
                cursor.close()
            if conn:
                conn.close()
            return jsonify({"error": "Product not found"}), 404

        conn.commit()
        print(f"SUCCESS: Updated product: {updated_product}")

        cursor.close()
        conn.close()

        return jsonify(dict(updated_product)), 200

    except psycopg.Error as e:
        error_msg = f"Database error: {str(e)}"
        print(f"PSYCOPG2 ERROR: {error_msg}")
        print(f"Error code: {e.pgcode if hasattr(e, 'pgcode') else 'N/A'}")
        print(
            f"Error details: {e.pgerror if hasattr(e, 'pgerror') else 'N/A'}")

        if conn:
            conn.rollback()
        if cursor:
            cursor.close()
        if conn:
            conn.close()

        return jsonify({"error": error_msg}), 500

    except Exception as e:
        error_msg = f"Server error: {str(e)}"
        print(f"GENERAL ERROR: {error_msg}")
        import traceback
        print(traceback.format_exc())

        if conn:
            conn.rollback()
        if cursor:
            cursor.close()
        if conn:
            conn.close()

        return jsonify({"error": error_msg}), 500


@pricelist_bp.route('/products/<int:product_id>', methods=['DELETE'])
@token_required
def delete_product(current_user, product_id):
    """Delete product"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM products WHERE id = %s RETURNING id", (product_id,))
        deleted = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()

        if not deleted:
            return jsonify({"error": "Product not found"}), 404

        return jsonify({"message": "Product deleted successfully", "id": product_id})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
