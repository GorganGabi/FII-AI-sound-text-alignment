import { Router } from 'express'
import * as uploadController from '../../Controllers/upload.controller.js'

const api = Router()

api.get('/', (req, res) => {
  res.send('<h1>API ROUTE</h1>')
})

api.post('/upload', uploadController.uploading)

export default api
