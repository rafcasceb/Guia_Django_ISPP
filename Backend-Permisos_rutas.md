
## Notas
N.A. = No archivados

* = Comprobar bookings asociadas recientes y si sí, archivar en vez de borrar

Comprobar siempre que el usuario que hace la operación no esté archivado

Si nadie puede, poner un forbidden directamente en el controlador (no borrar el método).


ESTUDIAR LO DE SI SE LE PASA EL OWNER PK O NO




## HotelOwner

| Método                        | Customer              | HotelOwner            | AppAdmin              |
|-------------------------------|-----------------------|-----------------------|-----------------------|
| list                          | --                    | --                    | Todos                 |
| retrieve                      | --                    | Él mismo              | Todos                 |
| create                        | --                    | --                    | --                    |
| update / partial update       | --                    | Él mismo              | --                    |
| destroy                       | --                    | Él mismo *            | --                    |
| get all hotels of owner explicit | --                 | Él mismo, N.A.        | Todos                 |
| get all hotels of owner implicit | --                 | Él mismo, N.A.        | Todos                 |
| delete all hotels of owner explicit    | --           | Él mismo, N.A. *      | Todos                 |
| delete all hotels of owner explicit    | --           | Él mismo, N.A. *      | Todos                 |
| retrieve current              | --                    | Él mismo              | --                    |

El get all hotels of owner admin solo cambia la 


## Hotel

| Método                        | Customer              | HotelOwner            | AppAdmin              |
|-------------------------------|-----------------------|-----------------------|-----------------------|
| list                          | Todos N.A.            | Todos N.A.            | Todos                 |
| retrieve                      | Todos N.A.            | Todos N.A.            | Todos                 |
| create                        | --                    | Nuevo                 | --                    |
| update / partial update       | --                    | Propios N.A.          | --                    |
| destroy                       | --                    | Propios N.A.          | --                    |
| get all room types of hotel   | Todos N.A.            | Todos N.A.            | Todos                 |
| get total vacancy for each room type of hotel | Todos N.A.           | Todos N.A.                  | Todos                 |
| get bookings of hotel         | --                    | Propios N.A.          | Todos                 |



## RoomType

| Método                        | Customer              | HotelOwner            | AppAdmin              |
|-------------------------------|-----------------------|-----------------------|-----------------------|
| list                          | --                    | Todos N.A.            | Todos                 |
| retrieve                      | Todos N.A.            | Todos N.A.            | Todos                 |
| create                        | --                    | Nuevo                 | --                    |
| update / partial update       | --                    | Propios N.A.          | --                    |
| destroy                       | --                    | Propios N.A.  *       | --                    |
| get total vacancy of room type| --                    | Propios N.A.          | Todos                 |
| get all rooms of room type    | --                    | Propios N.A.          | Todos                 |
| get vacancy for each room of room type | Todos N.A.          | Todos N.A.                   | Todos                 |



## Room

| Método                        | Customer              | HotelOwner            | AppAdmin              |
|-------------------------------|-----------------------|-----------------------|-----------------------|
| list                          | --                    | --                    | Todos                 |
| retrieve                      | Todos N.A.            | Todos N.A.            | Todos                 |
| create                        | --                    | Nuevo                 | --                    |
| update / partial update       | --                    | PropiosN.A.           | --                    |
| destroy                       | --                    | PropiosN.A.  *        | --                    |



## Customer

| Método                        | Customer              | HotelOwner            | AppAdmin              |
|-------------------------------|-----------------------|-----------------------|-----------------------|
| list                          | --                    | --                    | Todos                 |
| retrieve                      | Él mismo              | --                    | Todos                 |
| create                        | --                    | --                    | --                    |
| update / partial update       | Él mismo              | --                    | --                    |
| destroy                       | Él mismo *            | --                    | --                    |
| get bookings of customer      | Él mismo, los N.A.    | --                    | Todos                 |
| get current                   | Él mismo              | --                    | --                    |



## Bookings

| Método                        | Customer              | HotelOwner            | AppAdmin              |
|-------------------------------|-----------------------|-----------------------|-----------------------|
| list                          | --                    | --                    | Todos                 |
| retrieve                      | Propios               | Propios               | Todos                 |
| create                        | --                    | --                    | --                    |
| update / partial update       | --                    | --                    | --                    |
| destroy                       | --                    | --                    | --                    |
| cancel booking                | --                    | --                    | Todos                 |



## AppAmdin

| Método                        | Customer              | HotelOwner            | AppAdmin              |
|-------------------------------|-----------------------|-----------------------|-----------------------|
| list                          | --                    | --                    | Todos                 |
| retrieve                      | --                    | --                    | Todos                 |
| create                        | --                    | --                    | --                    |
| update / partial update       | --                    | --                    | Él mismo              |
| destroy                       | --                    | --                    | Él mismo              |
| get current                   | --                    | --                    | Él mismo              |