from flask import Flask, render_template, request, redirect, session
import random
import sqlite3

app = Flask(__name__)
app.secret_key = "clave_secreta"

# ================== USUARIOS ==================
usuarios = {}

# ================== CUADRO DE HONOR ==================
primer = [
    {"nombre": "JEIDI LIZET ESCOBAR ARIAS", "calificacion": "10.0", "grupo": "101"},
    {"nombre": "GEOVANNI HERNANDEZ TZOMPANZI", "calificacion": "10.0", "grupo": "102"},
    {"nombre": "ANA PAOLA GODINEZ SALGADO", "calificacion": "9.9", "grupo": "101"},
    {"nombre": "ANDREA DIAZ VELAZQUEZ", "calificacion": "9.9", "grupo": "101"},
    {"nombre": "ARELY FLORES ESTRADA", "calificacion": "9.9", "grupo": "101"},
    {"nombre": "BRENDA GONZALEZ FELIPE", "calificacion": "9.9", "grupo": "101"},
    {"nombre": "FATIMA CAMILA GALICIA GARCIA", "calificacion": "9.9", "grupo": "101"},
    {"nombre": "ANGELES HERNANDEZ REYES", "calificacion": "9.9", "grupo": "102"},
    {"nombre": "FERNANDA GARDUÑO SALGADO", "calificacion": "9.9", "grupo": "102"},
    {"nombre": "JUAN ANTONIO MUNGUIA FELIX", "calificacion": "9.9", "grupo": "102"},
    {"nombre": "ANALY LIMA JACINTO", "calificacion": "9.9", "grupo": "104"},
    {"nombre": "CARLA FERNANDA CELESTINO MORA", "calificacion": "9.9", "grupo": "104"},
    {"nombre": "VICTORIA CASTILLO GARCÍA", "calificacion": "9.9", "grupo": "104"},
    {"nombre": "MARIA MERCEDES SALGADO BERNAL", "calificacion": "9.7", "grupo": "101"},
    {"nombre": "NATALY PAOLA PEÑA MARÍN", "calificacion": "9.7", "grupo": "101"},
    {"nombre": "OSCAR DANIEL SEGUNDO AUSENCIO", "calificacion": "9.7", "grupo": "101"},
    {"nombre": "SANTIAGO JESUS SALGADO MARTINEZ", "calificacion": "9.7", "grupo": "101"},
    {"nombre": "YARITZEL MARTINEZ COLIN", "calificacion": "9.7", "grupo": "102"},
    {"nombre": "DANNA PAOLA GARDUÑO MONDRAGON", "calificacion": "9.7", "grupo": "103"},
    {"nombre": "FERNANDA ISABELLA JUAN MARIN", "calificacion": "9.7", "grupo": "103"},
    {"nombre": "NEREY IVANA RANGEL DOMINGUEZ", "calificacion": "9.7", "grupo": "103"},
    {"nombre": "GRETEL RANGEL DOMINGUEZ", "calificacion": "9.7", "grupo": "104"},
    {"nombre": "LEYDI YARETZI GARDUÑO BARRIOS", "calificacion": "9.7", "grupo": "104"},
    {"nombre": "REGINA GARDUÑO GONZALEZ", "calificacion": "9.7", "grupo": "101"},
    {"nombre": "VANESSA GALICIA CONRADO", "calificacion": "9.6", "grupo": "102"},
    {"nombre": "XOCHITL AMERICA RANGEL ALAMILLA", "calificacion": "9.6", "grupo": "102"},
    {"nombre": "ASHER ISAAC JAIMES ORTIZ", "calificacion": "9.6", "grupo": "103"},
    {"nombre": "IRAIS SAMARY CARMONA PICHARDO", "calificacion": "9.6", "grupo": "103"},
    {"nombre": "JUAN LUIS TENORIO HERNANDEZ", "calificacion": "9.6", "grupo": "103"},
    {"nombre": "MAGDALENA CRUZ SALGADO", "calificacion": "9.6", "grupo": "103"},
    {"nombre": "KARLA IVETH ALEJO ASCENCIO", "calificacion": "9.6", "grupo": "104"},
    {"nombre": "KARLA ITZEL MARTINEZ MILLAN", "calificacion": "9.6", "grupo": "105"},
    {"nombre": "LUIS FERNANDO VELAZQUEZ QUINTERO", "calificacion": "9.6", "grupo": "105"},
    {"nombre": "BEATDRRIZ NIETO MARTINEZ", "calificacion": "9.6", "grupo": "101"},
    {"nombre": "JOHANA ILIAN ARIAS DIAZ", "calificacion": "9.4", "grupo": "101"},
    {"nombre": "YOSAJANDI YERALDIN RODRIGUEZ MARTINEZ", "calificacion": "9.4", "grupo": "101"},
    {"nombre": "DANNA PAOLA GARCIA GARCIA", "calificacion": "9.4", "grupo": "102"},
    {"nombre": "DILAN CALEB SOLIS MIGUEL", "calificacion": "9.4", "grupo": "102"},
    {"nombre": "DILAN YAXER RANGER MARIN", "calificacion": "9.4", "grupo": "102"},
    {"nombre": "HUMBERTO ESCOBAR ALVAREZ", "calificacion": "9.4", "grupo": "102"},
    {"nombre": "YURIDIA VILCHIS REYES", "calificacion": "9.4", "grupo": "102"},
    {"nombre": "ADRIANA VARGAS TORRES", "calificacion": "9.4", "grupo": "103"},
    {"nombre": "JAIME VENTEÑO LOPEZ", "calificacion": "9.4", "grupo": "103"},
    {"nombre": "DANIELA VELAZQUEZ FRANCISCO", "calificacion": "9.4", "grupo": "104"},
    {"nombre": "OFELIA GUADALUPE SUAREZ MEJIA", "calificacion": "9.4", "grupo": "104"},
    {"nombre": "OZIEL EMMANUEL VALLEJO GONZALEZ", "calificacion": "9.4", "grupo": "104"},
    {"nombre": "XIMENA NAVA VALDEZ", "calificacion": "9.4", "grupo": "104"},
    {"nombre": "MARIA DEL CARMEN REYNA CAMACHO", "calificacion": "9.3", "grupo": "101"},
    {"nombre": "SANTIAGO YAEL NARCIZO ESCOBAR", "calificacion": "9.3", "grupo": "101"},
    {"nombre": "HIROMI YARETZI DAVALOS MERCADO", "calificacion": "9.3", "grupo": "102"},
    {"nombre": "IKER JESUS SALGADO MARTINEZ", "calificacion": "9.3", "grupo": "102"},
    {"nombre": "VALERIA GISELLE PEDRO CARMONA", "calificacion": "9.3", "grupo": "102"},
    {"nombre": "FERNANDO CASTRO CRISANTOS", "calificacion": "9.3", "grupo": "103"},
    {"nombre": "JADE ABRIL MUNGUIA GARDUÑO", "calificacion": "9.3", "grupo": "103"},
    {"nombre": "CAMILA MORENO RANGEL", "calificacion": "9.3", "grupo": "104"},
    {"nombre": "MONSERRATH SANCHEZ ALEJO", "calificacion": "9.3", "grupo": "104"},
    {"nombre": "ALFONSO RUZ TENORIO", "calificacion": "9.3", "grupo": "105"},
    {"nombre": "ABRAHAM MENDOZA CASTILLEJOS", "calificacion": "9.1", "grupo": "101"},
    {"nombre": "IRIS GUADALUPE HERNANDEZ VENTEÑO", "calificacion": "9.1", "grupo": "101"},
    {"nombre": "LUIS FERNANDO HERIBERTO ALGODON", "calificacion": "9.1", "grupo": "101"},
    {"nombre": "JIMENA CAMACHO CARBAJAL", "calificacion": "9.1", "grupo": "102"},
    {"nombre": "LICXIN YURICELY PALACIOS LOPEZ", "calificacion": "9.1", "grupo": "102"},
    {"nombre": "LUIS FERNANDO SANCHEZ FLORENCIO", "calificacion": "9.1", "grupo": "102"},
    {"nombre": "ARNOL ALDAIR ESPARZA CAMACHO", "calificacion": "9.1", "grupo": "103"},
    {"nombre": "BRAYAN ALONSO LAGORRETA LOPEZ", "calificacion": "9.1", "grupo": "103"},
    {"nombre": "PAOLA CRUZ MONDRAGON", "calificacion": "9.1", "grupo": "103"},
    {"nombre": "ELENA MONSERRAT MEDINA MARTINEZ", "calificacion": "9.1", "grupo": ""},
    {"nombre": "JADE CRISPIN SEGUNDO", "calificacion": "9.1", "grupo": ""},
    {"nombre": "JUAN DIEGO ESTRADA ZAMORA", "calificacion": "9.1", "grupo": ""},
    {"nombre": "YAIREL ITURBIDE SALVADOR", "calificacion": "9.1", "grupo": ""},
    {"nombre": "DANA MARLEN GARCIA GARCIA", "calificacion": "9.1", "grupo": ""},
    {"nombre": "ITZEL ALVAREZ MARTINEZ", "calificacion": "9.1", "grupo": ""},
    {"nombre": "PAULINA OROZCO VARGAS", "calificacion": "9.1", "grupo": ""},
    {"nombre": "VANESSA INES CONTRERAS", "calificacion": "9.1", "grupo": ""}
]

tercer = [
    {"nombre": "ANDRÉ LIZÁRRAGA MORALES", "calificacion": 10.0, "grupo": 301},
    {"nombre": "BRENDA DOMÍNGUEZ MEDINA", "calificacion": 10.0, "grupo": 301},
    {"nombre": "EVELIN FELIPE FRANCISCO", "calificacion": 10.0, "grupo": 301},
    {"nombre": "LUIS HAZEL FABIÁN MEDINA", "calificacion": 10.0, "grupo": 301},
    {"nombre": "YULISSA CARVAJAL MARTÍNEZ", "calificacion": 10.0, "grupo": 301},
    {"nombre": "ZULEYMA ESTRELLA NIETO MEDINA", "calificacion": 10.0, "grupo": 301},
    {"nombre": "ANDREA ROXXXANA CARMONA DE LOS SANTOS", "calificacion": 10.0, "grupo": 302},
    {"nombre": "DANNA PAOLA VELÁZQUEZ INIESTA", "calificacion": 10.0, "grupo": 302},
    {"nombre": "DANNY ALEXA PAULINO GARCÍA", "calificacion": 10.0, "grupo": 302},
    {"nombre": "LIA RENATA ÁLVAREZ GONZÁLEZ", "calificacion": 10.0, "grupo": 302},
    {"nombre": "LLUVIA ESMERALDA GÓMEZ ARRIAGA", "calificacion": 10.0, "grupo": 302},
    {"nombre": "LUCERO VILCHIS VILLARREAL", "calificacion": 10.0, "grupo": 302},
    {"nombre": "RUBÍ GUADALUPE JUAN JUÁREZ", "calificacion": 10.0, "grupo": 302},
    {"nombre": "SARAH DANIELA PEÑA MARÍN", "calificacion": 10.0, "grupo": 302},
    {"nombre": "ULISES CONTRERAS GARCÍA", "calificacion": 10.0, "grupo": 302},
    {"nombre": "VÍCTOR IVÁN LARA PADUA", "calificacion": 10.0, "grupo": 302},
    {"nombre": "FRIDA PAOLA BARRIOS SALGADO", "calificacion": 10.0, "grupo": 303},
    {"nombre": "MARIALE OROZCO BARRIOS", "calificacion": 10.0, "grupo": 303},
    {"nombre": "YURITZI NAYATZI SUÁREZ GARCÍA", "calificacion": 10.0, "grupo": 304},
    {"nombre": "ARMANDO FLORES ESTRADA", "calificacion": 9.9, "grupo": 301},
    {"nombre": "ELISA VICTORIA MARTÍNEZ MARTÍNEZ", "calificacion": 9.9, "grupo": 301},
    {"nombre": "JUAN MANUEL ÁLVAREZ MARÍN", "calificacion": 9.9, "grupo": 301},
    {"nombre": "MEXTLI XIMENA CARBAJAL SALGADO", "calificacion": 9.9, "grupo": 301},
    {"nombre": "VANESSA MARTÍNEZ ALMAZÁN", "calificacion": 9.9, "grupo": 301},
    {"nombre": "ADRIANA MATEO SEGUNDO", "calificacion": 9.9, "grupo": 302},
    {"nombre": "CAROLINA GARCÍA GONZÁLEZ", "calificacion": 9.9, "grupo": 302},
    {"nombre": "FERNANDA MARTÍNEZ MORENO", "calificacion": 9.9, "grupo": 302},
    {"nombre": "MARIANA SÁNCHEZ SÁNCHEZ", "calificacion": 9.9, "grupo": 302},
    {"nombre": "TANIA TENORIO SEVERIANO", "calificacion": 9.9, "grupo": 302},
    {"nombre": "LUZ ANNALI REYES BRÍGIDO", "calificacion": 9.9, "grupo": 303},
    {"nombre": "MARÍA NAYELI REYES MERCADO", "calificacion": 9.9, "grupo": 303},
    {"nombre": "MIGUEL GUTIÉRREZ BARRIOS", "calificacion": 9.9, "grupo": 303},
    {"nombre": "ANA KAREN ÁLVAREZ CRUZ", "calificacion": 9.9, "grupo": 304},

    {"nombre": "CARLOS ADRIÁN BERNARDO GARCÍA", "calificacion": 9.7, "grupo": 301},
    {"nombre": "CINTHIA DOMÍNGUEZ DÍAZ", "calificacion": 9.7, "grupo": 301},
    {"nombre": "ALAN JESÚS ESCOBAR ALMAZÁN", "calificacion": 9.7, "grupo": 302},
    {"nombre": "ALEYDIS YAMILA VILCHIS GÓMEZ", "calificacion": 9.7, "grupo": 302},
    {"nombre": "EDSON ULISES ARCHUNDIA GARCÍA", "calificacion": 9.7, "grupo": 302},
    {"nombre": "IAN YAEL FRANCO GASPAR", "calificacion": 9.7, "grupo": 302},
    {"nombre": "JAQUELINE GIL SALGADO", "calificacion": 9.7, "grupo": 302},
    {"nombre": "JOCELIN SÁNCHEZ MATÍAS", "calificacion": 9.7, "grupo": 302},
    {"nombre": "KENIA TENORIO SEVERIANO", "calificacion": 9.7, "grupo": 302},
    {"nombre": "MAGALY ÁLVAREZ VELÁZQUEZ", "calificacion": 9.7, "grupo": 302},
    {"nombre": "MARÍA GUADALUPE CONTRERAS REYES", "calificacion": 9.7, "grupo": 302},
    {"nombre": "MARÍA JOSÉ GÓMORA RUIZ", "calificacion": 9.7, "grupo": 302},
    {"nombre": "EMILY YISEL HERRERA ACOLTZI", "calificacion": 9.7, "grupo": 303},
    {"nombre": "NATALI LÓPEZ CARMONA", "calificacion": 9.7, "grupo": 303},
    {"nombre": "FERNANDA CAMACHO OROZCO", "calificacion": 9.7, "grupo": 304},
    {"nombre": "MARISELA GARCÍA PÉREZ", "calificacion": 9.7, "grupo": 304},

    {"nombre": "GABRIEL VELÁZQUEZ CASTRO", "calificacion": 9.6, "grupo": 301},
    {"nombre": "MARÍA FERNANDA MARTÍNEZ DELGADO", "calificacion": 9.6, "grupo": 301},
    {"nombre": "MICHELLE ZOÉ ARRIAGA GARCÍA", "calificacion": 9.6, "grupo": 301},
    {"nombre": "VALERIA CAROLINA VELÁZQUEZ COLÍN", "calificacion": 9.6, "grupo": 301},
    {"nombre": "YAMILETH DE JESÚS DOMÍNGUEZ", "calificacion": 9.6, "grupo": 301},
    {"nombre": "ARELI JULIETH MUNGUÍA ALANÍS", "calificacion": 9.6, "grupo": 302},
    {"nombre": "BRENDA URIBE ENRÍQUEZ", "calificacion": 9.6, "grupo": 302},
    {"nombre": "MARENI MARTÍNEZ MARTÍNEZ", "calificacion": 9.6, "grupo": 302},
    {"nombre": "MARÍA DE JESÚS PIÑA DOMÍNGUEZ", "calificacion": 9.6, "grupo": 302},
    {"nombre": "SARAÍ SÁNCHEZ VELÁZQUEZ", "calificacion": 9.6, "grupo": 303},
    {"nombre": "SARAÍ AHASTARI CRUZ QUINTANA", "calificacion": 9.6, "grupo": 303},
    {"nombre": "ANDREA VENTEÑO ÁLVAREZ", "calificacion": 9.6, "grupo": 304},
    {"nombre": "FRANCO JORDI ESCOBAR ESQUIVEL", "calificacion": 9.6, "grupo": 304},
    {"nombre": "JACQUELINE VELÁZQUEZ GARCÍA", "calificacion": 9.6, "grupo": 304},

    {"nombre": "ALI MARTÍNEZ CARMONA", "calificacion": 9.4, "grupo": 301},
    {"nombre": "ANA KAREN MARTÍNEZ ALEJO", "calificacion": 9.4, "grupo": 301},
    {"nombre": "BELÉN ESMERALDA AMBROSIO PABLO", "calificacion": 9.4, "grupo": 301},
    {"nombre": "CRISTOPHER LIRA MÉRIDA", "calificacion": 9.4, "grupo": 301},
    {"nombre": "PRISCILA ZARAGOZA MONDRAGÓN", "calificacion": 9.4, "grupo": 301},
    {"nombre": "ANA LADY MARTÍNEZ MARTÍNEZ", "calificacion": 9.4, "grupo": 302},
    {"nombre": "KARLA FERNANDA SÁNCHEZ SÁNCHEZ", "calificacion": 9.4, "grupo": 302},
    {"nombre": "MISHELLE OLMOS TENORIO", "calificacion": 9.4, "grupo": 302},
    {"nombre": "YITZEL MELISSA MARTÍNEZ ALMAZÁN", "calificacion": 9.4, "grupo": 302},
    {"nombre": "GERALDINE GARCÍA MARTÍNEZ", "calificacion": 9.4, "grupo": 302},
    {"nombre": "XEANIY KISELLE ARRIAGA SANTOS", "calificacion": 9.4, "grupo": 303},
    {"nombre": "JONATHAN MANUEL ESQUIVEL MARTÍNEZ", "calificacion": 9.4, "grupo": 304},

    {"nombre": "GUADALUPE URBINA GARDUÑO", "calificacion": 9.3, "grupo": 301},
    {"nombre": "JESÚS BALDOMERO CARBAJAL PADILLA", "calificacion": 9.3, "grupo": 301},
    {"nombre": "KARLA FERNANDA JAIME VARGAS", "calificacion": 9.3, "grupo": 301},
    {"nombre": "MARÍA GUADALUPE VARGAS GÓMEZ", "calificacion": 9.3, "grupo": 301},
    {"nombre": "ARELI LÓPEZ CABALLERO", "calificacion": 9.3, "grupo": 301},
    {"nombre": "CARMEN AURORA FLORES GONZÁLEZ", "calificacion": 9.3, "grupo": 302},
    {"nombre": "GABRIEL VÁZQUEZ GONZÁLEZ", "calificacion": 9.3, "grupo": 302},
    {"nombre": "JONATHAN ROSAS FRANCISCO", "calificacion": 9.3, "grupo": 302},
    {"nombre": "VLADIMIR ANICETO RANGEL", "calificacion": 9.3, "grupo": 302},
    {"nombre": "HAY DE GUADALUPE MORENO LÓPEZ", "calificacion": 9.3, "grupo": 303},
    {"nombre": "ÍNGRID ANALI HERNÁNDEZ CORONA", "calificacion": 9.3, "grupo": 303},
    {"nombre": "ITZEL SAMANTHA MARTÍNEZ JUAN", "calificacion": 9.3, "grupo": 303},
    {"nombre": "JESÚS BENJAMÍN CASTILLO GIL", "calificacion": 9.3, "grupo": 303},
    {"nombre": "JOCELIN YATZIRI REBOLLO GARDUÑO", "calificacion": 9.3, "grupo": 303},
    
    {"nombre": "MARTIN TENORIO SALGADO", "calificacion": 9.3, "grupo": 303},
    {"nombre": "ALAN YAIR VILCHIS EPIFANIO", "calificacion": 9.3, "grupo": 304},
    {"nombre": "KAREN ALEJANDRA CRISTINO RICO", "calificacion": 9.3, "grupo": 304},
    {"nombre": "ALAN DAVID MARTÍNEZ VILLAFAÑA", "calificacion": 9.1, "grupo": 301},
    {"nombre": "BLANCA ESTELA MONTES DE OCA PARAMO", "calificacion": 9.1, "grupo": 301},
    {"nombre": "DIANA GARCÍA GONZÁLEZ", "calificacion": 9.1, "grupo": 301},
    {"nombre": "MAITE CAMACHO LÓPEZ", "calificacion": 9.1, "grupo": 301},
    {"nombre": "ALEXANDER REMIGIO BALTAZAR", "calificacion": 9.1, "grupo": 302},
    {"nombre": "MIRANDA LÓPEZ OBANDO", "calificacion": 9.1, "grupo": 305},
    {"nombre": "ABRIL XIMENA ENRÍQUEZ GARCÍA", "calificacion": 9.1, "grupo": 304},
    {"nombre": "JAZMIN MARTINEZ ALANÍS", "calificacion": 9.0, "grupo": 304},
    {"nombre": "ANGEL DAVID FLORENCIO CARBAJAL", "calificacion": 9.0, "grupo": 304},
    {"nombre": "SANDI JIMENA GARCÍA SAMANO", "calificacion": 9.0, "grupo": 304},
    {"nombre": "JONATAN JESÚS VELAZQUEZ MORENO", "calificacion": 9.0, "grupo": 303},
    {"nombre": "EZEQUIEL GAMACHO REYNA", "calificacion": 9.0, "grupo": 304},
    {"nombre": "GABRIELA DOMINGUEZ ALVAREZ", "calificacion": 9.0, "grupo": 304}
]

quinto = [
     {"nombre": "ALISON FABIÁN DÍAZ", "calificacion": 10.0, "grupo": 502},
    {"nombre": "IVÁN GONZÁLEZ INÉS", "calificacion": 10.0, "grupo": 502},
    {"nombre": "MARÍA GUADALUPE ENRÍQUEZ DOMÍNGUEZ", "calificacion": 10.0, "grupo": 502},
    {"nombre": "BRIGID OSORIO OSORIO", "calificacion": 9.9, "grupo": 501},
    {"nombre": "JIMENA SOFÍA VILLEGAS VELÁZQUEZ", "calificacion": 9.9, "grupo": 501},
    {"nombre": "MARCO ANTONIO OLMOS SANTOS", "calificacion": 9.9, "grupo": 501},
    {"nombre": "XOCHITLH QUETZAL CARBAJAL SALGADO", "calificacion": 9.9, "grupo": 501},
    {"nombre": "ARELLY SARAÍ CHALA CARBAJAL", "calificacion": 9.9, "grupo": 502},
    {"nombre": "CAMILA CARBAJAL LÓPEZ", "calificacion": 9.9, "grupo": 502},
    {"nombre": "JENNIFER GONZÁLEZ NAVA", "calificacion": 9.9, "grupo": 502},

    {"nombre": "JESÚS ALEXANDER PASCUAL LÓPEZ", "calificacion": 9.7, "grupo": 502},
    {"nombre": "MARIANA CARBAJAL BERNAL", "calificacion": 9.7, "grupo": 501},
    {"nombre": "PRISCILA NARCISO", "calificacion": 9.7, "grupo": 501},
    {"nombre": "ARIADNA ESTÉVEZ SEVERIANO", "calificacion": 9.7, "grupo": 501},
    {"nombre": "AXEL ABI SALGADO ZEPEDA", "calificacion": 9.7, "grupo": 502},
    {"nombre": "DULCE ANETH SALGADO VILCHIS", "calificacion": 9.7, "grupo": 502},
    {"nombre": "ERICK SALGADO MODESTO", "calificacion": 9.7, "grupo": 502},
    {"nombre": "KARLA PALACIOS MARTÍNEZ", "calificacion": 9.7, "grupo": 502},
    {"nombre": "MADAHY PALACIOS LÓPEZ", "calificacion": 9.7, "grupo": 502},
    {"nombre": "MICHELLE ÁLVAREZ ZEPEDA", "calificacion": 9.7, "grupo": 502},
    {"nombre": "PAMELA CASARES VALDEZ", "calificacion": 9.7, "grupo": 502},
    {"nombre": "ÁNGELES MARTÍNEZ VÁZQUEZ", "calificacion": 9.7, "grupo": 503},
    {"nombre": "MARIAN REYES GARCÍA", "calificacion": 9.7, "grupo": 503},
    {"nombre": "OSCAR JESÚS CARBAJAL VÁZQUEZ", "calificacion": 9.7, "grupo": 503},
    {"nombre": "YAHEL LENO ANDRACA", "calificacion": 9.7, "grupo": 504},
    {"nombre": "JACQUELINE DÍAZ VARGAS", "calificacion": 9.6, "grupo": 501},
    {"nombre": "GABRIELA VELARDE REYES", "calificacion": 9.6, "grupo": 502},
    {"nombre": "INGRID ANGELICA JIMENA SÁNCHEZ", "calificacion": 9.6, "grupo": 502},
    {"nombre": "JULIO ALEXANDER VALDEZ VEGA", "calificacion": 9.6, "grupo": 502},
    {"nombre": "LUIS FERNANDO MARTÍNEZ GÁLVEZ", "calificacion": 9.6, "grupo": 502},
    {"nombre": "NORMA GARCÍA VILLAFAÑA", "calificacion": 9.6, "grupo": 502},
    {"nombre": "JOSÉ ALFREDO CARBAJAL ÁLVAREZ", "calificacion": 9.6, "grupo": 502},
    {"nombre": "ROSA EVELYN HERRERA GONZÁLEZ", "calificacion": 9.6, "grupo": 504},
    {"nombre": "ELIZABETH DÍAZ ACOLTZI", "calificacion": 9.6, "grupo": 504},
    {"nombre": "FÁTIMA SALGADO VELÁZQUEZ", "calificacion": 9.4, "grupo": 501},
    {"nombre": "PERLA MARTÍNEZ SALGADO", "calificacion": 9.4, "grupo": 501},
    {"nombre": "VANESSA LIZETH VELÁZQUEZ MARTÍNEZ", "calificacion": 9.4, "grupo": 501},
    {"nombre": "ÁNGEL DAVID SEGUNDO JIMÉNEZ", "calificacion": 9.4, "grupo": 501},
    {"nombre": "ARIANA MARÍN AUSENCIO", "calificacion": 9.4, "grupo": 502},
    {"nombre": "KAREN GODÍNEZ GONZÁLEZ", "calificacion": 9.4, "grupo": 502},
    {"nombre": "LIZBETH TENORIO SALGADO", "calificacion": 9.4, "grupo": 502},
    {"nombre": "JIMENA GARDUÑO SEVERIANO", "calificacion": 9.4, "grupo": 503},
    {"nombre": "JOSSELIN GARDUÑO CRUZ", "calificacion": 9.4, "grupo": 503},
    {"nombre": "MARÍA JOSÉ CARMONA GONZÁLEZ", "calificacion": 9.4, "grupo": 503},
    {"nombre": "YAIR REBOLLO ESQUIVEL", "calificacion": 9.4, "grupo": 504},
    {"nombre": "ASTRIT ITZEL IDELEFONSO GARDUÑO", "calificacion": 9.4, "grupo": 504},
    {"nombre": "IVET DÍAZ GÓMEZ", "calificacion": 9.4, "grupo": 504},
    {"nombre": "MIN SALGADO", "calificacion": 9.4, "grupo": 504},

    {"nombre": "ANALY MERCADO BENÍTEZ", "calificacion": 9.3, "grupo": 501},
    {"nombre": "ERICK EDUARDO LÓPEZ MARTÍNEZ", "calificacion": 9.3, "grupo": 501},
    {"nombre": "KIMBERLY HIROMY ÁLVAREZ VELÁZQUEZ", "calificacion": 9.3, "grupo": 501},
    {"nombre": "NAHOMY JANNEY MORALES LÓPEZ", "calificacion": 9.3, "grupo": 501},
    {"nombre": "REYNA VELÁZQUEZ VELÁZQUEZ", "calificacion": 9.3, "grupo": 501},
    {"nombre": "ALEJANDRA RICO VELÁZQUEZ", "calificacion": 9.3, "grupo": 502},
    {"nombre": "ELIZABETH VELÁZQUEZ VELÁZQUEZ", "calificacion": 9.3, "grupo": 502},
    {"nombre": "HUGO DANIEL DOMÍNGUEZ VÁZQUEZ", "calificacion": 9.3, "grupo": 502},
    {"nombre": "FILIBERTO VILLAFAÑA BARRIOS", "calificacion": 9.3, "grupo": 503},
    {"nombre": "JOSÉ ALBERTO TRUJILLO RAMÍREZ", "calificacion": 9.3, "grupo": 503},
    {"nombre": "REY DAVID GONZÁLEZ ÁVILA", "calificacion": 9.3, "grupo": 503},
    {"nombre": "XOCHITL CITLALI REBOLLO ÁNGELES", "calificacion": 9.3, "grupo": 503},
    {"nombre": "OCTAVIO QUINTERO ZEPEDA", "calificacion": 9.3, "grupo": 504},
    {"nombre": "YAQUELIN GONZÁLEZ GONZÁLEZ", "calificacion": 9.3, "grupo": 504},
    {"nombre": "BENJAMÍN MONDRAGÓN CARBAJAL", "calificacion": 9.1, "grupo": 501},
    {"nombre": "CAROL MARTÍNEZ MARTÍNEZ", "calificacion": 9.1, "grupo": 501},
    {"nombre": "YAIR RANGEL SOLIS", "calificacion": 9.1, "grupo": 501},
    {"nombre": "AILED CALLO REMIGIO", "calificacion": 9.1, "grupo": 502},
    {"nombre": "DULCE FLOR DE MARÍA ALANÍS CARBAJAL", "calificacion": 9.1, "grupo": 502},
    {"nombre": "ERNESTO ALONSO SÁNCHEZ MUNGÍA", "calificacion": 9.1, "grupo": 502},
    {"nombre": "JUAN MIGUEL DOMÍNGUEZ DÍAZ", "calificacion": 9.1, "grupo": 502},
    {"nombre": "MICHEL RAFAEL GONZÁLEZ", "calificacion": 9.1, "grupo": 502},
    {"nombre": "BERENICE OROZCO LÓPEZ", "calificacion": 9.1, "grupo": 503},
    {"nombre": "JOSÉ MARÍA SALGADO VARGAS", "calificacion": 9.1, "grupo": 503},
    {"nombre": "KARLA ESMERALDA CARMONA PIÑA", "calificacion": 9.1, "grupo": 503},
    {"nombre": "MARÍA DOLORES BENTEÑO TENORIO", "calificacion": 9.1, "grupo": 504},
    {"nombre": "ADOLFO ÁNGEL MARTÍNEZ CARBAJAL", "calificacion": 9.1, "grupo": 504},
    {"nombre": "ISMAEL SALGADO OROZCO", "calificacion": 9.1, "grupo": 504},
    {"nombre": "STEPHANIE ESMERALDA ARIAS RAMÍREZ", "calificacion": 9.1, "grupo": 504},
    {"nombre": "FREDY DELGADO REYES", "calificacion": 9.0, "grupo": 501},
    {"nombre": "MONTSE MONTSERRAT GARCÍA DIONICIO", "calificacion": 9.0, "grupo": 501},
    {"nombre": "RODRIGO ARIAS CARMONA", "calificacion": 9.0, "grupo": 504},
    {"nombre": "MARÍA FERNANDA MUÑOZ GARDUÑO", "calificacion": 9.0, "grupo": 503},
    {"nombre": "DANIEL GONZÁLEZ VELÁZQUEZ", "calificacion": 9.0, "grupo": 504},
    {"nombre": "INGRID COLIN MONTORO", "calificacion": 9.0, "grupo": 504}
]

# ================== BASE DE DATOS ==================
def get_db():
    return sqlite3.connect("base.db")

def crear_tabla():
    db = get_db()
    c = db.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS anuncios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            texto TEXT,
            fecha TEXT
        )
    """)
    db.commit()
    db.close()

crear_tabla()

# ================== JUEGO ==================
numero = random.randint(1, 250)

# ================== SISTEMA PRINCIPAL ==================
@app.route("/", methods=["GET", "POST"])
def sistema():
    global numero

    page = request.args.get("page", "registro")
    mensaje_juego = ""

    # ---------- REGISTRO ----------
    if page == "registro" and request.method == "POST":
        usuario = request.form["usuario"]
        contraseña = request.form["contraseña"]
        usuarios[usuario] = contraseña
        session["usuario"] = usuario
        return redirect("/?page=principal")

    # ---------- LOGOUT ----------
    if page == "logout":
        session.clear()
        return redirect("/")

    # ---------- CREAR ANUNCIO ----------
    if page == "anuncios" and request.method == "POST":
        nombre = request.form["nombre"]
        texto = request.form["texto"]
        fecha = request.form["fecha"]

        db = get_db()
        c = db.cursor()
        c.execute(
            "INSERT INTO anuncios (nombre, texto, fecha) VALUES (?,?,?)",
            (nombre, texto, fecha)
        )
        db.commit()
        db.close()
        return redirect("/?page=anuncios")

    # ---------- JUEGO ----------
    if page == "juego" and request.method == "POST":
        try:
            intento = int(request.form["numero"])

            if intento == numero:
                mensaje_juego = "🎉 ¡Correcto! Adivinaste el número"
                numero = random.randint(1, 250)
            elif intento < numero:
                mensaje_juego = "⬆ El número es mayor"
            else:
                mensaje_juego = "⬇ El número es menor"

        except ValueError:
            mensaje_juego = "❌ Ingresa un número válido"

    # ---------- LEER ANUNCIOS ----------
    db = get_db()
    c = db.cursor()
    c.execute("SELECT id, nombre, texto, fecha FROM anuncios ORDER BY id DESC")
    anuncios = c.fetchall()
    db.close()

    return render_template(
        "INDE_X_X.html",
        page=page,
        usuario=session.get("usuario"),
        anuncios=anuncios,
        primer=primer,
        tercer=tercer,
        quinto=quinto,
        mensaje_juego=mensaje_juego
    )

# ================== BORRAR ANUNCIO ==================
@app.route("/borrar_anuncio/<int:id>")
def borrar_anuncio(id):
    db = get_db()
    c = db.cursor()
    c.execute("DELETE FROM anuncios WHERE id=?", (id,))
    db.commit()
    db.close()
    return redirect("/?page=anuncios")

# ================== EDITAR ANUNCIO ==================
@app.route("/editar_anuncio/<int:id>", methods=["GET", "POST"])
def editar_anuncio(id):
    db = get_db()
    c = db.cursor()

    if request.method == "POST":
        nombre = request.form["nombre"]
        texto = request.form["texto"]
        fecha = request.form["fecha"]

        c.execute(
            "UPDATE anuncios SET nombre=?, texto=?, fecha=? WHERE id=?",
            (nombre, texto, fecha, id)
        )
        db.commit()
        db.close()
        return redirect("/?page=anuncios")

    c.execute("SELECT id, nombre, texto, fecha FROM anuncios WHERE id=?", (id,))
    anuncio = c.fetchone()
    db.close()

    return render_template(
        "INDE_X_X.html",
        page="editar_anuncio",
        anuncio=anuncio
    )

# ================== EJECUCIÓN ==================
if __name__ == "__main__":
    app.run(debug=True)
