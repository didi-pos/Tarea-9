<div align="center">
<h1>Tarea 9</h1>
  <p>
    Ingeniería Electrónica · Universidad Santo Tomás
    <br>
    <b>Didier Posse</b>
    <br>
    <em>Primer punto</em>
  </p>
</div>

<hr>

<div align="center">
  <h2>Creación de la Simulación</h2>
</div>

<ol>
  <li><br>
    <div align="center">
      <p><img width=850 src="https://github.com/user-attachments/assets/27b3e581-30dd-45b9-94c1-e08aee71777d"/></p>
    </div>
    <p>
      Primero se ingresa a la carpeta donde uno tiene el entorno virtual de python, ya que asi es como podremos ejecutar las simulaciones para saber que realmente estan funcionando para después Dockerizarlas.
      Después creamos los archivos Python (.py) donde se va a colocar el código de las simulaciones, ahora si se ingresa al entorno virtual con <code>source &lt;nombre_entorno_virtual&gt;/bin/activate</code>.
      Luego de ingresar al entorno virtual, se ejecutan las simulaciones con <code>python &lt;nombre_archivo_simulación&gt;</code>, y deberia cargar sin problemas.
      Recordar que se requiere tener instalado pybullet en el entorno virtual, yo ya lo tenia instalado y es necesario para archivos que usen esta libreria (como la del brazo_robotico.py).
    </p>
  </li>
  <li><br>
    <div align="center">
      <p><img width=850 src="https://github.com/user-attachments/assets/8720c7de-c89f-4f75-aa13-680e8e3d07e3"/></p>
      <p><img width=850 src="https://github.com/user-attachments/assets/a3a13d49-b32b-4156-a884-3ffb8009107e"/></p>
    </div>
    <p>
      Aqui se muestra el código que las dos simulaciones, teniendo en cuenta que para que se pueda mostrar con un entorno gráfico tanto en el entorno virtual como cuando se Dockerice, seria colocar esta linea:
      <code>physicsClient = p.connect(p.GUI)</code> con <code>(p.GUI)</code> y no con <code>(p.DIRECT)</code>, de resto el código normal con sus librerias que puede contener pybullet o ktinker para ejecutarlos.
    </p>
  </li>
  <li><br>
    <div align="center">
      <p><img width=850 src="https://github.com/user-attachments/assets/8202d40d-bff9-4767-a8cb-0401cc8cbb40"/></p>
      <p><img width=850 src="https://github.com/user-attachments/assets/ead77629-7ee3-41a1-877d-0c13b7fbfc2a"/></p>
      <p><img width=850 src="https://github.com/user-attachments/assets/135181a3-cbad-40e9-b541-5493cfaaf3e9"/></p>
    </div>
    <p>
      Estas serian las simulaciones ya ejecutandose exitosamente y cumpliendo con las funciones que queremos, ya estaria listo para Dockerizarlas.
    </p>
  </li>
</ol>

<hr>

<div align="center">
  <p><em>Segundo Punto</em></p>
</div>

<hr>

<div align="center">
  <h2>Dockerizar las Simulaciones</h2>
</div>

<h2>Primera Simulación</h2>
<ol>
  <li><br>
    <div align="center">
      <p><img width=850 src="https://github.com/user-attachments/assets/53a3aafe-fe69-4120-b8fe-d7dfdd288af8"/></p>
    </div>
    <p>
      Para empezar la Dockerización, se requiere una carpeta donde se va a colocar todos los archivos necesarios para el proceso y entre estos claramente debe estar el archivo de la simulación.
      Después de crear esa carpeta, se crea un archivo Texto (.txt) que se llamara requirements.txt donde se va a colocar las librerias que se colocaron el archivo de la simulación que se requieren
      simular como lo es pybullet, también numpy es una que requiere instalación, las demás que usamos vienen ya con la instalación de python.
      Luego se mueve el archivo de la simulación (.py) a la carpeta que se creó.
      Después se crea un archivo sin extensión que lo llamaremos Dockerfile, practicamente este es un archivo se va a ejecutar el código que contenga como los archivos (.bash), pero en docker, donde
      será capaz de configurar todos esos archivos para crear la imagen del archivo con todas sus dependencias necesarias.
      Luego se ejecuta este comando <code>xhost +local:docker</code> para permitir las conexiones X11, que son necesarias para mostrar el entorno gráfico cuando se ejecute el contenedor.
      Finalmente se construye la imagen con <code>docker build -t &lt;nombre_de_la_imagen&gt; .</code>
    </p>
  </li>
  <li><br>
    <div align="center">
      <p><img width=850 src="https://github.com/user-attachments/assets/3806ac2e-1eb3-47d3-80a9-50c20c41f0c4"/></p>
    </div>
    <p>
      Aqui se muestra el archivo "Dockerfile" donde muestra los comandos que se usaron para configurarlo y que se requiere instalar unas cosas, crear la carpeta en docker y agregar el archivo en esta,
      aquí muestro la funcion exacta de los comandos que se usaron para este archivo:
      <ul>
        <li><code>FROM python:3.11-slim</code> → Define la imagen base de Python (ligera y optimizada).</li>
        <li><code>LABEL maintainer="..."</code> → Agrega una etiqueta con la información del creador del contenedor.</li>
        <li><code>RUN apt-get update ...</code> → Instala las dependencias necesarias para que la imagen soporte PyBullet y la salida gráfica (OpenGL y librerías del sistema). Al final se limpia la caché para reducir el tamaño de la              imagen.</li>
        <li><code>WORKDIR /brazo_robotico</code> → Define la carpeta de trabajo dentro del contenedor donde se colocarán los archivos.</li>
        <li><code>COPY requirements.txt .</code> → Copia el archivo con las dependencias Python dentro del contenedor.</li>
        <li><code>RUN pip install --no-cache-dir -r requirements.txt</code> → Instala las dependencias Python sin guardar caché de pip.</li>
        <li><code>COPY brazo_robotico.py .</code> → Copia el script principal de la simulación al contenedor.</li>
        <li><code>ENV DISPLAY=:0</code> → Configura la variable de entorno para X11 (para mostrar GUI cuando se ejecute con las opciones de docker run adecuadas).</li>
        <li><code>CMD ["python", "brazo_robotico.py"]</code> → Comando por defecto que arranca la simulación al iniciar el contenedor.</li>
      </ul>
    </p>
  </li>
  <li><br>
    <div align="center">
      <p><img width=850 src="https://github.com/user-attachments/assets/11b67d57-a727-4cb1-b5e6-cbef639bb2e8"/></p>
    </div>
    <p>
      Por último se ejecuta el contenedor con la imagen creada, con el comando <code>docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --device /dev/dri &lt;nombre_de_la_imagen&gt;</code>.
      Es necesario colocarlo así para que se puedaa ejecutar la simulación con un entorno gráfico.
    </p>
  </li>
  <li><br>
    <div align="center">
      <p><img width=850 src="https://github.com/user-attachments/assets/d837d3d6-8e2f-4487-81ee-ceee47c82297"/></p>
    </div>
    <p>
      Aqui ya se muestra la simulación ejecutandose con entorno gráfico como un contenedor.
    </p>
  </li>
</ol>

<h2>Segunda Simulación</h2>
<ol>
  <li><br>
    <div align="center">
      <p><img width=850 src="https://github.com/user-attachments/assets/5a46a058-00a0-481d-86f2-e911bfec4905"/></p>
    </div>
    <p>
      Igual a la primera simulación, se hace el mismo proceso de crear la carpeta e ingresar a ella, después al crear el archivo requirements.txt ahí si cambia un poco.
      El contenido de este archivo es vacío ya que no se requiere instalar librerias de la simulación a parte como toca con pybullet y con numpy, ya que tkinter ya viene
      preinstalada cuando se instala python, asi que ese archivo se coloca vacío.
      Eso era lo único diferente porque después también toca mover el archivo de la simulación (.py) a la carpeta, crear el "Dockerfile" de la misma manera y contruir de
      la misma forma la imagen que contiene el archivo de la simulación (.py) con sus dependencias.
    </p>
  </li>
  <li><br>
    <div align="center">
      <p><img width=850 src="https://github.com/user-attachments/assets/ab2ae835-48d2-4e78-8f4d-62a8bf1fd262"/></p>
    </div>
    <p>
      Aquí se muestra el archivo "Dockerfile" el cual es el mismo proceso que el anterior, aunque hay que tener en cuenta que a pesar que no tengamos que descargar la libreria
      tkinter en el archivo "requirements.txt", si se requiere instalarlo como dependencia del sistema, se pondria en el <code>RUN</code> como <code>tk-dev</code>, de resto es igual.
    </p>
  </li>
  <li><br>
    <div align="center">
      <p><img width=850 src="https://github.com/user-attachments/assets/48a2ea10-45fc-4c92-97a3-bb76a301dc1d"/></p>
    </div>
    <p>
      Ahora si se pondria el comando para que se ejecute o arranque el contenedor de la simulación con un entorno gráfico.
    </p>
  </li>
  <li><br>
    <div align="center">
      <p><img width=850 src="https://github.com/user-attachments/assets/64db1708-c373-4d49-a759-508be14ae1be"/></p>
      <p><img width=850 src="https://github.com/user-attachments/assets/f7d0fe9c-d738-4b05-86e1-0e1414410431"/></p>
    </div>
    <p>
      Aqui se evidencia como se ejecutó y cumple con las funciones de la simulación correctamente.
    </p>
  </li>
</ol>
