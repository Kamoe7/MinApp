import React from 'react'
import '../css/Terms.css'
import { useLanguage } from '../components/LanguageProvider'
import parse from 'html-react-parser';

const Terms = () => {
    const {t} = useLanguage();
    
    const handleGoBack = () =>{
        window.history.back()
    }
  return (
    <div className='wrapper'>

         <div className='terms-content'>
        <div className='terms-section'>
             
             <div className='terms-top-text'>
                <h1 className='terms-heading head-mob-md'>{t('terms.title')}</h1>
             </div>

       
             <div style={{textAlign: 'center' , marginBlock: '2rem'}}>
                <button className='terms-button' onClick={handleGoBack}>
                   {t('terms.button')}
                </button>
             </div>

          
                <div className='terms-table'>
                    <div className='terms-condition'>
                       {parse(t('terms.content'))}
                </div>
            </div>



             <div className='terms-button-lower'>
                  <button className='terms-button' onClick={handleGoBack}>
                    {t('terms.button')}
                </button>
            </div>
        </div>
       
 
    </div>
        
    </div>
   
  )
}

export default Terms;
