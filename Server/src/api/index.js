import { Router } from 'express'
import * as uploadController from '../../Controllers/upload.controller.js'

const api = Router()

api.get('/', (req, res) => {
  res.send('<h1>API ROUTE</h1>')
})

/**
 * @api {post} /api/upload Speech recognition
 * @apiGroup Feedback
 * @apiParam {String} upload.text User's text
 * @apiParam {dataForm} mySound Input tag name
 * @apiParamExample {json} Input
 * "text": "Acesta este un text frumos!"
 * "mySound": sunet.mp3
 * @apiSuccessExample {json} Success
 *    HTTP/1.1 200 OK
 *    {
 *       "syncData":[{"end":0.29,"start":0.16,"word":"to","matched":0},
 *                  {"end":0.47,"start":0.3,"word":"the","matched":0},
 *                  {"end":0.64,"start":0.48,"word":"end","matched":0}]
 *    }
 * @apiErrorExample {json} Register error
 *    HTTP/1.1 500 Internal Server Error
 * @apiErrorExample {json} API Error
 *    HTTP/1.1 404 API not found
 */
api.post('/upload', uploadController.uploading)

export default api
