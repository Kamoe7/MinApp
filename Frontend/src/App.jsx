import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import LoginBox from './components/LoginBox';
import ProductManagementApp from './pages/Pricelist';
import Terms from './pages/Terms';
import Navbar from './components/Navbar';
import LanguageProvider  from './components/LanguageProvider';
import './App.css';
import Footer from './components/Footer'


const ProtectedRoute = ({ children }) => {
  const token = localStorage.getItem('token');
  
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  
  return children;
};


const Layout = ({ children }) => {
  const location = useLocation();
  
 
  const routesWithoutLayout = ['/pricelist'];
  
  const showLayout = !routesWithoutLayout.includes(location.pathname);
  
  if (!showLayout) {

    return <>{children}</>;
  }

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
        
            <Route path="/login" element={<LoginBox />} />
            
            
            <Route path="/terms" element={<Terms />} />
            
      
            <Route 
              path="/pricelist" 
              element={
                <ProtectedRoute>
                  <ProductManagementApp />
                </ProtectedRoute>
              } 
            />
            
        
            <Route path="/" element={<Navigate to="/login" replace />} />
            
     
            <Route path="*" element={<Navigate to="/login" replace />} />
          </Routes>
        </Layout>
      </Router>
      
    </LanguageProvider>
  );
}

export default App;
