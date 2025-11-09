import React from 'react'
import "../css/footer.css"
import { useLanguage } from './LanguageProvider'

const Footer = () => {
  const {t} = useLanguage();
  return (
    <footer className="footer">
      <div className="footer-div">
        <div className="footer--text-section">
          <div className="footer-brand">
            <span className="footer--lettafaktura-text">{t('footer.brand')}</span>
          </div>
          <nav className="footer-menu">
            <a href="#">{t('nav.home')}</a>
            <a href="#">{t('nav.order')}</a>
            <a href="#">{t('nav.contact')}</a>
          </nav>
        </div>
        <hr className='custom-line'></hr>
        <div className="footer-copyright">
          <p className="copyright-text">
            {t('footer.copyright')}
          </p>
        </div>
      </div>
    
    </footer>

  )
}

export default Footer