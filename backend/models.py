from utils.database import get_connection
from werkzeug.security import generate_password_hash


def init_db():
    conn = None
    cur = None

    try:
        print("=" * 60)
        print("STARTING DATABASE INITIALIZATION")
        print("=" * 60)

        conn = get_connection()
        cur = conn.cursor()

        # Create translations table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS translations (
                id SERIAL PRIMARY KEY,
                key VARCHAR(255) UNIQUE NOT NULL,
                sv TEXT NOT NULL,
                en TEXT NOT NULL,
                page VARCHAR(100) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP                    
            )
        ''')
        print("✅ Translations table created")

        # Create users table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✅ Users table created")

        # Create products table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                article_no VARCHAR(50) UNIQUE NOT NULL,
                product_service VARCHAR(255) NOT NULL,
                in_price DECIMAL(10, 2) NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                unit VARCHAR(50) NOT NULL,
                in_stock INTEGER NOT NULL DEFAULT 0,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✅ Products table created")

        # Create indexes
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_article_no ON products(article_no);
            CREATE INDEX IF NOT EXISTS idx_product_service ON products(product_service);
        """)
        print("✅ Indexes created")

        # Insert default user
        hashed_password = generate_password_hash(
            'admin777', method='pbkdf2:sha256')
        cur.execute('''
            INSERT INTO users (email, password_hash)
            VALUES (%s, %s)
            ON CONFLICT (email) DO NOTHING
        ''', ('admin@example.com', hashed_password))
        print("✅ User created/exists")

        # Insert products
        cur.execute('SELECT COUNT(*) FROM products')
        result = cur.fetchone()
        product_count = result['count']

        if product_count == 0:
            print(f"Inserting products...")
            sample_products = [
                ('1234567890', 'This is a test product', 900500,
                 1500800, 'kilometers/hour', 2500600, 'Description'),
                ('1234567891', 'Sony DSLR Camera Professional',
                 12000, 15000, 'pieces', 45, 'High-end camera'),
                ('1234567892', 'Random product', 800,
                 1234, 'units', 150, 'Various items'),
                ('1234567893', 'Laptop Computer Core i7',
                 45000, 65000, 'pieces', 25, 'Business laptop'),
                ('1234567894', 'Office Chair Ergonomic', 15000,
                 22000, 'pieces', 80, 'Comfortable chair'),
                ('1234567895', 'Wireless Mouse Bluetooth',
                 800, 1200, 'pieces', 200, 'Premium mouse'),
                ('1234567896', 'Mechanical Keyboard RGB',
                 5000, 7500, 'pieces', 120, 'Gaming keyboard'),
                ('1234567897', 'Monitor 27 inch 4K', 25000,
                 35000, 'pieces', 60, 'Ultra HD display'),
                ('1234567898', 'USB-C Hub Multiport', 2500,
                 3800, 'pieces', 180, 'Multiple ports'),
                ('1234567899', 'External SSD 1TB', 8000,
                 11000, 'pieces', 95, 'Fast storage'),
                ('1234567900', 'Webcam HD 1080p', 3500,
                 5200, 'pieces', 140, 'HD video'),
                ('1234567901', 'Headphones Noise Canceling',
                 18000, 25000, 'pieces', 70, 'Premium audio'),
                ('1234567902', 'Desk Lamp LED Adjustable',
                 2000, 3200, 'pieces', 160, 'Energy efficient'),
                ('1234567903', 'Cable Management Kit',
                 500, 850, 'sets', 300, 'Organize cables'),
                ('1234567904', 'Standing Desk Converter',
                 12000, 17500, 'pieces', 40, 'Adjustable desk'),
                ('1234567905', 'Printer Laser All-in-One',
                 22000, 32000, 'pieces', 35, 'Print scan copy'),
                ('1234567906', 'Router WiFi 6 Mesh', 15000,
                 21000, 'pieces', 55, 'Wireless coverage'),
                ('1234567907', 'Power Strip Surge Protected',
                 1200, 1800, 'pieces', 220, 'Multiple outlets'),
                ('1234567908', 'Graphics Tablet Digital',
                 8500, 12500, 'pieces', 48, 'Drawing tablet'),
                ('1234567909', 'Smart Speaker Voice Assistant',
                 6000, 8500, 'pieces', 110, 'Smart home hub'),
            ]

            for article_no, product_service, in_price, price, unit, in_stock, description in sample_products:
                cur.execute("""
                    INSERT INTO products (article_no, product_service, in_price, price, unit, in_stock, description)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (article_no, product_service, in_price, price, unit, in_stock, description))

            print(f"✅ {len(sample_products)} products inserted")
        else:
            print(f"✅ Products already exist ({product_count})")

        # Insert translations
        translations_data = [
            # Navbar
            ('nav.home', 'Hem', 'Home', 'navbar'),
            ('nav.order', 'Beställ', 'Order', 'navbar'),
            ('nav.customers', 'Våra kunder', 'Our Customers', 'navbar'),
            ('nav.about', 'Om oss', 'About Us', 'navbar'),
            ('nav.contact', 'Kontakta oss', 'Contact us', 'navbar'),
            ('nav.language', 'SV', 'EN', 'navbar'),

            # Login
            ('login.title', 'Logga in', 'Log in', 'login'),
            ('login.email.label', 'Skriv in din epost adress',
             'Enter your email address', 'login'),
            ('login.email.placeholder', 'Epost adress', 'Email address', 'login'),
            ('login.password.label', 'Skriv in ditt lösenord',
             'Enter your password', 'login'),
            ('login.password.placeholder', 'Lösenord', 'Password', 'login'),
            ('login.button', 'Logga in', 'Log in', 'login'),
            ('login.register', 'Registrera dig', 'Register', 'login'),
            ('login.forgot', 'Glömt lösenord?', 'Forgot password?', 'login'),
            ('login.error', 'Fel e-postadress eller lösenord',
             'Incorrect email or password', 'login'),
            ('login.error.email', 'Vänligen skriv in en giltig epost adress',
             'Please enter a valid email address','login'),
            ('login.error.password', 'Detta fält kan inte vara tomt',
             'This field cannot be empty','login'),

            # Terms
            ('terms.title', 'Villkor', 'Terms', 'terms'),
            ('terms.button', 'stäng och gå tillbaka', 'Close and Go Back', 'terms'),
            ('terms.content',  '''<p><b>GENOM</b> att klicka på Fakturera Nu väljer du att registrera dig enligt den information som du har skrivit in och texten på registreringssidan och villkoren här, och du accepterar samtidigt villkoren här.</p>

<p>Du kan använda programmet GRATIS i 14 dagar.</p>

<p>123 Fakturera är så lätt och självförklarande att chansen att du behöver support är minimal, men om du skulle behöva support finns vi här för dig, med vårt kontor bemannat större delen av dagen. Efter provperioden fortsätter prenumerationen och kostar 99 kr exkl. moms per månad, vilket faktureras årligen. Om du inte vill behålla programmet säger du bara upp provperioden genom att meddela oss före 14 dagar från registreringen.</p>

<p>Du har förstås rätt att avsluta användningen av programmet utan några kostnader, genom att meddela oss per e-post före 14 dagar från registreringen att du inte vill fortsätta med programmet, och du betalar då förstås ingenting.</p>

<p>Om vi inte får ett sådant meddelande från dig före 14 dagar från registreringen kan beställningen av naturliga skäl inte ändras. Med registrering avses datum och tid när du valde att trycka på knappen Fakturera Nu.</p>

<p>Fakturering sker för ett år i taget.</p>

<p>Priset för 123 Fakturera (erbjudandepris 99 kr per månad / ordinarie pris 159 kr per månad) är för årsavgiften Start för ett års användning av programmet.</p>

<p>(Vid användning av erbjudandepriset 99 kr räknas ettårsperioden från registreringen.)</p>

<p>Alla priser är exkl. moms.</p>

<p>Erbjudande, Lagerkontroll, Medlemsfakturering, Multiuserversion och Engelsk utskrift är (eller kan vara) tilläggsmoduler som kan beställas senare.</p>

<p>Förmedling, liksom fakturering, kan ske från K-Soft Sverige AB, Box 2826, 187 28 Täby. I framtiden kan vi välja att samarbeta med ett annat företag för t.ex. förmedling och fakturering. Kundrelationen är dock hos oss. Betalningen görs till det företag som fakturan kommer från.</p>

<p>Årsavgiften löper kontinuerligt, men om du inte vill fortsätta använda programmet behöver du bara säga upp trettio dagar före nästa ettårsperiods början.</p>

<p>Introduktionserbjudandet (99 kr per månad) gäller årsavgiften Start för det första året. Efter det första året faktureras ordinarie pris, vilket för närvarande, för årsavgift Start är etthundrafemtionio kronor per månad, för årsavgift Fjärrkontroll trehundra kronor per månad och för årsavgift Pro trehundratrettiotre kronor per månad. Efter ett år faktureras årsavgiften Fjärrkontroll som standard, men du kan välja Start eller Pro genom att meddela när som helst före förfallodagen.</p>

<p>Om du väljer att behålla programmet genom att inte meddela oss per e-post inom 14 dagar från registreringen att du inte vill fortsätta med programmet, accepterar du att du kommer att betala fakturan för din beställning. Utebliven betalning av fakturan eller sen betalning ger inte rätt att avbeställa ordern. Vi hjälper gärna till med logotyp till ett självkostnadspris.</p>

<p>Licens för användning av 123 Fakturera säljs förstås i enlighet med gällande lagar.</p>

<p>För att kunna hjälpa dig enklare och ge dig support, samt för att följa lagarna, måste vi av naturliga skäl lagra din information.</p>

<p>I samband med lagring av information kräver lagen att vi ger dig följande information:</p>

<p>Om du beställer som privatperson har du rätt att ångra dig enligt lag. Din information lagras så att vi kan hjälpa dig osv. Vi kommer att använda den för att kunna hjälpa dig om du behöver hjälp, följa lagarna om bokföring osv. När det finns uppgraderingar och liknande kan vi skicka dig erbjudanden och liknande om våra produkter och tjänster via e-post eller liknande. Du kan kontaktas via e-post, post och telefon. Om du inte vill bli kontaktad skickar du bara ett e-postmeddelande till oss om det.</p>

<p>Du kan när som helst be att inte få information om uppgraderingar via e-post, brev eller liknande, och det kommer vi förstås inte att göra. Du skickar en sådan begäran till oss via e-post, post eller liknande.</p>

<p>Av naturliga skäl måste vi lagra, bearbeta och flytta dina uppgifter. Din information lagras tills vidare. Du ger oss tillåtelse att lagra, bearbeta och flytta dina uppgifter, samt att skicka erbjudanden och liknande via e-post, brev och liknande, och berätta för andra att du är kund. På grund av hur det fungerar med programvara behöver tillstånd också ges till andra parter. Tillståndet ges därför till oss, samt till de företag och/eller person(er) som äger programvaran, källkoden, webbplatsen och liknande. Det ges också till nuvarande och framtida företag som ägs och/eller kontrolleras av en eller flera av dem som för närvarande äger och/eller kontrollerar oss. Det ges också till nuvarande och framtida företag som ägs och/eller kontrolleras av en eller flera av dem som för närvarande äger och/eller kontrollerar företagen (om sådana finns) som äger eller kommer att äga programvaran, källkoden, webbplatsen och liknande. Det ges också till nuvarande och framtida personer (om sådana finns) som äger eller kommer att äga programvaran, källkoden, webbplatsen och liknande. Detta gäller både nuvarande och framtida produkter och tjänster. Det ges också till ett annat företag (som K-Soft Sverige AB), som vi kan använda för att skicka/sälja produkter, uppgraderingar och liknande, antingen genom förmedling eller på annat sätt.</p>

<p>Du har förstås rätt att begära tillgång till, ändring och radering av den information vi har om dig. Du har också rätt att begära begränsning av databehandling och att invända mot databehandling och rätten till dataportabilitet. Du har rätt att klaga till tillsynsmyndigheten. Du kan hitta mer juridisk information om oss här. Irlands lagar är tillämpliga lagar. Att lägga en beställning är förstås helt frivilligt. Vi använder förstås ingen automatiserad profilering eller beslut.</p>

<p>Om du vill kontakta oss, använd informationen på denna webbplats.</p>

<p>Klicka på Fakturera Nu för att registrera dig enligt den information du har angett och villkoren här. (Datum och tid för antagande registreras automatiskt i våra register.)</p>

<p>Vår erfarenhet är att våra kunder är mycket nöjda med hur vi arbetar och hoppas och tror att detta också blir din upplevelse.</p>

<p>Ha en bra dag!</p>''',
             '''<p><b>BY</b> clicking Invoice Now, you choose to register according to the information that you have typed in and the text on the registration page and the terms here, and you at the same time accept the terms here.</p>

<p>You can use the program FOR FREE for 14 days.</p>

<p>123 Fakturera is so easy and self-explanatory that the chance that you will need support is minimal, but if you should need support, we are here for you, with our office manned for the most part of the day. After the trial period, the subscription continues and costs SEK 99 excluding VAT per month, which is billed annually. If you do not want to keep the program, just cancel the trial period by giving notice before 14 days from registration.</p>

<p>You have of course the right to terminate the use of the program without any costs, by giving us notice per email before 14 days from registration, that you do not want to continue with the program, and you then of course do not pay anything.</p>

<p>If we do not receive such a notice from you before 14 days from registration, then the order, for natural reasons, cannot be changed. With registration it is meant the date and time when you did choose to press the button Invoice Now.</p>

<p>Billing is for one year at a time.</p>

<p>The price for 123 Fakturera (offer price SEK 99 per month / ordinary price SEK 159 per month) is for the annual fee Start for one year's use of the program.</p>

<p>(When using the offer price of SEK 99, the one-year period is calculated from registration.)</p>

<p>All prices are excluding VAT.</p>

<p>Offer, Inventory Control, Member Invoicing, Multiuser version and English printout are (or can be) additional modules that can be ordered later.</p>

<p>Intermediation, as well as invoicing, may take place from K-Soft Sverige AB, Box 2826, 187 28 Täby. In the future, we may choose to cooperate with another company for e.g. intermediation and invoicing. However, the customer relationship is with us. The payment is made to the company from which the invoice comes.</p>

<p>The annual fee is on a continuous basis, but if you do not wish to continue using the program, all you have to do is give notice thirty days before the start of the next one-year period.</p>

<p>The introductory offer (SEK 99 per month) is for the annual fee Start for the first year. After the first year, the ordinary price is billed, which is currently, for annual fee Start, one hundred and fifty-nine kroner per month, for annual fee Remote control, three hundred kroner per month and for annual fee Pro, three hundred and thirty-three kroner per month. After one year, the annual Remote Control fee is invoiced as standard, but you can choose Start or Pro by giving notice at any time before the due date.</p>

<p>If you choose to keep the program by not notifying us by email within 14 days of registration that you do not wish to continue with the program, you accept that you will pay the invoice for your order. Failure to pay the invoice or late payment does not give the right to cancel the order. We are happy to help you with logo at a cost price.</p>

<p>License for the use of 123 Fakturera is of course sold in accordance with applicable laws.</p>

<p>In order to be able to help you more easily and provide you with support, as well as to comply with the laws, we, for natural reasons, have to store your information.</p>

<p>In connection with the storage of information, the law requires that we provide you with the following information:</p>

<p>If you order as a private person, you have the right to cancel as stated by law. Your information is stored so that we can help you, etc. We will use it to be able to help you if you need help, follow the laws regarding bookkeeping, etc. When there are upgrades and the like, we may send you offers and the like about our products and services by email or the like. You may be contacted by email, post and telephone. If you don't want to be contacted, just send us an email about it.</p>

<p>You can at any time ask not to be sent information about upgrades by email, letter or the like, and we will of course not do that. You send such a request to us by email, post or similar.</p>

<p>For natural reasons, we have to store, process and move your data. Your information is stored until further notice. You give us permission to store, process and move your data, as well as to send you offers and the like by email, letter and the like, and tell others that you are customer. Due to the way it works with software, permission also needs to be given to other parties. The permission is therefore granted to us, as well as to the companies and/or person(s) who own the software, the source code, the website and the like. It is also given to current and future companies owned and/or controlled by one or more of those who currently own and/or control us. It is also given to current and future companies owned and/or controlled by one or more of those who currently own and/or control the companies (if any), which own or will own the software, source code, website and the like. It is also given to current and future persons (if any) who own or will own the software, source code, website and the like. This applies both to current and future products and services. It is also given to another company, (like K-Soft Sverige AB), which we can use to send/sell products, upgrades and the like, either by intermediation or otherwise.</p>

<p>You of course have the right to request access to, change and deletion of the information we hold about you. You also have the right to request restriction of data processing, and to object to data processing and the right to data portability. You have the right to complain to the supervisory authority. You can find more legal information about us here. The laws of Ireland are the applicable laws. Placing an order is of course completely voluntary. Of course, we do not use any automated profiling or decisions.</p>

<p>If you wish to contact us, please use the information on this website.</p>

<p>Click on Invoice Now to register according to the information you have entered and the terms here. (Date and time of admission are entered automatically in our registers.)</p>

<p>Our experience is that our customers are very satisfied with the way we work and hope and believe that this will also be your experience.</p>

<p>Have a great day!</p>''', 'terms'),

            # footer 
            ('footer.brand', '123 Fakturera', '123 Fakturera', 'footer'),
            ('footer.copyright', '© 2024 123 Fakturera. Alla rättigheter förbehållna.',
             '© 2024 123 Fakturera. All rights reserved.', 'footer'),

        ]

        for key, sv, en, page in translations_data:
            cur.execute('''
                INSERT INTO translations (key, sv, en, page)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (key) DO UPDATE
                SET sv = EXCLUDED.sv, en = EXCLUDED.en
            ''', (key, sv, en, page))

        print("✅ Translations inserted")

        conn.commit()
        print("=" * 60)
        print("DATABASE INITIALIZED SUCCESSFULLY!")
        print("=" * 60)

    except Exception as e:
        print("=" * 60)
        print(f"ERROR: {e}")
        print(f"ERROR TYPE: {type(e).__name__}")
        print("=" * 60)

        import traceback
        traceback.print_exc()

        if conn:
            conn.rollback()

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
