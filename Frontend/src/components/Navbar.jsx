

import { useState } from 'react';
import '../css/NavBar.css';


export default function NavBar() {
  const [lang, setLang] = useState('sv');
  const [showDropdown, setShowDropDown] = useState(false);
  const [showMobileMenu,setShowMobileMenu] = useState(false)
  
  const flag = lang === 'sv'
    ? 'https://storage.123fakturere.no/public/flags/SE.png'
    : 'https://storage.123fakturere.no/public/flags/GB.png';

  const langText = lang === 'sv' ? 'Svenska' : 'English';

  return (
    <nav className="navbar">
      <header className='nav-header'>
        <div className='nav-section'>
            <div 
              className='hamburger-btn'
              onClick={()=>setShowMobileMenu(!showMobileMenu)}>
                <svg xmlns="http://www.w3.org/2000/svg" height="36px" viewBox="0 -960 960 960" width="40px" fill="#e3e3e3"><path d="M120-240v-80h720v80H120Zm0-200v-80h720v80H120Zm0-200v-80h720v80H120Z"/></svg>
          
              </div>


                <a href="#" className="logo-link">
            <img
              src="https://storage.123fakturera.se/public/icons/diamond.png"
              alt="123 Fakturera"
              className="logo"
            />
          </a>


            <ul className="menu-bar">
              <div className='menu-list'>
                <a href="#" className='menu-list'>Hem</a>
                <a href="#" className='menu-list'>Beställ</a>
                <a href="#" className='menu-list'>Våra kunder</a>
                <a href="#" className='menu-list'>Om oss</a>
                <a href="#" className='menu-list'>Kontakta oss</a>
              </div>

              <div className='lang-switch-wrapper '>
                <div className="lang-switch" onClick={()=> setShowDropDown(v=>!v)}>
                <span className="lang-text ">{langText}</span>
                  
                    <img
                      src={flag}
                      alt={langText}
                      className="flag"
                      // onClick={() => setLang(prev => prev === 'sv' ? 'en' : 'sv')}
                  />

                  {showDropdown && (

                     <div className='dropdown-menu'>
                    <div className='dropdown-item'
                      onClick={(e) =>{
                        e.stopPropagation();
                        setLang('sv');
                        setShowDropDown(false);
                      }}
                    >
                      <span className='dropdown-lang-name'>Svenska</span>
                     
                        <img 
                          src='https://storage.123fakturere.no/public/flags/SE.png'
                          alt='SE'
                          className='dropdown-flag'
                          />
                    

                      </div>

                      <div className='dropdown-item'
                        onClick={(e)=>{
                          e.stopPropagation();
                          setLang('en');
                          setShowDropDown(false);
                        }}>
                          <span className='dropdown-lang-name'>English</span>
                          
                            <img 
                              src="https://storage.123fakturere.no/public/flags/GB.png"
                              alt="GB"
                              className="dropdown-flag"

                              />
                     
                      </div>

                  </div>

                  )}
                 

              </div>

              

              </div>
          </ul>

            {/* Mobile/Tablet Language Switcher */}
            <div className="lang-switch-wrapper mobile-lang">
              <div className="lang-switch" onClick={() => setShowDropDown(v => !v)}>
                <span className="lang-text mobile-lang-text">{langText}</span>
                <img
                  src={flag}
                  alt={langText}
                  className="flag"
                />
              </div>

              {showDropdown && (
                <div className="dropdown-menu">
                  <div 
                    className='dropdown-item'
                    onClick={(e) => {
                      e.stopPropagation();
                      setLang('sv');
                      setShowDropDown(false);
                    }}
                  >
                    <span className='dropdown-lang-name'>Svenska</span>
                    <img 
                      src='https://storage.123fakturere.no/public/flags/SE.png'
                      alt='SE'
                      className='dropdown-flag'
                    />
                  </div>

                  <div 
                    className='dropdown-item'
                    onClick={(e) => {
                      e.stopPropagation();
                      setLang('en');
                      setShowDropDown(false);
                    }}
                  >
                    <span className='dropdown-lang-name'>English</span>
                    <img 
                      src="https://storage.123fakturere.no/public/flags/GB.png"
                      alt="GB"
                      className="dropdown-flag"
                    />
                  </div>
                </div>
              )}
            </div>
          </div>
          {/*for mobile humberger */}
              {showMobileMenu && (
                <div className='mobile-menu-dropdown'>
                  <a href='#' onClick={() => setShowMobileMenu(false)}>Hem</a>
                  <a href="#" onClick={() => setShowMobileMenu(false)}>Beställ</a>
                  <a href="#" onClick={() => setShowMobileMenu(false)}>Våra kunder</a>
                  <a href="#" onClick={() => setShowMobileMenu(false)}>Om oss</a>
                  <a href="#" onClick={() => setShowMobileMenu(false)}>Kontakta oss</a>
                      
                </div>
              )}
      
   

      </header>

      
    </nav>
  );
}
