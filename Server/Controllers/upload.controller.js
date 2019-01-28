import { getRootPath } from '../helpers/parser'

const multer = require('multer');
const path = require('path');
const spawn = require('child_process').spawn;
const config = require('../src/config').default;
const fs = require('fs');
const async = require('async');

var root;
getRootPath(process.cwd(), (res) => {
  root = res
});

module.exports.uploading = (req, res) => {

  const storage = multer.diskStorage({
    destination: path.join(root, 'Interfata/'),
    filename: function (req, file, cb) {
      cb(null, path.extname(file.originalname) === '.txt' ? 'text.txt' : 'mySound' + path.extname(file.originalname))
    }
  });

  function checkFileType (file, cb) {

    const filetypes = /mp3|wav|txt/;
    const extname = filetypes.test(path.extname(file.originalname).toLowerCase());
    let mimetype;
    (file.mimetype === 'audio/mpeg' || file.mimetype === 'audio/wav' || file.mimetype === 'audio/mp3' || file.mimetype === 'text/plain') ? mimetype = true : mimetype = false
    if (mimetype && extname) {
      return cb(null, true)
    } else {
      cb('Eroare: Doar audio!')
    }
  }

  const upload = multer({
    storage: storage,
    // fileFilter: function (req, file, cb) {
    //   checkFileType(file, cb)
    // }
  }).array('mySound', 2);

  upload(req, res, (err) => {
    if (err) {
      const error = {error: 'Fisierul nu s-a putut incarca...Extensie gresita. Uploadati din nou!'};
      res.send(error)
    }
    else {
      // fisierul salvat o sa fie mySound.extensie (vezi filename din multer.diskStorage)
      // dupa care trebuie trimis modulului de prelucrare date
      // si sa fie convertit in test.raw, and that's all, ar trebui sa mearga dupa
      // console.log(req);
      console.log('[SERVER] Am primit in urma upload-ului fisierul:');
      console.log(req.files);
      console.error(req.body);
      get_sound_alignment_result(res, req)
    }
  })
}

function get_sound_alignment_result (res, req) {
  // CALL PYTHON MODULE TO GET THE RESULT
  async.waterfall([
    (cb) => {
      // SEND AUDIO FILE TO `PRELUCRAREA DATELOR` MODULE
      console.log('[SERVER] Trimitem ca parametru fisierul primit catre modulul:' + path.join(root, 'Prelucrarea datelor/stripAudio.py'))
      const pythonProcess = spawn('py',
        [path.join(path.join(root, 'Prelucrarea datelor/stripAudio.py')),
          path.join(root, 'Interfata/mySound.wav'),
            path.join(root, 'Interfata/test.raw')
        ]);
      let response = '';
      pythonProcess.stdout.on('data', (data) => {
        response += data
      });
      pythonProcess.stdout.on('end', () => {
        console.log('StripAudio finishied. Response is: ', response)
        cb()
      })
    },
    (cb) => {
      // SEND RAW FILE + TEXT FILE TO text_alignment module
      console.log('[SERVER] Trimitem ca parametru fisierul primit catre modulul:' + path.join(root, 'text_alignment/text_alignment.py'))
      const pythonProcess = spawn('py',
        [path.join(path.join(root, 'text_alignment/text_alignment.py')),
          '-rec',  path.join(root, 'Interfata/test.raw'), //argv [1] si argv[2]
          '-orig', path.join(root, 'Interfata/text.txt'), //argv [3] si argv[4]
          '-out', path.join(path.join(path.join(root, 'Interfata/vers.json'))), //argv [5] si argv[6]
          '-m', 'ro'
        ]);
      let response = '';
      pythonProcess.stdout.on('data', (data) => {
        response += data
      });
      pythonProcess.stdout.on('end', () => {
        console.log('[SERVER] Am primit de la modulul de python urmatorul raspuns:');
          cb(null, response)
        // fs.readFile(path.join(path.join(process.cwd(), '/uploads/response.json')), function (err, data) {
        //   if (err) {
        //     console.log(err)
        //     return cb(err)
        //   }
        //   fs.writeFile(path.join(root, 'Interfata/vers.json'), data, function (err) {
        //     console.log(data)
        //     if (err) {
        //       return console.log(err)
        //     }
        //     data = JSON.parse(data)
        //     cb(null, data)
        //   })
        //
        // })
      })
    }
  ], (err, data) => {
    if (err) {
      return res.send('eroare sefu')
    }
    res.json({syncData: data})
  })

}
