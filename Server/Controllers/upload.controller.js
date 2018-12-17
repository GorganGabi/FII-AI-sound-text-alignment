import {getRootPath} from "../helpers/parser";

const multer = require('multer')
const path = require('path')
const spawn = require("child_process").spawn;
const config = require("../src/config").default;
const fs = require('fs');


var root;
getRootPath(process.cwd(), (res) => {
    root = res
});

module.exports.uploading = (req, res) => {

    const storage = multer.diskStorage({
        destination: './uploads',
        filename: function (req, file, cb) {
            cb(null, 'mySound' + path.extname(file.originalname))
        }
    });

    function checkFileType(file, cb) {

        const filetypes = /mp3|wav/;
        const extname = filetypes.test(path.extname(file.originalname).toLowerCase());
        let mimetype;
        (file.mimetype === 'audio/mpeg' || file.mimetype === 'audio/wav' || file.mimetype === 'audio/mp3') ? mimetype = true : mimetype = false;
        if (mimetype && extname) {
            return cb(null, true)
        } else {
            cb('Eroare: Doar audio!')
        }
    }

    const upload = multer({
        storage: storage,
        fileFilter: function (req, file, cb) {
            checkFileType(file, cb)
        }
    }).single('mySound');

    upload(req, res, (err) => {
        if (err) {
            const error = {error: 'Fisierul nu s-a putut incarca...Extensie gresita. Uploadati din nou!'};
            get_sound_alignment_result(error, res)
        }
        else {
            console.log('[SERVER] Am primit in urma upload-ului fisierul:');
            console.log(req.file);
            console.log('[SERVER] Am primit in textul:');
            console.log(req.body.text);
            fs.writeFile(path.join(process.cwd(), 'uploads/text.txt'), req.body.text, function (err) {
                if (err) {
                    return console.log(err);
                }
                console.log("[SERVER] Textul a fost salvat cu success in text.txt!");
                get_sound_alignment_result(res)
            });

        }
    })
};

function get_sound_alignment_result(res) {
    // CALL PYTHON MODULE TO GET THE RESULT
    console.log('[SERVER] Trimitem ca parametru fisierul primit catre modulul:' + path.join(root, 'text_alignment/text_alignment.py'));
    const pythonProcess = spawn("py",
        [path.join(path.join(root, 'text_alignment/text_alignment.py')),
            '-rec', path.join(path.join(process.cwd(), '/uploads/test.raw')), //argv [1] si argv[2]
            '-orig', path.join(path.join(process.cwd(), '/uploads/text.txt')), //argv [3] si argv[4]
            '-out', path.join(path.join(process.cwd(), '/uploads/response.txt')) //argv [5] si argv[6]
        ]);
    let response = "";
    pythonProcess.stdout.on("end", () => {
        console.log('[SERVER] Am primit de la modulul de python urmatorul raspuns:');
        console.log(response);
        fs.readFile(path.join(path.join(process.cwd(), '/uploads/response.txt')), function (err, data) {
            if (err) {
                console.log(err)
            }
            res.json({syncData: JSON.parse(data.toString())})
        });
    });
}
