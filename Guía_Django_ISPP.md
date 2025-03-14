# Guía de Django para ISPP



1. [Introducción](#1-datos-fundamentales-del-equipo)  
2. [Instalación, preparación y ejecución](#2-instalación-preparación-y-ejecución)
    - [2.1. Instalación de repositorio y BD](#21-instalación-de-repositorio-y-bd)
    - [2.2. Ejecución general](#22-ejecución-general)
    - [2.3. *Imports*](#23-imports)
    - [2.4. Migraciones](#24-migraciones)
    - [2.5. Ejecutar tests](#25-ejecutar-tests)
3. [Estructura](#3-estructura)
    - [3.1. Estructura de carpetas](#31-estructura-de-carpetas)
    - [3.2. Funcionalidades y flujo de información](#32-funcionalidades-y-flujo-de-información)
4. [Comentarios sobre modelos](#4-comentarios-sobre-modelos)
    - [4.1. Atributos](#41-atributos)
    - [4.2. Validaciones BD](#42-validaciones-bd)
    - [4.3. Usuarios](#43-usuarios)
5. [Validación y autorización](#5-validación-y-autorización)
    - [Validaciones semánticas vs validaciones sintácticas](#51-validaciones-semánticas-vs-validaciones-sintácticas)
    - [Validaciones del modelo](#52-validaciones-del-modelo)
    - [Validaciones del serializador](#53-validaciones-del-serializador)
    - [Validaciones del servicio](#54-validaciones-del-servicio)
    - [Autorización](#55-autorización)
6. [Permisos de roles](#6-permisos-de-roles)
7. [Archivado](#7-archivado)
8. [Serializadores](#8-serializadores)
    - [8.1. Serializar input](#81-serializar-input)
    - [8.2. Validar serializador](#82-validar-serializador)
    - [8.3. Ejecutar acción](#83-ejecutar-acción)
    - [8.4. Serializar output](#84-serializar-output)
    - [8.5. Serializar foreign keys](#85-serializar-foreign-keys)
9. [Rutas](#9-rutas)
    - [9.1. Métodos reservados del controlador](#91-métodos-reservados-del-controlador)
    - [9.2. Métodos no reservados del controlador](#92-métodos-no-resevados-del-controlador)
    - [9.3. Cuidado con los solapamientos](#93-cuidado-con-los-solapamientos)
    - [URL names (reverse)](#94-url-names-reverse)
10. [Controladores y servicios](#10-controladores-y-servicios)
    - [10.1. Estructura general de un método de un controlador](#101-estructura-general-de-un-método-de-un-controlador)
    - [10.2. Nomenclaturas métodos](#102-nomenclaturas-métodos)
    - [10.3. Estructura de request](#103-estructura-de-request)
    - [10.4. Respuestas y excepciones](#104-respuestas-y-excepciones)
11. [Tests](#11-tests)
    - [Comentarios generales](#111-comentarios-generales)
    - [Tipos de creación de objetos](#112-tipos-de-creación-de-objetos)
12. [Otros](#12-otros)
    - [Seeders](#121-seeders)
    - [Sesión y tokens](#122-sesión-y-tokens)
    - [Pre-commit](#123-pre-commit)
13. [Enlaces de interés](#13-enlaces-de-interés)






<br><br><br>

## 1. Introducción

Esto es una guía que he hecho para que todos más o menos sigamos los mismos criterios básicos en cuanto de la estructura de los archivos y las rutas de la API. No soy para nada experto en Django. He echado un buen rato para estudiar cuáles eran las mejores opciones y creo el sistema que propongo ha quedado bastante lógico y robusto, pero cualquiera que tenga otra propuesta de lo que sea, que lo diga. Si preferís meter las URLS a mano en el urls.py en vez de usar el Django Rest Framework (DRF), decidlo; ambos tienen sus ventajas e inconvenientes. Si cualquiera de las cosas que haya dicho por aquí os parece una tontería o simplemente innecesario, decidlo también. Ni se os ocurra callaros.

El enlace al repositorio con algunos ejemplos: https://github.com/rafcasceb/Guia_Django_ISPP. Fijaos en cómo hacer la estructuras de las carpetas y los métodos, pero desde entonces hemos cambiado algunas cosas como el formato de las rutas por ejemplo. EJEMPLOS ALGO ANTICUADOS.






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

Se pueden hacer migraciones de paquetes en particulares, pero es más cómodo situarse en el directorio `\backend` y hacerlo para todos a la vez. Es importante mencionar que para que esto funcione, los paquetes deben contar ya con el subpaquete `migrations`, que tiene que tener también una carpeta `__init__.py`. Así que si son nuevos, hay que añadirlos a mano (vacíos).

Para crear los archivos de las migraciones:
```bash
python manage.py makemigrations
```

Para aplicar las migraciones a la base de datos una vez que tenemos los archivos de las migraciones:
```bash
python manage.py migrate
```

Sería raro, pero se podría dar que haya habido cambios grandes en las migraciones y no se pueda migrar directamente. Lo solución más normal es borrar la base de datos manualmente (en Heidi, DBeaver o lo que sea), crearla una nueva (mismo nombre, claro) y migrar de nuevo. Debería funcionar.


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
python manage.py test pawtel.<APP_NAME>.tests.<TEST_FILE_NAME>.<CLASS_NAME>.<METHOD_NAME>
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
- Define un formato de objeto JSON y transforma una instancia de entidad en un objeto JSON y viceversa.
- Transforman las instancias de las entidades a un objeto JSON.
- Transforman otros objetos JSON al formato del JSON
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

## 4. Comentarios sobre modelos

### 4.1. Atributos
Los atributos de texto (strings) serán definidos con el atributo de Django `CharField`, no con `TextField`. Tienen sus diferencias, pero para nuestros requisitos, el primero nos vale mejor.

Sobre las *foreign keys*, en Django lo mejor no es cargar el objeto entero como en Java con el ORM de Hibernate. Es un poco diferente: usamos `models.ForeignKey`.

Por ejemplo:
```python
class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="rooms")
    number = models.IntegerField()
```

En principio, podemos usar tanto el id como el objeto (el objeto seguro, pero lo de el id directamente hay que comprobarlo muy bien porque puede que no funcione).
```python
room = Room.objects.first()
hotel_id = room.hotel_id  # Acceso directo al ID (más eficiente, si es que funciona)
hotel_obj = room.hotel    # Acceso al objeto completo (puede hacer query extra si no está en caché)
```

### 4.2. Validaciones BD
Otro aspecto a tener en cuenta es las validaciones y persistencias de las instancias de los modelos. Hay que diferenciar entre los métodos `clean()`, `full_clean()` `save()`.

Como ya se ha comentado, las validacinoes de los modelos se aplican de cara a la base de datos, no en la creación de instancias en Django. Sin embargo, con `save()` no basta, sino que hay que usar `full_clean()` antes para probar las validaciones.

| Método        | Valida Campos | Ejecuta `clean()` Personalizado | Verifica Unicidad | Guarda en BD |
|---------------|---------------|---------------------------------|-------------------|--------------|
| `full_clean()` | ✅ Sí        | ✅ Sí                          | ✅ Sí           | ❌ No       |
| `clean()`     | ❌ No        | ✅ Sí                          | ❌ No           | ❌ No       |
| `save()`      | ❌ No (a menos que se sobrescriba) | ❌ No (a menos que se sobrescriba) | ❌ No (a menos que se sobrescriba) | ✅ Sí |


### 4.3. Usuarios

Los usuarios se implementarán mediante un `AppUser`. Esta entidad está configurada para que Django la considere la entidad base de usuarios, por lo que los registros ser harán con esta entidad.

A la vez, tenemos tres tipos diferentes de usuarios que representan roles diferentes: `Admin`, `HotelOwner` y `Customer`. Cada uno de estos estará asociado a un `AppUser`.






<br><br><br>

## 5. Validación y autorización

### 5.1. Validaciones semánticas vs validaciones sintácticas

Las validaciones sintácticas verifican que los datos cumplen con el formato correcto, como la longitud de un campo, el tipo de dato o la estructura esperada (por ejemplo, el formato de un número de teléfono).

Las validaciones semánticas, en cambio, verifican el significado y la coherencia de los datos dentro del contexto de la aplicación, que sean lógicos y útiles dentro del sistema. Por ejemplo, asegurarse de que una fecha de reserva no sea en el pasado, que una edad ingresada sea mayor a 18 si el usuario debe ser adulto, que un nombre de usuario no contenga palabras prohibidas, o que un usuario no tenga más de cierto número de elementos. 


<br>

### 5.2. Validaciones del modelo
Los modelos de Django implementa **validaciones semánticas**. Se aplican para la base de datos. Es necesario por si entrasen datos por fuera de la API.

Podrían aplicar validaciones sintácticas pero no se ha considerado necesario.


<br>

### 5.3. Validaciones del serializador
Los serializadores implementan **validaciones semánticas**. Junto a los servicios completan las validaciones en la capa del servicio.

Podrían aplicar validaciones sintácticas pero por separación de responsabilidades y facilidad de uso, se cederá a los servicios.

Implementan las mismas validaciones que los modelos, pero cuidado con la sintáxis que es un poco diferente. Junto a las validacoines, definen si los campos son legibles o modificables en función de la petición HTTP. Ya se verá más adelante.


<br>

### 5.4. Validaciones del servicio
Los servicios implementan **validaciones sintácticas**. Junto a los serializadores completan las validaciones en la capa del servicio.

En función de la ruta de la petición a la API, se realizarán diferentes validaciones.

Puesto que los servicios serán usados casi exclusivamente por los controladores de la API, no se ha considerado necesario validar cada vez todos los argumentos en cada función, sino que solo se valian al principio del método del controlador, y dentro de los métodos del servicio se asume que son correctos y existen. Por ejemplo, en el `update_room` no hace falta comprobar si existe o no la *primary key* que se le pasa como argumento, o si tiene asociado un RoomType y éste a su vez un Hotel y demás. Se asume que en los pasos previos de la autorización y la validación se ha comprobado esto, y el método de *update* tan solo hará *retrieve* del objeto y lo devolverá.

Se hablará de las excepciones y las respuestas más adelante.


<br>

### 5.5. Autorización
El primer paso de la mayoría de métodos de los controladores (en el futuro espero que todos) es autorizar la petición, que es diferente a la validación que se hará en pasos posteriores.

La autorización, comprueba que se tengan los permisos para realizar la opción que se pide.
 - El usuario que realiza la operación está autenticado
 - El usuario que realiza la operación tiene el rol necesario para la operación en concreto.
 - Los objetos de la operación existen.
 - El usuario que realiza la operación tiene potestad sobre esos objetos (por ejemplo, un dueño de hotel solo puede modificar sus hoteles).

La validación se encarga de los cambios que va a realizar la operación, comprobando el contenido de los datos y las consecuencias en el sistema.






<br><br><br>

## 6. Permisos de roles
	 is staff and is superuser por defecto false
Los usuarios que tenemos y cómo implementar roles






<br><br><br>

## 7. Archivado

### Definición de funcionalidad de archivado
...

Los usuarios usarán `is_active`. Cuidado, porque significa lo opuesto: is_active -> not is_archived.

### Implementación de funcionalidad de archivado
Cómo hacer el archivado en el futuro (tengo ejemplos)





<br><br><br>

# 8. Serializadores
Recordamos que valen para transformar una instancia de una entidad en un JSON y viceversa, y además permite validar semánticamente los valores.

## 8.1. Serializar input
Las peticiones POST, PUT y PATCH envían un JSON con datos. Para validarlos y tratarlos, aplicaremos el serializador sobre estos datos.

En función de la petición, habrá campos requeridos, campos permitidos y campos no permitidos. Por ejemplo, por norma general los POST deben incluir prácticamente todos los campos, salvo el ID que no debe procesarse; los PUT tienen que incluir todos los campos editables; y los PATCH pueden incluir cualquier campo editable, sin tener que estar todos.

Para esto se ha creado la clase `BaseSerializer`, la cual será extendida por todos los serializadores, y permite definir de forma muy sencilla estas restricciones. Ya no hace falta definir manualmente en cada atributo si está requerido o no, sino con unas listas.

```python
class RoomSerializer(BaseSerializer):

    fields_required_for_post = ["name", "room_type"]
    fields_editable = ["name"]
    fields_not_readable = []

    class Meta:
        # Serializer definition...
```

Para que funcione esta lógica que depende del método HTTP, hay que pasarle el contexto de la petición al serializador (lo envolvemos en un diccionario con `context = {"request": request}`).

En caso de *update*, también hay que pasarle la instancia actual para mantener los datos no incluidos en la petición.

Por ejemplo:
```python
@staticmethod
def serialize_input_room_update(request, pk):
    room = RoomService.retrieve_room(pk)
    context = {"request": request}
    serializer = RoomSerializer(instance=room, data=request.data, context=context)
    return serializer
```


<br>

## 8.2. Validar serializador
Para validar el contenido del serializador, hay que usar el método `is_valid()`. 

Por ejemplo:
```python
@staticmethod
def validate_update_room(pk, input_serializer):
    if not input_serializer.is_valid():
        raise ValidationError(input_serializer.errors)

    # Sintactic validations...
```

Como dato, el serializador directamente valida que las foreign keys existan en la base de datos. Sin embargo, no puede comprobar validaiones semánticas como que el objeto de la foreign key pertenezca al usuario en cuestión. Eso habría que comprobarlo a mano como las demás validaciones restantes.


<br>

## 8.3. Ejecutar acción
Después de validar, crearemos o actualizaremos las entidades usando directamente los serializadores, sin tener que sacar los datos manualmente, o siquiera sacar la instancia.

Por ejemplo:
```python
@staticmethod
def create_room(input_serializer):
    room_created = input_serializer.save()
    return room_created
```

```python
@staticmethod
def update_room(pk, input_serializer):
    room = RoomService.retrieve_room(pk)
    return input_serializer.update(room, input_serializer.validated_data)
```

Para otras peticiones que no traigan datos en la petición y no haga falta usar serializadores para éstos, ya se llevará la acción de la forma que toque.


<br>

## 8.4. Serializar output
La mayoría de las rutas devuelven los objetos principales involucrados en la operación. Simplemente se aplica el serializador sobre la instancia. Se indicará si son varias instancias o una sola.

Por ejemplo:
```python
@staticmethod
def serialize_output_room(room, many=False):
    return RoomSerializer(room, many=many).data
```


<br>

## 8.5. Serializar *foreign keys*
Como norma general, en las *foreign keys* no se serializará la entidad entera, sino solo su ID.

La única excepcón de momento son los roles, los cuales llevarán anidados su `AppUser` al completo, por comodidad.





<br><br><br>

## 9. Rutas

### 9.1. Métodos reservados del controlador
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

(Importante la "/" al final.)

Algunos comparten el mismo URL name simplemente porque comparten la ruta. Ya cuando se utilice esa ruta con un método HTTP se redirigirá al método que corresponda. La función `reverse` de Django lo que hace es darnos la URL completa a partir del nombre de una "vista", que sería lo que nosotros llamamos método de un controlador.


<br>

### 9.2. Métodos no resevados del controlador
Podemos definir nuevos métodos del controlador con nombres no reservados. Hay varias maneras, pero la más directa es añadiendo el decorador `@action` para especificar qué petición deseamos que se redirija al método. Indicamos el método HTTP y la ruta. En función del tipo de acción que necesitemos, construiremos la ruta de forma diferente. Por ejemplo (casos no realistas de la aplicación):

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

#### _Query params_
¿Queremos filtrar los hoteles según ciertos parámetros? Usamos _query params_. Vienen en la *request*.
```python
@action(detail=False, methods=['get'])  # GET /hotels?name={name}&city={city}
def filter_hotels(self, request):
    ...
```
O podemos ponerlo en el método `list` en función del caso:
```python
def list(self, request):
    filters = request.query_params.dict()  # URL filters checked
    ...
```

#### _Path params_ (menos común)
¿Queremos un resumen de los hoteles de una ciudad (por decir algo)? Añadimos un nuevo _path_ a la ruta y recibimos un _path param_ para indicar el nombre. Aunque suele ser mejor filtrar por *query params*.
```python
@action(detail=False, methods=['get'], url_path="city-summary/(?P<city>[\w\s-]+)")  # GET /hotels/city-summary/{city}
def get_summary_by_city(self, request, city=None):
    ...
```


<br>

### 9.3. Cuidado con los solapamientos
Mucho cuidado con los solapamientos de rutas, sobre todo con los _path params_. Vamos a ver un ejemplo. Si quisiéramos filtrar por nombre, utilizaríamos en principio un _query param_ `?name=nombre_que_sea`, pero vamos a poner un momento el ejemplo de que fuera con _path param_:

Queremos un método que nos busque un hotel por nombre. No es uno de los métodos reservados, así que crearemos uno nuevo. En principio uno puede pensar en usar la ruta `/hotels/{name}`, sin embargo, se está pisando con la ruta del método reservado 'retrieve': `/hotels/{id}`. Django, en principio, no nos dejaría tener ambas rutas a la vez porque no las diferenciaría. Habría que optar, por tanto, por una nueva ruta única, algo como `/hotels/name/{name}`:

```python
@action(detail=False, methods=['get'], url_path="name/(?P<name>[^/.]+)")  # GET /hotels/name/{name}
def get_hotel_by_name(self, request, name=None):
    ...
```
De nuevo, lo suyo sería un _query param_ en este caso.


<br>

### 9.4. URL names (reverse)
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






<br><br><br>


## 10. Controladores y servicios

### 10.1. Estructura general de un método de un controlador
Se intentará ceder toda la lógica de negocio a los servicios, manteniendo los controladores bastante concisos, encargándose simplemente de llamar en cada paso al método del servicio correspondiente. Por la lógica ya explicada en la sección 3.2, La estructura genérica por norma del proceso de un *endpoint* es la siguiente:
1. Authorize
2. Serialize input
3. Validate
4. Perform
5. Serialize output
6. Return

Por supuesto, endpoints como los de `retrieve` o `list` no necesitan los pasos 2 y 3. O el `delete` no necesita 2, 3, ni 4. Se puede añadir algún paso adicional si la casuística particular del caso en cuestión lo necesita.

Un ejemplo sería el siguiente:

```python
def update(self, request, pk=None):
    RoomService.authorize_action_room(request, pk)
    input_serializer = RoomService.serialize_input_room_update(request, pk)
    RoomService.validate_update_room(pk, input_serializer)
    room_updated = RoomService.update_room(pk, input_serializer)
    output_serializer_data = RoomService.serialize_output_room(room_updated)
    return Response(output_serializer_data, status=status.HTTP_200_OK)
```

Lo servicios se encargarán del resto, de forma muy organizada. Se recomienda poner algunos comentarios para separar los métodos de las clases de los servicios según las peticiones HTTP para los que valen. Puede haber sección de generales u otros.


<br>

### 10.2. Nomenclaturas métodos
Pensar luego mejor para cada caso y en función de si es controlador o servicio.

Cada método se puede nombrear de veinte formas diferentes. Pero si tú dices get_prize_by_hotel ya puede que no sepas si es el precio de un hotel, o un diccionario con el precio de cada hotel. Por tanto, no vamos a usar nunca By cuando hablemos de otra clase custom; reservaremos el By solo para atributos que no sean de clases custom. Para las clases custom usremos Of o For each, en función de si es para solo uno o para cada uno. Y así nos quitamos de dudas si os parece.

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

Aparte, no vale poner `list()`y listo, sino que hay que ser un poco más descriptivo, como `list_hotels()`, no hace falta tan solo complicarse. Pero que indique el nombre. En principio, que cada método de los servicios sean únicos en nombre.


<br>
    
### 10.3. Estructura de request
Importante recalcar que para acceder a sus objetos hay que usar puntos ".", NO acceder como un diccionario con "[]" o "get()".

| Método                    | Descripción  |
|---------------------------|--------------|
| **request.data**          | Contains parsed data from the request body (useful for POST, PUT, PATCH).|
| **request.query_params**  | Holds URL query parameters (e.g., ?key=value).|
| **request.method**        | The HTTP method (e.g., "GET", "POST", "PUT").|
| **request.user**          | The authenticated user making the request.|
| **request.auth**          | Authentication details.|
| **request.headers**       | A dictionary-like object of request headers.|


<br>

### 10.4. Respuestas y excepciones

Para las respuestas de los métodos de los controladores usaremos por defecto `Response`, con el status de `rest_framework`, en vez de puesto a mano. Esto solo se hace en los controladores.

```python
from rest_framework import status #, viewsets
from rest_framework.response import Response

def retrieve(self, request, pk=None):
    ...
    return Response(output_serializer_data, status=status.HTTP_200_OK)

def create(self, request):
    ...
    return Response(output_serializer_data, status=status.HTTP_201_CREATED)

def destroy(self, request, pk=None):
    ...
    return Response(status=status.HTTP_204_NO_CONTENT)
```

En los servicios se podrán lanzar excepciones. Sin embargo, no las pondremos igual que las respuestas, "tan a mano" por así decirlo. Usaremos las excepciones de rest_framework.exceptions, en principio. Internamente, ya nos devuelven una Response con el status adecuado, por lo que son prácticamente equivalentes. Por ejemplo:

```python
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError

@staticmethod
def validate_create_room(input_serializer):
    if not input_serializer.is_valid():
        raise ValidationError(input_serializer.errors)

    ...

    if room_type.is_archived:
        raise ValidationError({"room_type": "Invalid room type."})

    if name and Room.objects.filter(room_type__hotel_id=hotel_id, name=name).exists():
        raise ValidationError({"name": "Name in use by same hotel."})
```

PD: ValidationError se puede importar de varios sitios. Hay que estudiar las diferencias.

No se hará `return`, sino `raise`. Django Rest Framework ya las recoje y las procesa como tiene que ser.

Si por algún motivo hiciese falta escribir a mano la respueta de un error, se escribiría `{"detail": ...}`. En el caso de una respueta correcta (casi imposible), usaríamos `{"message": ...}`.







<br><br><br>

## 11. Tests

### 11.1. Comentarios generales
Tests bien hechos. Con cobertura, que funcionen como tienen que funcionar y que prueben cosas de verdad; ese es el fundamento.

No usamos `pytest`, sino el sistema de testeo propio de Django. En la sección 2.5 podemos ver cómo ejecutar los tests.

Podemos hacer un método `setUp` con objetos o acciones que se harán antes de cada test.

También podemos usar `subTest` para parametrizar múltiples tests a la vez. Especialmente últiles para rangos de variables en modelos. Por ejemplo:
```python
def test_create_room_invalid_name(self):
    invalid_names = ["", None, "A" * 51]

    for name in invalid_names:
        with self.subTest(name=name):
            room = Room(name=name, room_type=self.room_type)
            with self.assertRaises(ValidationError):
                room.full_clean()
```

En la inmensa mayoría de tests de controladores (views) nos tenemos que autenticar. Para ello, podemos definir en el setup (salvo excecpiones) un usuario y forzar la autenticación con él. El método para esto último sería:

```python
self.client.force_authenticate(user=self.app_user)  # siendo app_user el usuario AppUser previamente definido (no el usuario de rol)
```
Importante autenticarse con el usuario de AppUser, no con el de rol como podría ser su HotelOwner.

Se pueden usar herramientas externas cómodas y útiles como Postman. Hay que tener en cuenta el uso de tokens. En la sección 12.2 se habla más de ellos. Se deja un conjunto de consultas de Postman en el Microsoft Teams, para que el quiera probar que no tenga que partir de cero.


<br>

### 11.2. Tipos de creación de objetos
En los tests solemos tener que crear objetos. Hay tres maneras fáciles que yo sepa ahora, pero hay que tener cuidado con no confundirlas, porque funcionan un poco diferentes y utilizan nomenclaturas diferentes.

#### A nivel de BD
Todo lo que tenga la expresión `<NOMBRE_ENTIDAD>.objects` está relacionado a la base de datos. Usa, como podemos ver con `hotel_owner_id`, el nombre de los atributos en la BD. Ya nos lo guarda en la base de datos.

```python
self.hotel = Hotel.objects.create(
    name=...,
    address=...,
    hotel_owner_id=...,
)
```

#### A nivel de Python solo
La creación normal en Django. Como podemos ver con `hotel_owner`, usa el nombre de los atributos en Django. Pero no está guardado en la base de datos. Para eso simplemente hacemos `full_clean()` y `save()` como ya hemos visto.

```python
self.hotel_model = Hotel(
    name=...,
    address=...,
    hotel_owner=...,
    ...
)
```

#### En JSON
Creamos el JSON a mano. No hay más magia. Tendremos que usar luego el serializador. Por tanto, tenemos que usar los nombres de los atributos de Django, como podemos ver con `hotel_owner`.

Esto digamos que es lo que se hace desde el frontend (creo), o al menos lo que le llega a la API y con lo que se puede probar en Postman.

```python
self.valid_data = {
    "name": ...,
    "address": ...,
    "hotel_owner": ...,
    ...
}
```






<br><br><bR>

## 12. Otros

### 12.1. Seeders
Los seeders al ejecutarse rellenan la base de datos con ejemplos. Si hacemos el comando base, los seeds se añaden a los datos anteriores. Si se quiere borrar todos los datos guardados se usa la versión *clean*.

Los comandos son los siguientes:
```bash
python manage.py seed
python manage.py seed --clean
```


<br>

### 12.2. Sesión y tokens
El inicio de sesión funciona mediante el uso de tokens (una cadena larga de caracteres). Un token es un identificador único de un usuario, durante el tiempo de vida del token (10 mins) y se ha de incluir en las peticiones a la API para poder autenticarse (y ver su autorización). Al iniciar sesión se otorga un token nuevo. También existen tokens de refresco con mayor tiempo de vida (2 días) para solicitar un token nuevo.

| Operación | URL | Cuerpo | Token | Descripción |
|-----------|-----|--------|-------|-------------|
| Registro | http://localhost:8000/auth/register/ | Datos del usuario para el POST | - | Crea el usuario del rol indicado en la BD, sin iniciar sesión |
| Inicio de sesión | http://localhost:8000/auth/login/ | Username y password | Token normal | Inicia sesión y devuelve un token nuevo y un token para refresco |
| Refrescar token | http://localhost:8000/auth/token/refresh/ | - | Token de refresco | Genera un nuevo token para el usuario asociado al token de refresco |
| Información del usuario | http://localhost:8000/auth/user-info/ | - | Token normal | Los datos del usuario |

En Postman se pone el token en la pestaña de Authorization, como Bearer Token. Se puede poner como variable para no tener que estar cambiándolo en todas las peticiones.


<br>

### 12.3. Pre-commit
Hay un pre-commit que comprueba los commits antes de confimarlos y revisa y unifica ciertos aspectos, especialmente visuales.

A veces una parte del pre-commit llamada `black` falla. Haremos lo siguiente:
- Ejecutar comando `black .`, para ejecutarlo a mano.
- Nos saltamos el precommit como último recurso: `git commit --no-verify -m "..." -m "..."`.






<br><br><br>

## 13. Enlaces de interés

Poned otros si queréis.

https://www.django-rest-framework.org/api-guide/viewsets/
https://www.django-rest-framework.org/api-guide/serializers/
https://www.django-rest-framework.org/api-guide/routers/
https://gokulnath-dev.medium.com/what-is-action-decorator-in-django-rest-framework-c371559c56d9

