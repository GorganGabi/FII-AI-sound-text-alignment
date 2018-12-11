import 'babel-polyfill'
import http from 'http'
import path from 'path'
import express from 'express'
import helmet from 'helmet'
import bodyParser from 'body-parser'
import api from './api'
import {config} from './config'
import {getRootPath} from '../helpers/parser'

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
let root;
getRootPath(process.cwd(), (res) => {
    root = res
});

app.use(express.static(path.join(root.toString(), 'Interfata/')))

app.use('/api', api);

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname + '/public/index.html'))
});
app.get('/audio', (req, res) => {
    res.sendFile(path.join(root.toString(), 'Interfata/proiectIA.html'))
});

app.server.listen(config.port, () => {
    console.log(`Started on port ${config.port}(${config.env})`)
});

export default app
