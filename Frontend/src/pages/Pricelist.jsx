import React, { useState, useEffect } from 'react';
import { Menu, Search, Plus, Printer, Settings, ChevronDown, MoreVertical, Edit2, Save } from 'lucide-react';
import '../css/pricelist.css'
import { useNavigate } from 'react-router-dom';
const API_URL = 'https://minapp-backend.onrender.com/api/pricelist';


const getAuthToken = () => {
  return localStorage.getItem('token') || '';
};


const fetchWithAuth = async (url, options = {}) => {
  const token = getAuthToken();
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };
  
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  
  const response = await fetch(url, {
    ...options,
    headers,
  });
  
  if (response.status === 401) {
    console.error('Authentication failed');
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/login';
    throw new Error('Authentication required');
  }
  
  return response;
};

export default function ProductManagementApp() {
  const navigate = useNavigate();
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editingCell, setEditingCell] = useState(null);
  const [menuOpen, setMenuOpen] = useState(false);
  const [searchArticle, setSearchArticle] = useState('');
  const [searchProduct, setSearchProduct] = useState('');

  // Fetch products from API
  const fetchProducts = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const params = new URLSearchParams();
      if (searchArticle) params.append('search_article', searchArticle);
      if (searchProduct) params.append('search_product', searchProduct);
      
      const response = await fetchWithAuth(
        `${API_URL}/products?${params.toString()}`
      );
      
      if (!response.ok) {
        throw new Error('Failed to fetch products');
      }
      
      const data = await response.json();
      const transformedData = data.map(p => ({
        id: p.id,
        articleNo: p.article_no,
        productService: p.product_service,
        inPrice: parseFloat(p.in_price),
        price: parseFloat(p.price),
        unit: p.unit,
        inStock: p.in_stock,
        description: p.description,
      }));
      
      setProducts(transformedData);
    } catch (err) {
      console.error('Error fetching products:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProducts();
  }, []);


  useEffect(() => {
    const timer = setTimeout(() => {
      if (searchArticle || searchProduct) {
        fetchProducts();
      }
    }, 500);
    
    return () => clearTimeout(timer);
  }, [searchArticle, searchProduct]);

  const handleCellEdit = (id, field, value) => {
    setProducts(products.map(p => 
      p.id === id ? { ...p, [field]: value } : p
    ));
  };

  const handleCellBlur = async (id, field, value) => {
    setEditingCell(null);
    

    const fieldMap = {
      articleNo: 'article_no',
      productService: 'product_service',
      inPrice: 'in_price',
      inStock: 'in_stock',
    };
    
    const backendField = fieldMap[field] || field;
    
    try {
      const response = await fetchWithAuth(
        `${API_URL}/products/${id}/field?field=${backendField}&value=${encodeURIComponent(value)}`,
        {
          method: 'PATCH',
        }
      );
      
      if (!response.ok) {
        throw new Error('Failed to update product');
      }
      
      const updatedProduct = await response.json();
      console.log('Product updated successfully:', updatedProduct);
      
   
    } catch (err) {
      console.error('Error updating product:', err);
      setError('Failed to save changes');
  
      fetchProducts();
    }
  };

  const handleLogout = () =>{
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/login');
  };

  const filteredProducts = products;

  return (
    <div className="app">
         <header className="header">
        <div className="header-left">
          <button className="menu-btn" onClick={() => setMenuOpen(!menuOpen)}>
            <Menu size={24} />
          </button>
          <div className="user-info">
            <div className="avatar">
                JA
                </div>
            <div className="user-details">
              <h3>John Susleen</h3>
              <p>CQUPTS</p>
            </div>
          </div>
        </div>
        <div className="header-right">
          <div className="lang-selector">
            <span>English</span>
            <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 60 30'%3E%3Crect width='60' height='30' fill='%23012169'/%3E%3Cpath d='M0 0L60 30M60 0L0 30' stroke='%23fff' stroke-width='6'/%3E%3Cpath d='M0 0L60 30M60 0L0 30' stroke='%23C8102E' stroke-width='4' stroke-linecap='round'/%3E%3Cpath d='M30 0v30M0 15h60' stroke='%23fff' stroke-width='10'/%3E%3Cpath d='M30 0v30M0 15h60' stroke='%23C8102E' stroke-width='6'/%3E%3C/svg%3E" alt="UK Flag" className="flag" />
          </div>
        </div>
      </header>

      <aside className={`sidebar ${menuOpen ? 'mobile-open' : 'mobile-hidden'}`}>
        <h3>Menu</h3>
        <div className="menu-item">
          <div style={{width: 20, height: 20, background: '#90caf9', borderRadius: 4}}></div>
          <span>Invoices</span>
        </div>
        <div className="menu-item">
          <div style={{width: 20, height: 20, background: '#81c784', borderRadius: 4}}></div>
          <span>Customers</span>
        </div>
        <div className="menu-item">
          <Settings size={20} />
          <span>My Business</span>
        </div>
        <div className="menu-item">
          <div style={{width: 20, height: 20, background: '#64b5f6', borderRadius: 4}}></div>
          <span>Invoice Journal</span>
        </div>
        <div className="menu-item active">
          <div style={{width: 20, height: 20, background: '#ffb74d', borderRadius: 4}}></div>
          <span>Price List</span>
        </div>
        <div className="menu-item">
          <div style={{width: 20, height: 20, background: '#4dd0e1', borderRadius: 4}}></div>
          <span>Multiple Invoicing</span>
        </div>
        <div className="menu-item">
          <div style={{width: 20, height: 20, background: '#f06292', borderRadius: 4}}></div>
          <span>Unpaid Invoices</span>
        </div>
        <div className="menu-item">
          <div style={{width: 20, height: 20, background: '#fff176', borderRadius: 4}}></div>
          <span>Offer</span>
        </div>
        <div className="menu-item">
          <div style={{width: 20, height: 20, background: '#4db6ac', borderRadius: 4}}></div>
          <span>Inventory Control</span>
        </div>
        <div className="menu-item">
          <div style={{width: 20, height: 20, background: '#7986cb', borderRadius: 4}}></div>
          <span>Member Invoicing</span>
        </div>
        <div className="menu-item">
          <div style={{width: 20, height: 20, background: '#9575cd', borderRadius: 4}}></div>
          <span>Import/Export</span>
        </div>
        <div className="menu-item">
          <div style={{width: 20, height: 20, background: '#e0e0e0', borderRadius: 4}}></div>
          <span>Log out</span>
        </div>
      </aside>

      <main className={`main-content ${menuOpen ? '' : 'full-width'}`}>
        <div className="toolbar">
          <div className="search-row">
            <div className="search-box">
              <input
                type="text"
                placeholder="Search Article No..."
                value={searchArticle}
                onChange={(e) => setSearchArticle(e.target.value)}
              />
              <Search size={20}  />
            </div>
            <div className="search-box">
              <input
                type="text"
                placeholder="Search Product..."
                value={searchProduct}
                onChange={(e) => setSearchProduct(e.target.value)}
              />
              <Search size={20}/>
            </div>
          </div>
          <div className="action-buttons">
            <button className="btn btn-primary">
              <Plus size={18} />
              New Product
            </button>
            <button className="btn btn-secondary">
              <Printer size={18} />
              Print List
            </button>
            <button className="btn btn-tertiary">
              <Settings size={18} />
              Advanced mode
            </button>
          </div>
        </div>

        <div className="table-container">
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th className="row-indicator"></th>
                  <th>Article No. <ChevronDown size={16}/></th>
                  <th>Product/Service <ChevronDown size={16}/></th>
                  <th>In Price</th>
                  <th>Price</th>
                  <th>Unit</th>
                  <th>In Stock</th>
                  <th>Description</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {loading ? (
                  <tr>
                    <td colSpan="9" style={{textAlign: 'center', padding: '40px'}}>
                      Loading...
                    </td>
                  </tr>
                ) : filteredProducts.length === 0 ? (
                  <tr>
                    <td colSpan="9" style={{textAlign: 'center', padding: '40px'}}>
                      No products found
                    </td>
                  </tr>
                ) : (
                  filteredProducts.map((product) => (
                    <tr key={product.id}>
                      <td className="row-indicator">→</td>
                      <td className="editable-cell">
                        {editingCell === `${product.id}-articleNo` ? (
                          <input
                            autoFocus
                            value={product.articleNo}
                            onChange={(e) => handleCellEdit(product.id, 'articleNo', e.target.value)}
                            onBlur={(e) => handleCellBlur(product.id, 'articleNo', e.target.value)}
                            onKeyDown={(e) => e.key === 'Enter' && e.target.blur()}
                          />
                        ) : (
                          <div
                            className="cell-content"
                            onClick={() => setEditingCell(`${product.id}-articleNo`)}
                          >
                            {product.articleNo}
                          </div>
                        )}
                      </td>
                      <td className="editable-cell">
                        {editingCell === `${product.id}-productService` ? (
                          <input
                            autoFocus
                            value={product.productService}
                            onChange={(e) => handleCellEdit(product.id, 'productService', e.target.value)}
                            onBlur={(e) => handleCellBlur(product.id, 'productService', e.target.value)}
                            onKeyDown={(e) => e.key === 'Enter' && e.target.blur()}
                          />
                        ) : (
                          <div
                            className="cell-content"
                            onClick={() => setEditingCell(`${product.id}-productService`)}
                          >
                            {product.productService}
                          </div>
                        )}
                      </td>
                      <td className="editable-cell">
                        {editingCell === `${product.id}-inPrice` ? (
                          <input
                            autoFocus
                            type="number"
                            value={product.inPrice}
                            onChange={(e) => handleCellEdit(product.id, 'inPrice', e.target.value)}
                            onBlur={(e) => handleCellBlur(product.id, 'inPrice', e.target.value)}
                            onKeyDown={(e) => e.key === 'Enter' && e.target.blur()}
                          />
                        ) : (
                          <div
                            className="cell-content"
                            onClick={() => setEditingCell(`${product.id}-inPrice`)}
                          >
                            {product.inPrice}
                          </div>
                        )}
                      </td>
                      <td className="editable-cell">
                        {editingCell === `${product.id}-price` ? (
                          <input
                            autoFocus
                            type="number"
                            value={product.price}
                            onChange={(e) => handleCellEdit(product.id, 'price', e.target.value)}
                            onBlur={(e) => handleCellBlur(product.id, 'price', e.target.value)}
                            onKeyDown={(e) => e.key === 'Enter' && e.target.blur()}
                          />
                        ) : (
                          <div
                            className="cell-content"
                            onClick={() => setEditingCell(`${product.id}-price`)}
                          >
                            {product.price}
                          </div>
                        )}
                      </td>
                      <td className="editable-cell">
                        {editingCell === `${product.id}-unit` ? (
                          <input
                            autoFocus
                            value={product.unit}
                            onChange={(e) => handleCellEdit(product.id, 'unit', e.target.value)}
                            onBlur={(e) => handleCellBlur(product.id, 'unit', e.target.value)}
                            onKeyDown={(e) => e.key === 'Enter' && e.target.blur()}
                          />
                        ) : (
                          <div
                            className="cell-content"
                            onClick={() => setEditingCell(`${product.id}-unit`)}
                          >
                            {product.unit}
                          </div>
                        )}
                      </td>
                      <td className="editable-cell">
                        {editingCell === `${product.id}-inStock` ? (
                          <input
                            autoFocus
                            type="number"
                            value={product.inStock}
                            onChange={(e) => handleCellEdit(product.id, 'inStock', e.target.value)}
                            onBlur={(e) => handleCellBlur(product.id, 'inStock', e.target.value)}
                            onKeyDown={(e) => e.key === 'Enter' && e.target.blur()}
                          />
                        ) : (
                          <div
                            className="cell-content"
                            onClick={() => setEditingCell(`${product.id}-inStock`)}
                          >
                            {product.inStock}
                          </div>
                        )}
                      </td>
                      <td className="editable-cell">
                        {editingCell === `${product.id}-description` ? (
                          <input
                            autoFocus
                            value={product.description}
                            onChange={(e) => handleCellEdit(product.id, 'description', e.target.value)}
                            onBlur={(e) => handleCellBlur(product.id, 'description', e.target.value)}
                            onKeyDown={(e) => e.key === 'Enter' && e.target.blur()}
                          />
                        ) : (
                          <div
                            className="cell-content"
                            onClick={() => setEditingCell(`${product.id}-description`)}
                          >
                            {product.description}
                          </div>
                        )}
                      </td>
                      <td>
                        <button className="more-btn">
                          <MoreVertical size={18} />
                        </button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>
  );
}