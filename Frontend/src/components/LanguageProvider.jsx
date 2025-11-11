import React, { Children, createContext,useContext, useEffect, useState } from 'react'

const LanguageContext = createContext();

export const useLanguage = () =>{
    const context = useContext(LanguageContext);
    if(!context) {
        throw new Error('useLanguage must be used within LangProvider')
    }
    return context;
}

const LanguageProvider = ({children}) => {
    const [language, setlanguage]= useState(() =>{
        return localStorage.getItem('language') || 'sv';
    })
    const [translations , setTranslations ] = useState(()=>{
            //cached from localstorage
        const cached = localStorage.getItem(`translations_${language}`);
        return cached ? JSON.parse(cached) : {}
    });
    const [loading,setLoading] = useState(true);

    useEffect(() =>{
        fetchTranslations(language);
    },[language])

    const fetchCachedTranslations = async (lang) =>{

        const cached = localStorage.getItem(`translations_${lang}`);

        if (cached){

            const cachedData = JSON.parse(cached);
            setTranslations(cachedData);
            setLoading(false);

            fetchTranslations(lang);
        }else{
            setLoading(true);
            await fetchTranslations(lang);
        }
        
    }

    const fetchTranslations = async (lang) =>{
        try {
            console.log(`Fetching translations for: ${lang}`); 
            // const response = await fetch(`http://localhost:5000/api/translations/${lang}`);
              const response = await fetch(`https://minapp-backend.onrender.com/api/translations/${lang}`);
            if (!response.ok){
                throw new Error(`HTTP ERROR!! : ${response.status}`);
            }
            const data = await response.json()
            console.log('received data :',data)
            setTranslations(data);
            localStorage.setItem(`translations_${lang}`,JSON.stringify(data));
        } catch (error) {
            console.log('Error while Fetching :',error)

        } finally{
            setLoading(false);
        }
    }

    const toggleLanguage = () =>{
        const newLang = language === 'sv' ?'en' :'sv';

        const cached = localStorage.getItem(`translations_${newLang}`);
        if(cached) {
            setTranslations(JSON.parse(cached));
            setlanguage(newLang);
            localStorage.setItem('language',newLang);

            fetchTranslations(newLang);
        }else{
            setLoading(true);
            setlanguage(newLang);
            localStorage.setItem('language',newLang);
        }

        // setlanguage(newLang);
        // localStorage.setItem('language',newLang);
    }


    const t = (key) =>{
        const translation= translations[key];
        if(!translation){
            console.warn(`translation missing key:${key}`);
            return key;
        }
        return translation;
    };


  return (
    <LanguageContext.Provider value={{ language, toggleLanguage, t, loading }}>
      {loading ? (
        <div style={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          height: '100vh',
          backgroundColor: '#white',
          backgroundImage:`url('https://storage.123fakturera.se/public/wallpapers/sverige43.jpg')`,
          backgroundSize:'cover',
          color: '#fff'
        }}>
          <div style={{ textAlign: 'center' }}>
            <div style={{
              border: '4px solid #f3f3f3',
              borderTop: '4px solid #3498db',
              borderRadius: '50%',
              width: '50px',
              height: '50px',
              animation: 'spin 1s linear infinite',
              margin: '0 auto 20px'
            }}></div>
            <p>Laddar...</p>
            <style>{`
              @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
              }
            `}</style>
          </div>
        </div>
      ) : children}
    </LanguageContext.Provider>
  )
}

export default LanguageProvider;
