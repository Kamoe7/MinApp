import React from 'react'

const Login = () => {
  return (
    <div>
      <div className='login-container'>
        <nav className='navbar'>
          <ul className='nav-links'>
            <li>Hem</li>
          <li>Beställ</li>
          <li>Våra Kunder</li>
          <li>Om oss</li>
          <li>Kontakta oss</li>
          <li>
            Svenska <img src="https://storage.123fakturere.no/public/flags/SE.png" alt="Swedish flag" />
          </li>
          </ul>
        </nav>

        {/*login box*/}
        <div className='login-box'>
          <h1>Logga in</h1>
          <div className='input-group'>
            <label>Skriv in din epost adress</label>
            <input type='email' placeholder='Epost adress'/>
          </div>

          <div className='input-group'>
            <label>Skriv in ditt lösenord</label>
            <input type='password' placeholder='Lösenord'/>
          </div>

          <button className='login-btn'>Logga in</button>

          <div className='links'>
            <a href="#">Registrera dig</a>
            <a href="#">Glömt lösenord?</a>
          </div>

        </div>

        {/*footer*/}
        <footer>
          <p>123 Fakturera</p>
          <span>© Lättfaktura, CRO no. 638537, 2025. All rights reserved.</span>
        </footer>
      </div>
    </div>
  )
}

export default Login