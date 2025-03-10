# Guía de Django para ISPP


1. [Introducción]()




1. [Introducción](#1-datos-fundamentales-del-equipo)  
2. [Instalación, preparación y ejecución]()  
    - [Instalación de repositorio y BD]()
    - [Ejecución general]()
    - [*Imports*]()
    - [Migraciones]()
    - [Ejecutar tests]()
3. [Estructura]()
    - [Estructura de carpetas]()
    - [Funcionalidades y flujo de información]()
4. [Modelos]()
    - []()
5. [Validaciones]()
6. [Archivado]()
7. [Permisos de roles]()
8. [Serializadores]()
9. [Enrutamiento]()
10. [Controladores y servicios]()
11. [Tests]()




<br><br><br>

## 1. Introducción

Esto es una guía que he hecho para que todos más o menos sigamos los mismos criterios básicos en cuanto de la estructura de los archivos y las rutas de la API. No soy para nada experto en Django. He echado un buen rato para estudiar cuáles eran las mejores opciones y creo el sistema que propongo ha quedado bastante lógico y robusto, pero cualquiera que tenga otra propuesta de lo que sea, que lo diga. Si preferís meter las URLS a mano en el urls.py en vez de usar el Django Rest Framework (DRF), decidlo; ambos tienen sus ventajas e inconvenientes. Si cualquiera de las cosas que haya dicho por aquí os parece una tontería o simplemente innecesario, decidlo también. Ni se os ocurra callaros.

El enlace al repositorio con algunos ejemplos: https://github.com/rafcasceb/Guia_Django_ISPP. Fijaos en cómo hacer la estructuras de las carpetas y los métodos, pero desde entonces hemos cambiado algunas cosas como el formato de las rutas por ejemplo.




<br><br><br>

## 2. Instalación, preparación y ejecución

### 2.1. Instalación de repositorio y BD
Para poder instalar la aplicación, seguir los pasos definidos en el documento [USAGE.md](https://github.com/LuisMelladoDiaz/Pawtel-ComparadorDeHotelesParaMascotas/blob/8a14a746e4555fda9609c1f78ac9b2fc6d27fba0/docs/USAGE.md) del repositorio.

Hay que crear un entorno virtual bajo el directorio `\backend`.
```bash
python -m venv venv             # crear
venv\Scripts\activate           # activar (las barras hacia la izquierda)
deactivate                      # desactivar
```

Si la ejecución de scripts está deshabilitada en el sistema, probar con el comando:
```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```


<br>

### 2.2. Ejecución general
Importante que todos los paquetes de Python deben tener un archivo `__init__.py` para poder ser reconocidos.

Para poder lanzar el proyecto, los tests o las migraciones hay que cambiar el directorio a `\backend`.


<br>

### 2.3. *Imports*
Es posible que al realizar un *import* automático su ruta empiece por "backend.pawtel". Hay que quitar "backend" y que empiece directamente por "pawtel".

También es posible que los *imports* de Django aparezcan subrayados en amarillo diciendo que no se reconocen. La solución más posible es seleccionar manualmente el intérprete del entorno virtual como el intérprete de Python. Ver la primera respuesta en esta [pregunta de StackOverflow](https://stackoverflow.com/questions/67586182/how-to-resolve-import-django-contrib-could-not-be-resolved-from-source-in-vs).


<br>

### 2.4. Migraciones
Para transformar los modelos de Django en esquemas de la base de datos hace falta realizar las llamadas migraciones. Las migraciones no se hacen solas sino que tenemos que ejecutarlas nosotros cuando implementemos cambios en los modelos para que mantener la base de dato actualizada.

Es muy importante tener cuidado con las migraciones, pues éstas se estructuran en forma de cadena, de manera que al realizar un cambio no se aplican de cero, sino que se aplican sobre las migraciones anteriores, indicando solamente los cambios. Si bien de momento no tenemos datos en las bases de datos, es muy importante no borrar ninguna migración y preservar la cadena.

Se pueden hacer migraciones de paquetes en particulares, pero es más cómodo situarse en el directorio `\backend` y hacerlo para todos a la vez. Es importante mencionar que para que esto funcione, los paquetes deben contar ya con la carpeta `migrations`. Así que si son nuevos, hay que añadirlos a mano (vacíos).

Para crear los archivos de las migraciones:
```bash
python manage.py makemigrations
```

Para aplicar las migraciones a la base de datos una vez que tenemos los archivos de las migraciones:
```bash
python manage.py migrate
```


<br>

### 2.5. Ejecutar tests
Los tests se pueden ejecutar a diferentes niveles:

A nivel general
```
python manage.py test pawtel
```

A nivel de paquete (llamados apps)
```
python manage.py test pawtel.<APP_NAME>
```

Para lanzar los tests de una sola clase:
```
python manage.py test pawtel.<APP_NAME>.tests.<TEST_FILE_NAME>
```

Para lanzar los tests de un solo método (test):
```
python manage.py test pawtel.<APP_NAME>.tests.<TEST_FILE_NAME>.<METHOD_NAME>
```

Cuidado con los *app names* porque no son tal cual los nombres de las carpetas. Es el nombre definido en el `apps.py` dentro del paquete. Hay que ir al `SETTINGS.py` y en `INSTALLED_APPS` añadir la ruta al `apps.py`. Para HotelOwner, por ejemplo, sería `"pawtel.hotel_owners.apps.HotelOwnersConfig"`.








<br><br><br>

## 3. Estructura

### 3.1. Estructura de carpetas
Representación visual de la estructura de las carpetas del proyecto a fecha del 08-08-2025. Puede que en un futuro varíe.

```csharp
backend/
│── manage.py
│── .env
│── requirements.txt
│── venv/
│── pawtel/
│   ├── hotel_owners/
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── services.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── migrations/
│   │   ├── tests/
│   │   │   ├── test_models.py
│   │   │   ├── test_serializers.py
│   │   │   ├── test_services.py
│   │   │   ├── test_views.py
│   ├── hotels/
│   │   ├── ...
│   ├── ...
```

Haremos un paquete por cada concepto/objeto principal. Lo más normal es que cada entidad represente un concepto, sin embargo, en función de su relevancia y uso, ciertas entidades pueden pertenecer a otros paquetes que no sean suyos propios. A lo mejor necesitamos una entidad auxiliar que no va a recibir ninguna consulta, sino que es por definir con más comodidad un atributo de una entidad principal. No vamos a trabajar prácticamente nunca con la entidad auxiliar sino con la principal. En ese caso, pueden estar en el mismo paquete.

Detalles relevantes:
- El archivo `manage.py` es el principal fichero ejecutable del backend. Los comandos de la consola se ejecutarán en referencia a él.
- Cada paquete dentro de `pawtel` define las llamadas "aplicaciones" (*apps*). El archivo `apps.py` define el nombre que usará. Se reflejará, como ya se ha explicado, en el `SETTINGS.py`.
- Prácticamente todos los paquetes contarán con los archivos `models.py`, `serializers.py`, `services.py`, `views.py` y `urls.py`, los cuales definirán el código principal de las funcionalidades y el flujo de información.


<br>

### 3.2. Funcionalidades y flujo de información
Las entidades se definen en el `models.py` usando el lenguaje de Django.  

#### Entidades
- Usaremos `models.py`.
- Definiremos las entidades necesarias dentro, usando el lenguaje de Django y Python.
- Realizaremos validaciones sintácticas que se aplicarán al intentar persistir en la base de datos.


#### Serializadores
- Usaremos `serializers.py`.
- Transforman las instancias de las entidades en objetos JSON. 
- Cuando esta API tenga que devolver un objeto como respuesta a una petición, no lo hará tal cual usando el objeto de Django, sino que los transformaremos a objetos JSON para que sea más cómodo trabajar con ellos desde el frontend. Para ello simplemente aplicaremos el serializador al objeto de Django antes de enviarlo.
- ADEMÁS, cuando a la API le llegue un objeto con datos para realizar operaciones como la creación o la actualización de objetos, no se usarán los datos sin más, sino que hay que comprobar la validez de los datos en estructura y contenido.
    - Los serializadores nos permiten implementar validaciones sintácticas, así que implementaremos las mismas que definimos en el modelo de cara a la base de datos, pero esta vez serán aplicados de cara al *input* de las peticiones. Simplemente aplicaremos el serializador sobre el objeto JSON que nos llegue.
    - Además, en función del método HTTP podemos restringir los campos del JSON para que solo se actualizen, creen o lean los campos deseados.
- Cuando una entidad tenga relación con otra, como norma general en el JSON solo se escribirá el ID (que será su PK/FK en principio). Podrá haber alguna excepción con entidades auxiliares.
- Todos los nombres de los objetos del JSON se escribirán en snake_case.

#### Rutas
- Usaremos `urls.py`.
- Las llamadas a la API entran por aquí. Se relaciona una ruta base con su controlador correspondiente. Todas las rutas con esa ruta base serán redirigadas a ese controlador.


#### Controladores
- Usaremos `views.py`.
- Las llamadas a la API serán redirigadas a su controlador correspondiente. Aquí se definirán métodos que procesarán cada petición particular (método HTTP + ruta). En cada método se hará, en princpio, lo siguiente:
    1. Se autenticará la petición (roles y objetos solicitados válidos).
    2. Se validarán los datos de entrada y si hace falta, se hará algún cálculo o transformación mínima para adaptar los datos.
    3. Se llamará al servicio para que haga la lógica de negocio que corresponda.
    3. Se devolverá el resultado.
- En principio, no hay que tener mucho codigo en los métodos del controlador; el controlador recibe y devuelve la información, pero es el servicio el que se encarga del proceso interno.
- Vamos a usar nombres descriptivos y ser consistentes con ellos. E intentemos seguir el principio de la única responsabilidad (_single responsability_) para cada método. En vez de `get_by_name`, mejor `get_hotel_by_name`.
- Como norma general, un controlador por `views.py`.


#### Servicios
- Usaremos `services.py`.
- Los métodos de los controladores llamarán a los servicios para efectuar la lógica de negocio (realizar consultas, hacer transformaciones, borrar objetos, etc.). 
- Vamos a usar nombres descriptivos y ser consistentes con ellos. Y sigamos el principio de la única responsabilidad (_single responsability_) para cada método. En vez de `get_by_name`, mejor `get_hotel_by_name`.
- Lo más normal sería un solo servicio por `services.py`, pero en función de si tenemos alguna entidad auxiliar como ya se comentó, puede que tengamos algún otro servicio en el mismo archivo. Eso en el caso de servicios completamente enfocados a una entidad, pero también puede ser que tengamos un conjunto de operaciones particulares y relacionadas, para una cierta funcionalidad bastante bien diferenciada, que, aunque se base en una entidad, nos convenga separlo a un servicio aparto. Funcionalmente no hay diferencia alguna, pero es tan solo por tener las cosas ordenadas.


#### Pruebas
- Usaremos `/tests/test_models.py`, `/tests/test_serializers.py`,  `/tests/test_services.py` y `/tests/test_views.py`.
- En el primero probaremos los modelos; serán pruebas cortas y simples. Probaremos las validaciones más que nada. Probamos los valores más susceptibles a fallo solo y luego hacemos una instancia correcta.
- En el segundo probaremos los serializadores. Probaremos las validaciones, la restricción de campos según el método HTTP y la transformación de objeto Django a objeto JSON y viceversa.
- En el segundo probaremos los servicios; estudiaremos todas las funcionalidades en detalle. *Pruebas muy exhaustivas con mucha cobertura*.
- En el tercero probaremos todo el flujo desde el controlador; cada uno de sus métodos desde una perspectiva más global. *Pruebas muy exhaustivas con mucha cobertura*. 




<br><br><br>

## 2. Rutas y controladores

### 2.1. Métodos reservados del controlador
En el urls.py se relaciona una ruta base con un controlador del views.py. Cada controlador está representado por una clase, y cada clase tiene varios métodos para recibir las diferentes rutas a partir de esa ruta base.

Django Rest Framework (DRF) se reserva varios nombres de métodos del controlador para redirigir automáticamente ciertas rutas. Por ejemplo, si tenemos relacionada la ruta base `hotels` con el controlador de hoteles y definimos el método `list(self, request)` en el controlador de hoteles, cuando Django reciba la petición `GET api/hotels`, la redirigirá automáticamente al método list.

Aquí están los métodos reservados de DRF para el Default Router:

| Método en ViewSet                      | Método HTTP   | URL generada                      | URL name (para reverse) |
|----------------------------------------|---------------|-----------------------------------|-------------------------|
| list(self, request)                    | GET           | /hotels/ (lista todos)        | {basename}-list         |
| create(self, request)                  | POST          | /hotels/ (crear)              | {basename}-list         |
| retrieve(self, request, pk=None)       | GET           | /hotels/{id}/ (uno solo)      | {basename}-detail       |
| update(self, request, pk=None)         | PUT           | /hotels/{id}/ (editar)        | {basename}-detail       |
| partial_update(self, request, pk=None) | PATCH         | /hotels/{id}/ (editar parcial)| {basename}-detail       |
| destroy(self, request, pk=None)        | DELETE        | /hotels/{id}/ (borrar)        | {basename}-detail       |

Algunos comparten el mismo URL name simplemente porque comparten la ruta. Ya cuando se utilice esa ruta con un método HTTP se redirigirá al método que corresponda. La función `reverse` de Django lo que hace es darnos la URL completa a partir del nombre de una "vista", que sería lo que nosotros llamamos método de un controlador.


<br>

### 2.2. Métodos no resevados del controlador
Podemos definir nuevos métodos del controlador con nombres no reservados. Hay varias maneras, pero la más directa es añadiendo el decorador `@action` para especificar qué petición deseamos que se redirija al método. Indicamos el método HTTP y la ruta. En función del tipo de acción que necesitemos, construiremos la ruta de forma diferente. Por ejemplo:

#### Añadir _paths_
¿Queremos todas las ciudades? Tan solo necesitamos un nuevo _path_.
```python
    @action(detail=False, methods=['get'], url_path="cities")  # GET /hotels/cities
    def get_all_cities(self, request):
        ...
```

¿Queremos un atributo de un hotel, el nombre por ejemplo? Dejamos primero que filtre por id (detail=True) y luego añadimos un nuevo _path_ a la ruta.
```python
    @action(detail=True, methods=['get'], url_path="name")  # GET /hotels/{id}/name
    def get_name_by_hotel_id(self, request, pk=None):
        ...
```

#### _Path params_
¿Queremos un resumen de los hoteles de una ciudad (por decir algo)? Añadimos un nuevo _path_ a la ruta y recibimos un _path param_.
```python
    @action(detail=False, methods=['get'], url_path="city-summary/(?P<city>[\w\s-]+)")  # GET /hotels/city-summary/{city}
    def get_summary_by_city(self, request, city=None):
        ...
```

#### _Query params_
¿Queremos filtrar los hoteles según ciertos parámetros? Usamos _query params_.
```python
    @action(detail=False, methods=['get'])  # GET /hotels?name={name}&city={city}
    def filter_hotels(self, request):
        ...
```


<br>

### 2.3. Cuidado con los solapamientos
Mucho cuidado con los solapamientos de rutas, sobre todo con los _path params_. Vamos a ver un ejemplo. Si quisiéramos filtrar por nombre, utilizaríamos en principio un _query param_ `?name=nombre_que_sea`, pero vamos a poner un momento el ejemplo de que fuera con _path param_:

Queremos un método que nos busque un hotel por nombre. No es uno de los métodos reservados, así que crearemos uno nuevo. En principio uno puede pensar en usar la ruta `/hotels/{name}`, sin embargo, se está pisando con la ruta del método reservado 'retrieve': `/hotels/{id}`. Django, en principio, no nos dejaría tener ambas rutas a la vez porque no las diferenciaría. Habría que optar, por tanto, por una nueva ruta única, algo como `/hotels/name/{name}`:

```python
    @action(detail=False, methods=['get'], url_path="name/(?P<name>[^/.]+)")  # GET /hotels/name/{name}
    def get_hotel_by_name(self, request, name=None):
        ...
```
De nuevo, lo suyo sería un _query param_ en este caso.


<br>

### 2.4. URL names (reverse)
Utilizaremos el parámetro url_name del decorador `@action` para definir el URL name de cada método. Para darnos la URL completa, la función `reverse` de Django utilizará el siguiente patrón: `{basename}-{url_name}`.

Para reverse de ruta con _path params_, usamos `kwargs`:
```python
url = reverse('hotels-detail', kwargs={'pk': 1})  # Genera /hotels/1/
```

Para reverse de ruta con _query params_, los añadimos como cadena:
```python
url = reverse('hotels-filter_hotels')  # /hotels/filter_hotelss/
url_with_query_params = f"{url}?name=Ulises&city=Valencia" # /hotels/filter_hotelss/?name=Ulises&city=Valencia
```

Los URL names de los métodos reservados ya se han comentado.




<br><br>

## 3. Nomenclaturas métodos
Cada método se puede nombrear de veinte formas diferentes. Pero si tú dices get_prize_by_hotel ya no sabes si es el precio de un hotel, o un diccionario con el precio de cada hotel. Por tanto, no vamos a usar nunca By cuando hablemos de otra clase custom; reservaremos el By solo para atributos que no sean de clases custom. Para las clases custom usremos Of o For each, en función de si es para solo uno o para cada uno. Y así nos quitamosd de dudas si os parece.

### BY: encontrar un objeto o una colección de objetos dado un valor de uno de sus atributos que no es una clase custom
- General: `get_<object>_by_<attribute>`
- Ejemplo único: `get_hotel_by_name`
- Ejemplo colección: `get_hotels_by_city`

### OF: encontrar un objeto o una colección de objetos dado un valor de uno de sus atributos que sí es una clase custom
- General: `get_<object>_of_<custom_class>`
- Ejemplo único: `get_room_type_of_room`
- Ejemplos colección: `get_rooms_of_room_type, get_room_types_of_hotel`

### FOR EACH: encontrar un objeto o una colección de objetos para cada uno de las instancias de una clase custom (diccionario)
- General: `get_<object>_for_each_<instance_of_custom_class>`
- Ejemplo único: `get_prize_for_each_room_type`
- Ejemplo colección: `get_room_types_for_each_hotel`

PD: los métodos de los ejemplos no siguen este formato, así que no les echéis cuenta en ese sentido.




<br><br>

## 4. Foreign keys
En Django lo mejor no es cargar el objeto entero como en Java con el ORM de Hibernate. Es un poco diferente. Usamos `ForeignKey` que nos deja tanto el id como el objeto si queremos hacer la petición. Un resumen muy simplificado:

Definición:
```python
from django.db import models

class Hotel(models.Model):
    name = models.CharField(max_length=255)

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="rooms")
    number = models.IntegerField()
```

Uso:
```python
room = Room.objects.first()
hotel_id = room.hotel_id  # Acceso directo al ID (más eficiente)
hotel_obj = room.hotel    # Acceso al objeto completo (puede hacer query extra si no está en caché)
```




<br><br>

## 5. Enlaces de interés

Poned otros si queréis.

https://www.django-rest-framework.org/api-guide/viewsets/
https://www.django-rest-framework.org/api-guide/serializers/
https://www.django-rest-framework.org/api-guide/routers/
https://gokulnath-dev.medium.com/what-is-action-decorator-in-django-rest-framework-c371559c56d9

