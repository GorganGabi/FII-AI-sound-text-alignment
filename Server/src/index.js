import 'babel-polyfill'
import http from 'http'
import path from 'path'
import express from 'express'
import helmet from 'helmet'
import bodyParser from 'body-parser'
import api from './api'
import config from './config'

require('dotenv').config();
let app = express();
app.server = http.createServer(app);

// pentru a avea access la req.body unde vom putea pune informatii
app.use(bodyParser.urlencoded({extended: true}));
app.use(bodyParser.json());
app.use(express.json());

// ofera servicii pentru securitate
app.use(helmet());

// static files
app.use(express.static('public'));

app.use('/api', api);

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname + '/public/index.html'))
});

app.server.listen(8080, () => {
    console.log(`Started on port 8080(${config.env})`)
});

export default app
