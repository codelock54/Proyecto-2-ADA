FROM  python:3.8

RUN apt-get update && apt-get install -y libgl1-mesa-glx libxkbcommon0 libegl1 libdbus-1-3 libxcb-xinerama0 libxcb-xkb1 libxcb-image0 libxcb-render0 libxcb-shm0 libxcb-keysyms1 libxcb-xtest0 
RUN  apt-get install -y libxcb-icccm4 libxcb-xfixes0 libxcb-util1 libfontconfig1
WORKDIR  /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#CMD [ "python", "main.py" ]

CMD ["sh", "-c", "export QT_QPA_PLATFORM=linuxfb && python main.py"]


