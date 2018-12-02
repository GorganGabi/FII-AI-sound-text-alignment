import {Router} from 'express'

const api = Router()

api.get('/', (req, res) => {
    res.send('<h1>API ROUTE</h1>')
});

export default api

