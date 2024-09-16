#db.py


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Configuramos el engine para conectar con SQLite
engine = create_engine("sqlite:///database/products.db",
                       connect_args={"check_same_thread": False})

# Base declarativa para los modelos
Base = declarative_base()

# Creamos una sesión para interactuar con la base de datos
Session = sessionmaker(bind=engine)
session = Session()


#Creamos una función para la primera vez que se inicie la app
def first_start():
    from models import User,Product #Importamos los modelos aqui para que no entre en conflito

    Base.metadata.create_all(engine) # Creamos todas las tablas de los modelos, si aún no existen

    # Hacemos dos consultas a la base de datos, para obtener el total de usuarios y productos
    users=session.query(User).all()
    products=session.query(Product).all()

    # Si las consultas dan como resultado exactamente 0 Usuarios y 0 Productos,
    # Entendemos que la aplicación nunca ha sido iniciada, por lo que
    # Crearemos unos usuarios y productos de muestra
    if not users and not products:

        # Creamos instancias de ambos
        user=User(username="user",pasw="user",email="user@user.com",birthday="30/01/2000",admin=False)
        admin=User(username="admin",pasw="admin",email="admin@admin.com",birthday="30/01/1998",admin=True)
        product1 = Product(name="Impresora", price=299.75)
        product2 = Product(name="Monitor 24'", price=247.25)
        product3 = Product(name="Teclado inalámbrico", price=48.90)
        product4 = Product(name="Ratón inalámbrico", price=77.90)
        product5 = Product(name="Auriculares inalámbricos", price=110.99)
        product6 = Product(name="Tarjeta grafica (4080)", price=460.75)
        product7 = Product(name="Router Wi-Fi", price=99.99)

        # Los añadimos a una lista
        first_list=[user,admin,product1,product2,product3,product4,product5,product6,product7]

        # Iteramos sobre esta lista
        for i in first_list:
            session.add(i) # Añadiendo uno a uno los objetos a la sesión

        session.commit() # Confirmamos cambios
        session.close() # Y cerramos la sesión



# Ejecutamos la función al inciar el programa
first_start()



