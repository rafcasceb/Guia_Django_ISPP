# Guía de Django para ISPP

Esto es una guía que he hecho para que todos más o menos sigamos los mismos criterios básicos en cuanto de la estructura de los archivos y las rutas de la API. No soy para nada experto en Django. He echado un buen rato para estudiar cuáles eran las mejores opciones y creo el sistema que propongo ha quedado bastante lógico y robusto, pero cualquiera que tenga otra propuesta de lo que sea, que lo diga. Si preferís meter las URLS a mano en el urls.py en vez de usar el Django Rest Framework (DRF), decidlo; ambos tienen sus ventajas e inconvenientes. Si cualquiera de las cosas que haya dicho por aquí os parece una tontería o simplemente innecesario, decidlo también. Ni se os ocurra callaros.



<br><br>

## 1. Estructura y flujo de información
### 1.1. Paquetes
Haremos un paquete por concepto. Lo más normal es que cada entidad represente un concepto, sin embargo, en función de su relevancia y uso, ciertas entidades pueden pertenecer a otros paquetes que no sean suyos propios. A lo mejor necesitamos una entidad auxiliar que no va a recibir ninguna consulta, sino que es por definir con más comodidad un atributo de una entidad principal. No vamos a trabajar prácticamente nunca con la entidad auxiliar sino con la principal. En ese caso, pueden estar en el mismo paquete.


### 1.2. Entidades
Usaremos `models.py`.

Definiremos las entidades necesarias dentro.


###  1.3. Serializadores
Usaremos `serializers.py`.

Las llamadas a la API desde el frontend no devolverán tal cual los objetos (las instancias de las entidades), sino que los transformaremos a objetos JSON para que sea más cómodo trabajar con ellos. **TODOS los nombres de los objetos del JSON se escribirán en snake_case**. 


###  1.4. Rutas
Usaremos `urls.py`.

Las llamadas a la API entran por aquí. Se relaciona una ruta base con su controlador correspondiente. Todas las rutas con esa ruta base serán redirigadas a ese controlador.


###  1.5. Controladores
Usaremos `views.py`.

Las llamadas a la API serán redirigadas a su controlador correspondiente. Aquí se definirán métodos que procesarán cada petición particular (método HTTP + ruta). En cada método se hará, en princpio, lo siguiente:
 1. Una validación de los datos de entrada y si hace falta, algún cálculo o transformación mínima para adaptar los datos.
 2. Se llamará al servicio para que haga la lógica de negocio que corresponda.
 3. Se devolverá el resultado usando el serializador.

En principio, no hay que tener mucho codigo en los métodos del controlador; el controlador recibe y devuelve la información, pero es el servicio el que se encarga de todo el proceso interno.

Vamos a usar nombres descriptivos y ser consistentes con ellos. Y sigamos el principio de la única responsabilidad (_single responsability_) para cada método. En vez de `get_by_name`, mejor `get_hotel_by_name`.

Como norma general, un controlador por `views.py`.


###  1.6. Servicios
Usaremos `services.py`.

Los métodos de los controladores llamarán a los servicios para efectuar la lógica de negocio (realizar consultas, hacer transformaciones, borrar objetos, etc.). 

Vamos a usar nombres descriptivos y ser consistentes con ellos. Y sigamos el principio de la única responsabilidad (_single responsability_) para cada método. En vez de `get_by_name`, mejor `get_hotel_by_name`.

Lo más normal sería un solo servicio por `services.py`, pero en función de si tenemos alguna entidad auxiliar como ya se comentó, puede que tengamos algún otro servicio en el mismo archivo. Eso en el caso de servicios completamente enfocados a una entidad, pero también puede ser que tengamos un conjunto de operaciones particulares y relacionadas, para una cierta funcionalidad bastante bien diferenciada, que, aunque se base en una entidad, nos convenga separlo a un servicio aparto. Funcionalmente no hay diferencia alguna, pero es tan solo por tener las cosas ordenadas.


### 1.7. Pruebas
Usaremos `/tests/test_models`, `/tests/test_service.py` y `/tests/test_views.py`.

En el primero probaremos los modelos; serán pruebas cortas y simples. En el segundo probaremos los servicios; estudiaremos todas las funcionalidades en detalle. En el tercero probaremos todo el flujo desde el controlador; cada uno de sus métodos desde una perspectiva más global. *Pruebas muy exhaustivas con mucha cobertura*. 

Estas son unas directrices muy vagas y los ejemplos muy básicos. Cualquiera que proponga usar algunas estrategias más completas y mejores, por supuesto que bienvenido sea. Es más, espero que se os ocurran mejores cosas una vez que empezemos a usar Pytest y estas tecnologías, aunque si no, está bien. Con cosas nuevas me refiero a algunas anotaciones, algún otro método de _fixture_ previo o cualquier cosa, o incluso cambiar la estrategia general de las pruebas del servicio y el controlador como las he definido.




<br><br>

## 2. Rutas y controladores

### 2.1. Métodos reservados del controlador
En el urls.py se relaciona una ruta base con un controlador del views.py. Cada controlador está representado por una clase, y cada clase tiene varios métodos para recibir las diferentes rutas a partir de esa ruta base.

Django Rest Framework (DRF) se reserva varios nombres de métodos del controlador para redirigir automáticamente ciertas rutas. Por ejemplo, si tenemos relacionada la ruta base `hotels` con el controlador de hoteles y definimos el método `list(self, request)` en el controlador de hoteles, cuando Django reciba la petición `GET api/hotels`, la redirigirá automáticamente al método list.

Aquí están los métodos reservados de DRF para el Default Router:

| Método en ViewSet                      | Método HTTP   | URL generada                      | URL name (para reverse) |
|----------------------------------------|---------------|-----------------------------------|-------------------------|
| list(self, request)                    | GET           | /api/hotels/ (lista todos)        | {basename}-list         |
| create(self, request)                  | POST          | /api/hotels/ (crear)              | {basename}-list         |
| retrieve(self, request, pk=None)       | GET           | /api/hotels/{id}/ (uno solo)      | {basename}-detail       |
| update(self, request, pk=None)         | PUT           | /api/hotels/{id}/ (editar)        | {basename}-detail       |
| partial_update(self, request, pk=None) | PATCH         | /api/hotels/{id}/ (editar parcial)| {basename}-detail       |
| destroy(self, request, pk=None)        | DELETE        | /api/hotels/{id}/ (borrar)        | {basename}-detail       |

Algunos comparten el mismo URL name simplemente porque comparten la ruta. Ya cuando se utilice esa ruta con un método HTTP se redirigirá al método que corresponda. La función `reverse` de Django lo que hace es darnos la URL completa a partir del nombre de una "vista", que sería lo que nosotros llamamos método de un controlador.


<br>

### 2.2. Métodos no resevados del controlador
Podemos definir nuevos métodos del controlador con nombres no reservados. Hay varias maneras, pero la más directa es añadiendo el decorador `@action` para especificar qué petición deseamos que se redirija al método. Indicamos el método HTTP y la ruta. En función del tipo de acción que necesitemos, construiremos la ruta de forma diferente. Por ejemplo:

#### Añadir _paths_
¿Queremos todas las ciudades? Tan solo necesitamos un nuevo _path_.
```python
    @action(detail=False, methods=['get'], url_path="cities")  # GET /api/hotels/cities
    def get_all_cities(self, request):
        ...
```

¿Queremos un atributo de un hotel, el nombre por ejemplo? Dejamos primero que filtre por id (detail=True) y luego añadimos un nuevo _path_ a la ruta.
```python
    @action(detail=True, methods=['get'], url_path="name")  # GET /api/hotels/{id}/name
    def get_name_by_hotel_id(self, request, pk=None):
        ...
```

#### _Path params_
¿Queremos un resumen de los hoteles de una ciudad (por decir algo)? Añadimos un nuevo _path_ a la ruta y recibimos un _path param_.
```python
    @action(detail=False, methods=['get'], url_path="city-summary/(?P<city>[\w\s-]+)")  # GET /api/hotels/city-summary/{city}
    def get_summary_by_city(self, request, city=None):
        ...
```

#### _Query params_
¿Queremos filtrar los hoteles según ciertos parámetros? Usamos _query params_.
```python
    @action(detail=False, methods=['get'])  # GET /api/hotels?name={name}&city={city}
    def filter_hotels(self, request):
        ...
```


<br>

### 2.3. Cuidado con los solapamientos
Mucho cuidado con los solapamientos de rutas, sobre todo con los _path params_. Vamos a ver un ejemplo. Si quisiéramos filtrar por nombre, utilizaríamos en principio un _query param_ `?name=nombre_que_sea`, pero vamos a poner un momento el ejemplo de que fuera con _path param_:

Queremos un método que nos busque un hotel por nombre. No es uno de los métodos reservados, así que crearemos uno nuevo. En principio uno puede pensar en usar la ruta `/api/hotels/{name}`, sin embargo, se está pisando con la ruta del método reservado 'retrieve': `/api/hotels/{id}`. Django, en principio, no nos dejaría tener ambas rutas a la vez porque no las diferenciaría. Habría que optar, por tanto, por una nueva ruta única, algo como `/api/hotels/name/{name}`:

```python
    @action(detail=False, methods=['get'], url_path="name/(?P<name>[^/.]+)")  # GET /api/hotels/name/{name}
    def get_hotel_by_name(self, request, name=None):
        ...
```
De nuevo, lo suyo sería un _query param_ en este caso.


<br>

### 2.4. URL names (reverse)
Utilizaremos el parámetro url_name del decorador `@action` para definir el URL name de cada método. Para darnos la URL completa, la función `reverse` de Django utilizará el siguiente patrón: `{basename}-{url_name}`.

Para reverse de ruta con _path params_, usamos `kwargs`:
```python
url = reverse('hotels-detail', kwargs={'pk': 1})  # Genera /api/hotels/1/
```

Para reverse de ruta con _query params_, los añadimos como cadena:
```python
url = reverse('hotels-filter_hotels')  # /api/hotels/filter_hotelss/
url_with_query_params = f"{url}?name=Ulises&city=Valencia" # /api/hotels/filter_hotelss/?name=Ulises&city=Valencia
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

## 4. Enlaces de interés

Poned otros si queréis.

https://www.django-rest-framework.org/api-guide/viewsets/
https://www.django-rest-framework.org/api-guide/routers/
https://gokulnath-dev.medium.com/what-is-action-decorator-in-django-rest-framework-c371559c56d9