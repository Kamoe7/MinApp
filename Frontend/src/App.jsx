import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import LoginBox from './components/LoginBox';
import ProductManagementApp from './pages/Pricelist';
import Terms from './pages/Terms';
import Navbar from './components/Navbar';
import LanguageProvider  from './components/LanguageProvider';
import './App.css';
import Footer from './components/Footer'

// Protected Route Component
const ProtectedRoute = ({ children }) => {
  const token = localStorage.getItem('token');
  
  if (!token) {
    // If not logged in, redirect to login page
    return <Navigate to="/login" replace />;
  }
  
  return children;
};

// Layout wrapper component to conditionally show navbar and background
const Layout = ({ children }) => {
  const location = useLocation();
  
  // Routes that should NOT have navbar and background
  const routesWithoutLayout = ['/pricelist'];
  
  const showLayout = !routesWithoutLayout.includes(location.pathname);
  
  if (!showLayout) {
    // For pricelist and other admin pages, render without layout
    return <>{children}</>;
  }
  
  // For public pages (login, terms, etc.), render with layout
  return (
    <>
      <div className='background'>
        <div className='bg-img'></div>
      </div>
      <Navbar />
      <Footer/>
      {children}
    </>
  );
};

function App() {
  return (
    <LanguageProvider>
      <Router>
        <Layout>
          <Routes>
            {/* Login Route */}
            <Route path="/login" element={<LoginBox />} />
            
            {/* Terms Route */}
            <Route path="/terms" element={<Terms />} />
            
            {/* Protected Pricelist Route (no navbar/background) */}
            <Route 
              path="/pricelist" 
              element={
                <ProtectedRoute>
                  <ProductManagementApp />
                </ProtectedRoute>
              } 
            />
            
            {/* Default route - redirect to login */}
            <Route path="/" element={<Navigate to="/login" replace />} />
            
            {/* Catch all - redirect to login */}
            <Route path="*" element={<Navigate to="/login" replace />} />
          </Routes>
        </Layout>
      </Router>
      
    </LanguageProvider>
  );
}

export default App;