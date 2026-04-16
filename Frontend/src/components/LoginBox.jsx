import React from 'react'
import { useState } from 'react';
import "../css/LoginBox.css"
import VisOff from "../assets/VisOff.png"
import VisOn from "../assets/VisOn.png"
import { useLanguage } from './LanguageProvider';
import { useNavigate } from 'react-router-dom';

const LoginBox = () => {
  const [showPassword, setShowPassword] = useState(false);
  const {t} = useLanguage();
  const [email,setEmail] = useState('');
  const [password,setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading,setLoading] = useState(false);
  const navigate = useNavigate();
  const [emailTouched,setEmailTouched] =useState(false);
  const [passwordTouch,setPasswordTouch] = useState(false);

  // const passOff = '<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e3e3e3"><path d="m644-428-58-58q9-47-27-88t-93-32l-58-58q17-8 34.5-12t37.5-4q75 0 127.5 52.5T660-500q0 20-4 37.5T644-428Zm128 126-58-56q38-29 67.5-63.5T832-500q-50-101-143.5-160.5T480-720q-29 0-57 4t-55 12l-62-62q41-17 84-25.5t90-8.5q151 0 269 83.5T920-500q-23 59-60.5 109.5T772-302Zm20 246L624-222q-35 11-70.5 16.5T480-200q-151 0-269-83.5T40-500q21-53 53-98.5t73-81.5L56-792l56-56 736 736-56 56ZM222-624q-29 26-53 57t-41 67q50 101 143.5 160.5T480-280q20 0 39-2.5t39-5.5l-36-38q-11 3-21 4.5t-21 1.5q-75 0-127.5-52.5T300-500q0-11 1.5-21t4.5-21l-84-82Zm319 93Zm-151 75Z"/></svg>';
  // const passOn = '<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e3e3e3"><path d="M480-320q75 0 127.5-52.5T660-500q0-75-52.5-127.5T480-680q-75 0-127.5 52.5T300-500q0 75 52.5 127.5T480-320Zm0-72q-45 0-76.5-31.5T372-500q0-45 31.5-76.5T480-608q45 0 76.5 31.5T588-500q0 45-31.5 76.5T480-392Zm0 192q-146 0-266-81.5T40-500q54-137 174-218.5T480-800q146 0 266 81.5T920-500q-54 137-174 218.5T480-200Zm0-300Zm0 220q113 0 207.5-59.5T832-500q-50-101-144.5-160.5T480-720q-113 0-207.5 59.5T128-500q50 101 144.5 160.5T480-280Z"/></svg>'
  // const VisOn = 'C:/Users/Acer/miniApp/Frontend/src/assets/VisOn.png'
  // const VisOff = 'assets/VisOff.png'

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try{
          const response = await fetch('http://localhost:5000/api/auth/login',{
            method:'POST',
            headers:{
              'Content-Type':'application/json',

            },
            body:JSON.stringify({email,password})
                });
          
          const data = await response.json();

          if(response.ok){

            localStorage.setItem('token',data.token);
            localStorage.setItem('user',JSON.stringify(data.user));

            navigate('/pricelist');
          }else{
            setError(data.error || t('login.error'));
          }
    }catch (err){
      console.log('Login Error',err);
    }finally {
      setLoading(false);
    }

  };




  return (
    <div className="wrapper">
      

      <div className='content'>
        <div className='login-content-root'>
          <div className='back-login'>
            <h1 className='login-heading'>{t('login.title')}</h1>


            <form className='login-section' onSubmit={handleLogin}>
           

              <div className='login-email'>
                <label className='login-email-label'>{t('login.email.label')}</label>
                <input 
                  type='email' 
                  placeholder={t('login.email.placeholder')} 
                  className='login-input'
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                   onBlur={() => setEmailTouched(true)}
                  disabled={loading}
                />

              {emailTouched && !email.trim() && (
  <span className="error-messages">{t('login.error.email')}</span>
)}
                
              </div>
              <div className='login-password'>
                <label className='login-password-label'>{t('login.password.label')}</label>
                <div className='password-input-div'>
                  <input 
                    type={showPassword ? 'text' : 'password'}
                    placeholder={t('login.password.placeholder')}
                    className='login-input'
                    value={password}
                    onBlur={()=>setPasswordTouch(true)}
                    onChange={(e)=> setPassword(e.target.value)}
                    
                    disabled={loading}
                  />
                  <img
                    id="show-password-img"
                    src={showPassword 
                      ? VisOff
                      : VisOn
                    }
                    alt="toggle password visibility"
                    onClick={() => setShowPassword(!showPassword)}
                  />
                  
                </div>
                                  {passwordTouch && !password.trim() && (
                    <span
                      className='error-messages'
                    >{t('login.error.password')}</span>
                  )}
              </div>
              <div className='Login-Button-div'>
                <button className='Login-Button'>{t('login.button')}</button>
              </div>
              <div className='link'>
                <a href="#">{t('login.register')}</a>
                <a href="#">{t('login.forgot')}</a>
              </div>
            </form>
          </div>
        </div>
      </div>
      </div>
  )
}

export default LoginBox