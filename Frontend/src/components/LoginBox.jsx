import React from 'react'
import "../css/LoginBox.css"

const LoginBox = () => {
  return (
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
  )
}

export default LoginBox