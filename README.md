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
      Primero, se ingresa a la carpeta donde se tiene el <b>entorno virtual de Python</b>, ya que así es como podremos ejecutar las simulaciones para comprobar que realmente están funcionando antes de Dockerizarlas. 
      Luego, se crean los archivos <b>Python (.py)</b> donde se colocará el código de las simulaciones. 
      <br><br>
      Una vez listos, se ingresa al entorno virtual con el comando <code>source &lt;nombre_entorno_virtual&gt;/bin/activate</code>. 
      Después de activarlo, se ejecutan las simulaciones con <code>python &lt;nombre_archivo_simulación&gt;</code>, y si todo está correcto, deberían cargarse sin problemas. 
      <br><br>
      Es importante tener instalada la librería <b>PyBullet</b> dentro del entorno virtual, ya que es necesaria para los archivos que la utilizan (como el <i>brazo_robotico.py</i>).
    </p>
  </li>

  <li><br>
    <div align="center">
      <p><img width=850 src="https://github.com/user-attachments/assets/8720c7de-c89f-4f75-aa13-680e8e3d07e3"/></p>
      <p><img width=850 src="https://github.com/user-attachments/assets/a3a13d49-b32b-4156-a884-3ffb8009107e"/></p>
    </div>
    <p>
      Aquí se muestra el código de las dos simulaciones. Es importante tener en cuenta que, para que puedan mostrarse con un entorno gráfico tanto en el entorno virtual como cuando se Dockericen, 
      se debe colocar la línea <code>physicsClient = p.connect(p.GUI)</code> en lugar de <code>p.connect(p.DIRECT)</code>. 
      <br><br>
      El resto del código se mantiene igual, con sus respectivas librerías, ya sea <b>PyBullet</b> o <b>Tkinter</b>, dependiendo de la simulación.
    </p>
  </li>

  <li><br>
    <div align="center">
      <p><img width=850 src="https://github.com/user-attachments/assets/8202d40d-bff9-4767-a8cb-0401cc8cbb40"/></p>
      <p><img width=850 src="https://github.com/user-attachments/assets/ead77629-7ee3-41a1-877d-0c13b7fbfc2a"/></p>
      <p><img width=850 src="https://github.com/user-attachments/assets/135181a3-cbad-40e9-b541-5493cfaaf3e9"/></p>
    </div>
    <p>
      Estas son las simulaciones ejecutándose exitosamente en <b>PyBullet</b>, que es el motor encargado de correr simulaciones, juegos y aplicaciones interactivas. 
      <br><br>
      Gracias a esto, podemos verificar que las simulaciones funcionan correctamente y cumplen con las funciones que queremos. 
      Una vez comprobado, ya estarían listas para ser <b>Dockerizadas</b>.
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
      Para comenzar la <b>Dockerización</b>, se necesita crear una carpeta donde se colocarán todos los archivos necesarios para el proceso. Entre estos debe estar el archivo principal de la simulación. 
      <br><br>
      Dentro de esta carpeta se crea un archivo de texto llamado <b>requirements.txt</b>, donde se listan las librerías utilizadas en la simulación que deben instalarse, como <code>pybullet</code> o <code>numpy</code>. 
      Las demás librerías vienen incluidas con la instalación de Python. 
      <br><br>
      Luego, se mueve el archivo de simulación (<b>.py</b>) a la carpeta creada, y se genera un archivo sin extensión llamado <b>Dockerfile</b>. Este archivo contiene el código que se ejecutará en el proceso de construcción de la imagen, 
      muy parecido a un script de <i>bash</i>, pero adaptado para Docker. 
      <br><br>
      Antes de construir la imagen, se ejecuta el comando <code>xhost +local:docker</code> para permitir las conexiones X11 necesarias para mostrar el entorno gráfico. Finalmente, se construye la imagen con 
      <code>docker build -t &lt;nombre_de_la_imagen&gt; .</code>.
    </p>
  </li>

  <li><br>
    <div align="center">
      <p><img width=850 src="https://github.com/user-attachments/assets/3806ac2e-1eb3-47d3-80a9-50c20c41f0c4"/></p>
    </div>
    <p>
      Aquí se muestra el archivo <b>Dockerfile</b>, donde se pueden ver los comandos utilizados para configurarlo. A continuación, se detalla la función de cada línea:
      <ul>
        <li><code>FROM python:3.11-slim</code> → Define la imagen base de Python (ligera y optimizada).</li>
        <li><code>LABEL maintainer="..."</code> → Agrega una etiqueta con la información del creador del contenedor.</li>
        <li><code>RUN apt-get update ...</code> → Instala las dependencias necesarias para que la imagen soporte PyBullet y la salida gráfica (OpenGL y librerías del sistema). Al final, limpia la caché para reducir el tamaño de la imagen.</li>
        <li><code>WORKDIR /brazo_robotico</code> → Define la carpeta de trabajo dentro del contenedor donde se colocarán los archivos.</li>
        <li><code>COPY requirements.txt .</code> → Copia el archivo con las dependencias dentro del contenedor.</li>
        <li><code>RUN pip install --no-cache-dir -r requirements.txt</code> → Instala las dependencias de Python sin guardar caché.</li>
        <li><code>COPY brazo_robotico.py .</code> → Copia el script principal de la simulación al contenedor.</li>
        <li><code>ENV DISPLAY=:0</code> → Configura la variable de entorno X11 para habilitar la interfaz gráfica.</li>
        <li><code>CMD ["python", "brazo_robotico.py"]</code> → Comando por defecto que inicia la simulación al ejecutar el contenedor.</li>
      </ul>
    </p>
  </li>

  <li><br>
    <div align="center">
      <p><img width=850 src="https://github.com/user-attachments/assets/11b67d57-a727-4cb1-b5e6-cbef639bb2e8"/></p>
    </div>
    <p>
      Finalmente, se ejecuta el contenedor usando el comando:<br>
      <code>docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --device /dev/dri &lt;nombre_de_la_imagen&gt;</code>.
      <br><br>
      Este comando permite que la simulación se ejecute con su <b>entorno gráfico</b> habilitado correctamente.
    </p>
  </li>

  <li><br>
    <div align="center">
      <p><img width=850 src="https://github.com/user-attachments/assets/d837d3d6-8e2f-4487-81ee-ceee47c82297"/></p>
    </div>
    <p>
      Aquí ya se muestra la simulación corriendo con <b>entorno gráfico</b> dentro de un contenedor, utilizando <b>PyBullet</b> como motor principal.
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
      Igual que en la primera simulación, se crea la carpeta y se ingresa en ella. Sin embargo, en este caso, el archivo <b>requirements.txt</b> se deja vacío, 
      ya que no se requiere instalar librerías adicionales. 
      <br><br>
      La librería <b>Tkinter</b> ya viene preinstalada con Python, por lo tanto, no es necesario incluirla ahí. 
      Luego se mueve el archivo de la simulación (.py), se crea el <b>Dockerfile</b> y se construye la imagen de la misma manera que antes.
    </p>
  </li>

  <li><br>
    <div align="center">
      <p><img width=850 src="https://github.com/user-attachments/assets/ab2ae835-48d2-4e78-8f4d-62a8bf1fd262"/></p>
    </div>
    <p>
      Este es el archivo <b>Dockerfile</b>, que sigue el mismo proceso que el anterior. 
      Sin embargo, aunque no sea necesario incluir <b>Tkinter</b> en el <code>requirements.txt</code>, 
      sí se debe instalar como dependencia del sistema en el <code>RUN</code> mediante <code>tk-dev</code>.
    </p>
  </li>

  <li><br>
    <div align="center">
      <p><img width=850 src="https://github.com/user-attachments/assets/48a2ea10-45fc-4c92-97a3-bb76a301dc1d"/></p>
    </div>
    <p>
      Una vez configurado todo, se ejecuta el contenedor de la simulación con el comando correspondiente para que se abra el <b>entorno gráfico</b> correctamente.
    </p>
  </li>

  <li><br>
    <div align="center">
      <p><img width=850 src="https://github.com/user-attachments/assets/64db1708-c373-4d49-a759-508be14ae1be"/></p>
      <p><img width=850 src="https://github.com/user-attachments/assets/f7d0fe9c-d738-4b05-86e1-0e1414410431"/></p>
    </div>
    <p>
      Finalmente, se observa cómo la simulación se ejecuta correctamente dentro del contenedor, mostrando su interfaz gráfica mediante <b>Tkinter</b>. 
      <br><br>
      Este tipo de simulación se basa más en la visualización y la interacción directa, 
      por lo que utiliza menos comandos en consola y se centra en la parte gráfica.
    </p>
  </li>
</ol>
