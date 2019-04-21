# A-2019-backend

## Overview
* The App server will send an url of the image to the backend using JSON format.
* The backend will download this image on the server and call the **color** recognition part to get the color result of this image.
* The backend will use this color result to match the good facts in our kb, 
and see if there is good matching color, and if there exists matching color, then we try to find whether there 
exists such cloth that has this color. If not, then we just randomly recommend the clothes to the user based on 
the contraints we have in our kb.
