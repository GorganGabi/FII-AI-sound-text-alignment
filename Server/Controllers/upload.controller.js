const multer = require('multer')
const path = require('path')
const spawn = require("child_process").spawn
const config = require ("../src/config").default


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
      const error = {error: 'Fisierul nu s-a putut incarca...Extensie gresita. Uploadati din nou!'};
      get_sound_alignment_result(error, res)
    }
    else {
      const result = {upload: req.file}
      get_sound_alignment_result(result, res)
    }
  })
}

function get_sound_alignment_result(input, res) {
    // CALL PYTHON MODULE TO GET THE RESULT
    input = JSON.stringify(input)
    const pythonProcess = spawn("py", [config.sound_alignment_file_path, input])
    let response = "";

    pythonProcess.stdout.on("data", (data) => {
        response += data
    });
    pythonProcess.stdout.on("error", (err) => {
        res.json(err)
    });
    pythonProcess.stdout.on("end", () => {
        response = JSON.parse(response)
        res.json(response)
    });
}
