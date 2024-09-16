#models.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime,Float,ForeignKey,JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import pytz  # Importa pytz para manejar zonas horarias
from db import Base


# Definimos el modelo User, que es el que manejará la tabla de datos de los usuarios
class User(Base):
    __tablename__ = "user" # Nombre de la tabla en la base de datos
    __table_args__ = {"sqlite_autoincrement": True} # Permitimos que se autoincremente la primary key

    id = Column(Integer, primary_key=True) # Id unico para cada usuario
    username = Column(String, nullable=False,unique=True) # Usuario que nunca puede estár vacio, ni coincidir con otro
    _pasw = Column(String, nullable=False) # Contraseña nunca vacia
    email = Column(String,nullable=False,unique=True) # Usuario nunca vacio y unico
    age = Column(Integer,nullable=False) # Edad al momento de registrarse
    admin = Column(Boolean, nullable=False) # Columna que indicará si el usuario se trata de administrador o usuario raso
    # Capturará la fecha y hora de registro del usuario en la zona horaria de Madrid
    creation_date = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Europe/Madrid')))
    # Relacionamos cada usuario con su carrito de compras, y nos aseguramos que solo exista un carrito por usuario
    cart = relationship("Cart", back_populates="user", uselist=False)

    # En el constructor, pasamos como argumento admin=False por defecto, ya que la mayoria deberian ser usuarios normales
    def __init__(self, username, pasw, email, birthday, admin=False):
        self.username = username # Definimos el usuario
        self._pasw = pasw.encode('utf-8').hex() # Guardamos la contraseña en hexadecimal
        self.email = email # Definimos el correo
        # Guardamos la edad del usuario, llamando al metodo que calculará la edad segun la fecha de nacimiento
        # Proporcionada en el registro por el usuario
        self.age = self.calculate_age(birthday)
        self.admin = admin  # Asignamos el valor de administrador
        self.cart = Cart(username=self.username) # Creamos un carrito asociado al usuario

    @property
    def pasw(self):
        return self._pasw

    @pasw.setter
    def pasw(self, new_password):
        self._pasw = new_password.encode('utf-8').hex()



    def __str__(self):
        return f"{self.username}, {self.admin}, {self.creation_date}"

    #Creamos una función que se encargará de calcular la edad del usuario mediante la fecha proporcionada en el registro
    def calculate_age(self,birthday):
        # Convertimos la fecha de nacimiento en un objeto de tiempo con un formato especifico
        birthday_obj = datetime.strptime(birthday, "%d/%m/%Y")
        # Ajustamos la fecha a la zona horaria de Madrid
        birthday_obj = pytz.timezone('Europe/Madrid').localize(birthday_obj)
        # Calculamos la edad restando la fecha obtenida con la fecha actual de Madrid
        age = datetime.now(pytz.timezone('Europe/Madrid')) - birthday_obj
        #Divimos los dias obtenidos entre 365 que son los que tiene un año
        age_years = age.days // 365
        return age_years  # Y devolvemos el valor obtenido

# Definimos el modelo de producto, para alojar todos los productos en la app
class Product(Base):
    __tablename__ = "product" # Nombre de la tabla
    __table_args__ = {"sqlite_autoincrement": True} # Clave principal autoincrementable

    # Creamos las columnas de ID, nombre, precio y fecha de creación
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    creation_date = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Europe/Madrid')))

    # En el constructor solo pasaremos como argumentos nombre y precio
    def __init__(self, name, price):
        self.name = name
        self.price = price


    def __str__(self):
        return f"{self.name}, {self.price}, {self.creation_date}"


# Creamos el carrito por cada usuario
class Cart(Base):
    __tablename__ = 'carts' #Nombre de la tabla
    id = Column(Integer, primary_key=True) # ID del carrito como clave principal
    # Columna 'username' que actúa como clave foránea para referenciar la tabla 'user'
    username = Column(Integer, ForeignKey('user.username'))
    # Relación de uno a uno con el modelo 'User'. 'back_populates' asegura que las dos direcciones de la relación se mantengan sincronizadas
    user = relationship("User", back_populates="cart")
    products = Column(JSON) # Columna para almacenar los productos del carrito en formato JSON
    total_price= Column(Float) # Columna para almacenar el precio total de los productos agregados

    #Pasamos solamente el usuario en el constructor
    def __init__(self, username):
        self.username = username
        self.products = [] # Y además creamos la lista para almacenar los productos