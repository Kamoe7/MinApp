import React from 'react'
import "../css/footer.css"

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-div">
        <div className="footer--text-section">
          <div className="footer-brand">
            <span className="footer--lettafaktura-text">123 Fakturera</span>
          </div>
          <nav className="footer-menu">
            <a href="#">Hem</a>
            <a href="#">Beställ</a>
            <a href="#">Kontakta oss</a>
          </nav>
        </div>
        <hr className='custom-line'></hr>
        <div className="footer-copyright">
          <p className="copyright-text">
            © 2024 123 Fakturera. Alla rättigheter förbehållna.
          </p>
        </div>
      </div>
    
    </footer>

  )
}

export default Footer