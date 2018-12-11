import { Router } from 'express'
import * as uploadController from '../../Controllers/upload.controller.js'

const api = Router()

api.get('/', (req, res) => {
  res.send('<h1>API ROUTE</h1>')
})

/**
 * @api {post} /api/upload Speech recognition
 * @apiGroup Feedback
 * @apiParam {String} text User's text
 * @apiParam {dataForm} mySound Input tag name
 * @apiParamExample {json} Input
 * "upload": {
 *       "fieldname": "mySound",
 *       "originalname": "ceva.mp3",
 *       "encoding": "7bit",
 *       "mimetype": "audio/mpeg",
 *       "destination": "./uploads",
 *       "filename": "mySound-1544533515623.mp3",
 *       "path": "uploads\\mySound-1544533515623.mp3",
 *       "size": 0
 *   }
 * @apiSuccessExample {json} Success
 *    HTTP/1.1 200 OK
 *    {
 *      "msg":"Success"
 *    }
 * @apiErrorExample {json} Register error
 *    HTTP/1.1 500 Internal Server Error
 * @apiErrorExample {json} API Error
 *    HTTP/1.1 404 API not found
 */
api.post('/upload', uploadController.uploading)

export default api
