## Identificación de algoritmos de hash

Para identificar a que algoritmo de hasheo corresponde cada archivo se utilizaron dos páginas web: https://www.tunnelsup.com/hash-analyzer/ y https://hashes.com/en/tools/hash_identifier . Para esto se verificó en dichas páginas ingresando una contraseña aleatoria de cada archivo, lo que permitió validar los algoritmos de hasheo.

* Archivo 1: MD5
 ![](./images/archivo1_hash.png)
* Archivo 2: MD5 plus salt
 ![](./images/archivo2_hash.png)
* Archivo 3: MD5 plus salt
 ![](./images/archivo3_hash.png)
* Archivo 4: NTLM
 ![](./images/archivo4_hash.png)
* * Archivo 5: sha512crypt
 ![](./images/archivo5_hash.png)


## Obtención de textos planos

Para obtener los textos planos de los archivos con contraseñas hasheadas se utilizó la siguiente función:

```python
Ingresar función para crackear las contraseñas
```

Dicha función recibe de entrada un arreglo de archivos a crackear, donde cada archivo es un diccionario que posee la ruta donde se encuentra ubicado el archivo (`path`), el código del algoritmo de hasheo para identificar en hashcat `mode` y el archivo de salida a utilizar (`output`).

Este algoritmo fue utilizado bajo una máquina virtual con las siguientes características:
* Sistema operativo: Ubuntu 18.04LTS
* Memoria: 4096 MB

Mientras que la máquina base posee las siguientes características:
* Sistema operativo: MacOS Catalina 10.15.6
* Procesador: 3,6 GHz Quad-Core Intel Core i3
* Memoria: 16 GB 2400 MHz DDR4
* Gráfica: AMD Radeon R9 280X 3 GB
* Disco duro: 

#### Resultados

Al ejecutar la función previa se obtuvieron los siguientes tiempos para crackear cada uno de los archivos y la cantidad total de hash que posee cada archivo y cuantos de estos se lograron crackear:

* Archivo 1:
  * Tiempo: 2,35 segundos
  * Hash totales: 1000
  * Hash crackeados: 1000
  ![](./images/crack_archivo1.png)
* Archivo 2:
  * Tiempo: 3,34 segundos
  * Hash totales: 1000
  * Hash crackeados: 1000
  ![](./images/crack_archivo2.png)
* Archivo 3:
  * Tiempo: 45.51 segundos
  * Hash totales: 1000
  * Hash crackeados: 1000
  ![](./images/crack_archivo3.png)
* Archivo 4:
  * Tiempo: 2,34 segundos
  * Hash totales: 1000
  * Hash crackeados: 1000
 ![](./images/crack_archivo4.png)
* Archivo 5:
  * Tiempo: 
  * Hash totales: 20
  * Hash crackeados:
 ![](./images/crack_archivo5.png)

#### Diferencias

Hash - Explica el porqué un algoritmo se demora más en obtener el texto claro que otro
Explica detalladamente la diferencia entre el tiempo que toma crackear cada archivo, y para cuál de todos los archivos cree que se usó un algoritmo más seguro y porqué

## Re-cifrado

Para volver a cifrar las contraseñas se utilizará el algoritmo `Bcrypt` por las siguientes razones:

* Salt: El que este algoritmo haga uso de `salt` permite siempre generar distintos cifrados para la misma contraseña.
* Lentitud: Bcrypt fue ideado para ser un algoritmo lento, lo que dificulta los ataques por fuerza bruta, al contrario de lo que podría ser un algoritmo de la familia SHA-2, que son diseñados para ser rápidos facilitando así estos ataques.

En primera instancia se utilizó la función `create_file()` para generar un archivo único con las 4020 contraseñas en texto plano:

```python
Función create_file()
```

![](./images/passwords-textoplano.png)

Luego, para realizar este re-cifrado se programó la siguiente función:

```python
Código de re-hasheo
```

La que, tras ser ejecutada, llevó un tiempo de 284.88 segundos en completar la operación.

![](./images/rehash.png)

Estas contraseñas se encuentras en el archivo `passwords_bcrypt.txt` el cual contiene las 4020 contraseñas encriptadas utilizando el algoritmo `Bcrypt`.

![](./images/rehashed_passwords.png)

## Cifrado asimétrico

Se implementó el algoritmo de cifrado asimétrico RSA.

El primer paso de este algoritmo es generar la llave pública y privada, proceso el cual se compone de diversos pasos:

1. Seleccionar dos números primos `p` y `q`. Para tener fuertes llaves públicas y privadas se recomienda utilizar números primos muy largos.
2. Computar `n`, que es el resultado de multiplicar `p` con `q`. `n = p * q`
3. Computar `λ(n)` que corresponde a la función de Charmichael. `λ(n) = (p – 1) * (q – 1) λ(n)`
4. Computar la llave de encriptación (`e`), que corresponde a un número tal que el máximo común divisor entre `e` y `λ(n)` sea 1, es decir, que `e` y `λ(n)` sean coprimos.
5. Computar la llave de desencriptado (`d`) que corresponde al inverso multiplicativo modular de `e` y se obtiene utilizando el algoritmo extendido de Euclides (`d ≡ e^(− 1) (mod λ(n))`). 

```python
Insertar código
```

## Solicitud de llaves

Para el proceso de solicitud de llaves se utilizó una conexión por sockets entre dos archivos, para esto el script `crack_files.py` actuará como cliente, conectándose vía socket al script `rsa.py` que actua como servidor.

```python
Código cliente
```

```python
Código servidor
```

## Cifrado de hashes utilizando RSA

Se utilizó la siguiente función en el archivo cliente que permite cifrar los hashes en Bcrypt pero ahora aplicándoles RSA.

```python
Código de cifrado
```

Este algoritmo opera con la llave pública y el `n` que se obtienen vía socket del archivo servidor, donde una vez cifrados mediante RSA se envía el archivo con las 4020 contraseñas hasheadas al servidor mediante la siguiente función:

```python
Función de envío de archivo desde el cliente
```

Una vez enviado este archivo se finaliza el proceso del cliente.

En el servidor se cuenta con la función `receive_file()` que es la encarga de procesar el recibimiento del archivo con contraseñas desde el cliente para ser guardadas en el archivo `ser-rsa_passwords.txt` para posteriormente ser desencriptadas, utilizando la llave privada y el n, mediante la función `decrypt_file()`.

```python
Función receive_file()
```

```python
Función decrypt_file()
```

## Almacenamiento en SQLite

Finalmente, las contraseñas en encriptación Bcrypt se almacenan desde el servidor en una base de datos SQLite.
