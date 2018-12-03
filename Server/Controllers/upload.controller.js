const multer = require('multer')
const path = require('path')

module.exports.uploading = (req, res) => {

  const storage = multer.diskStorage({
    destination: './uploads',
    filename: function (req, file, cb) {
      cb(null, file.fieldname + '-' + Date.now() + path.extname(file.originalname))
    }
  })

  function checkFileType (file, cb) {
    const filetypes = /mp3|wav/
    const extname = filetypes.test(path.extname(file.originalname).toLowerCase())
    let mimetype
    (file.mimetype === 'audio/mpeg' || file.mimetype === 'audio/wav') ? mimetype = true : mimetype = false
    if (mimetype && extname) {
      return cb(null, true)
    } else {
      cb('Eroare: Doar imagini!')
    }
  }

  const upload = multer({
    storage: storage,
    fileFilter: function (req, file, cb) {
      checkFileType(file, cb)
    }
  }).single('mySound')

  upload(req, res, (err) => {
    if (err) {
      res.json({error: 'Fisierul nu s-a putut incarca...Extensie gresita. Uploadati din nou!'})
    }
    else
      res.json({upload: req.file})
  })
}