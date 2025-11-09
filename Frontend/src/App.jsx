import Login from './pages/Login'
import './App.css'
import Navbar from './components/Navbar'
import LoginBox from './components/LoginBox'
import Footer from './components/Footer'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Terms from './pages/Terms.jsx'
import LanguageProvider from './components/LanguageProvider.jsx'

function App() {
  return (
    <LanguageProvider>
       <Router>
      <div>
        <div className='background'>
          <div className='bg-img'></div>
        </div>

        <Navbar />
        
        <Routes>
          <Route path="/" element={
            <>
              <LoginBox />
              <Footer />
            </>
          } />
          <Route path="/terms" element={<Terms />} />
          {/* Add more routes as needed */}
        </Routes>
      </div>
    </Router>
    </LanguageProvider>
   
  )
}

export default App;