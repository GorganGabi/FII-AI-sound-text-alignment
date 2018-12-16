

# FII-AI-sound-text-alignment

## Getting Started
Aceste instructiuni te vor ajuta sa pornesti serverul pe masina ta (windows/linux).

### Prerequisites

Pentru ca serverul sa mearga trebuie sa descarci si sa instalezi nodeJS de la link-ul: https://nodejs.org/en/.

### Usage
Pentru a porni aplicatia, trebuie deschis un terminal. Pentru acesta, trebuie navigat (fie din file explorer sau de la linia de comanda) in folderul unde este fisierul package.json (Server/package.json). In cazul pentru file explorer, odata ajuns in folderul respectiv, trebuie deschis un terminal (Windows: SHIFT+Click dreapta -> Open PowerShell window here).

Pentru a instala modulele se va introduce in terminal urmatoarea comanda:

```
npm install
```
Dupa ce se termina de instalat folderul Server ar trebui sa contina un folder cu numele node_modules.

In continuare, va trebui creat un fisier cu numele .env (poate fi creat dintr-un editor precum WebStorm/Sublime etc.) in care se vor introduce informatiile din .env.example.

Pentru a porni serverul trebuie introdus in terminal comanda:
```
npm run dev
```


In cazul erorii EADDRINUSE, se poate modifica usor portul de la care va rula serverul din fisierul .env creat precedent.

### Upload Setup

Form-ul pentru upload trebuie sa contina enctype="multipart/form-data".
Input-ul trebuie sa aiba numele "mySound".


```
  <form action="api/upload" method="post" enctype="multipart/form-data">
               <input type="file" name="mySound" />
        <input type='submit' value='Send'>
      </form>
```

End point-ul la care se gaseste controllerul de upload este: /api/upload.

Pagina principala se va gasi la adresa: http://localhost:8080/audio (atentie! serverul trebuie sa fie pornit) , care va randa fisierul
proiectIA.html (inclusiv css+js) din calea: /Interfata/proiectIA.html

### Documentatia
 Se gaseste in fisierul: Server/apidoc/index.html