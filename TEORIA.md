# Parte E — Teoría del segundo parcial

**Materia:** Manejo Masivo de Datos (Big Data)  
**Matrícula:** 125054864

### 1. Diferencias entre los modos de Hadoop

En modo standalone, Hadoop se ejecuta en una sola máquina y utiliza el sistema de archivos local. En modo pseudo-distribuido, sus componentes funcionan como procesos independientes en un mismo equipo, simulando un clúster. En modo totalmente distribuido, los servicios se ejecutan en varias máquinas conectadas. HDFS se utiliza normalmente en los modos pseudo-distribuido y totalmente distribuido.

### 2. ¿Por qué utilizar volúmenes en lugar de COPY?

Los volúmenes permiten utilizar archivos grandes sin incorporarlos a la imagen Docker, evitando aumentar innecesariamente su tamaño. También facilitan actualizar el dataset sin reconstruir la imagen. En nuestro proyecto montamos el CSV en modo de solo lectura, protegiendo los datos originales mientras Hadoop los procesa.

### 3. Diferencias entre docker compose down y down -v

`docker compose down` elimina los contenedores y las redes creadas por Compose, pero conserva los volúmenes nombrados. Por eso nuestros 28 resultados permanecieron en PostgreSQL después de reiniciar los servicios. En cambio, `docker compose down -v` también elimina los volúmenes administrados por Compose y, con ellos, los datos almacenados.

### 4. ¿Por qué MapReduce no siempre es más rápido?

MapReduce necesita inicializar tareas, distribuir datos, ordenarlos y realizar la reducción, lo que genera sobrecarga. En nuestra prueba, Hadoop tardó 27.515 segundos, mientras que Python secuencial tardó 18.348 segundos. MapReduce suele resultar más conveniente cuando los datos son suficientemente grandes y pueden procesarse en paralelo utilizando varios nodos.

### 5. Diferencias entre CMD, ENTRYPOINT, COPY y ADD

`CMD` establece un comando o argumentos predeterminados que pueden reemplazarse al iniciar un contenedor. `ENTRYPOINT` define el ejecutable principal y normalmente permite agregarle argumentos. `COPY` copia archivos y carpetas a la imagen, mientras que `ADD` incorpora funciones adicionales, como extraer archivos TAR locales y obtener contenido desde determinadas fuentes.
