

N.A. = No archivados
* = Comprobar bookings asociadas recientes y si sí, archivar en vez de borrar

Comprobar siempre que el usuario que hace la operación no esté archivado

Si nadie puede, poner un forbidden. No basta con quitarlo porque si lo he puesto es porque se crea por defecto aunque no lo pongamos.


ESTUDIAR LO DE SI SE LE PASA EL OWNER PK O NO

cambiar suyos y suyo por propio  .



## HotelOwner

| Método                        | Customer              | HotelOwner            | AppAdmin              |
|-------------------------------|-----------------------|-----------------------|-----------------------|
| list                          | --                    | --                    | Todos                 |
| retrieve                      | --                    | Él mismo              | Cualquiera            |
| create                        | --                    | --                    | --                    |
| update / partial update       | --                    | Él mismo              | --                    |
| destroy                       | --                    | Él mismo *            | --                    |
| delete all hotels of owner    | --                    | Él mismo, las N.A. *  | --                    |
| get current                   | --                    | Él mismo              | --                    |



## Hotel

| Método                        | Customer              | HotelOwner            | AppAdmin              |
|-------------------------------|-----------------------|-----------------------|-----------------------|
| list                          | Todos N.A.            | Todos N.A.            | Todos                 |
| retrieve                      | Cualquiera N.A.       | Cualquiera N.A.       | Cualquiera            |
| create                        | --                    | Nuevo                 | --                    |
| update / partial update       | --                    | Suyos N.A.            | --                    |
| destroy                       | --                    | Suyos N.A. *          | --                    |
| get all room types of hotel   | Cualquiera N.A.       | Cualquiera N.A.       | Cualquiera            |
| get total vacancy for each room type of hotel | Cualquiera N.A.    | Cualquiera N.A.           | Cualquiera            |



## RoomType

| Método                        | Customer              | HotelOwner            | AppAdmin              |
|-------------------------------|-----------------------|-----------------------|-----------------------|
| list                          | --                    | Todos N.A.            | Todos                 |
| retrieve                      | Cualquiera N.A.       | Cualquiera N.A.       | Cualquiera            |
| create                        | --                    | Nuevo                 | --                    |
| update / partial update       | --                    | Suyos N.A.            | --                    |
| destroy                       | --                    | Suyos N.A. *          | --                    |
| get total vacancy of room type| --                    | Suyos N.A.            | Cualquiera            |
| get all rooms of room type    | --                    | Suyos N.A.            | Cualquiera            |
| get vacancy for each room of room type | Cualquiera N.A.   | Cualquiera N.A.            | Cualquiera            |



## Room

| Método                        | Customer              | HotelOwner            | AppAdmin              |
|-------------------------------|-----------------------|-----------------------|-----------------------|
| list                          | --                    | --                    | Todos                 |
| retrieve                      | Cualquiera N.A.       | Cualquiera N.A.       | Cualquiera            |
| create                        | --                    | Nuevo                 | --                    |
| update / partial update       | --                    | Suyos N.A.            | --                    |
| destroy                       | --                    | Suyos N.A. *          | --                    |



## Customer

| Método                        | Customer              | HotelOwner            | AppAdmin              |
|-------------------------------|-----------------------|-----------------------|-----------------------|
| list                          | --                    | --                    | Todos                 |
| retrieve                      | Él mismo              | --                    | Cualquiera            |
| create                        | --                    | --                    | --                    |
| update / partial update       | Él mismo              | --                    | --                    |
| destroy                       | Él mismo *            | --                    | --                    |
| get current                   | Él mismo              | --                    | --                    |
| get bookings of customer      | Él mismo, los N.A.    | --                    | --                    |



## Bookings

| Método                        | Customer              | HotelOwner            | AppAdmin              |
|-------------------------------|-----------------------|-----------------------|-----------------------|
| list                          | --                    | --                    | Todos                 |
| retrieve                      | Suyos                 | --                    | Cualquiera            |
| create                        | --                    | --                    | --                    |
| update / partial update       | --                    | --                    | --                    |
| destroy                       | --                    | --                    | --                    |
| get bookings of customer      | Él mismo, las N.A.    | --                    | --                    |