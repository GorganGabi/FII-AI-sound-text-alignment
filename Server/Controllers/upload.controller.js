const multer = require('multer')
const path = require('path')
const spawn = require("child_process").spawn;
const config = require("../src/config").default;


module.exports.uploading = (req, res) => {

    const storage = multer.diskStorage({
        destination: './uploads',
        filename: function (req, file, cb) {
            cb(null, 'mySound'+ path.extname(file.originalname))
        }
    });

    function checkFileType(file, cb) {

        const filetypes = /mp3|wav/;
        const extname = filetypes.test(path.extname(file.originalname).toLowerCase());
        let mimetype;
        (file.mimetype === 'audio/mpeg' || file.mimetype === 'audio/wav'|| file.mimetype === 'audio/mp3') ? mimetype = true : mimetype = false;
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
            console.log(req.file)
            const result = {upload: req.file};
            get_sound_alignment_result(result, res)
        }
    })
};

function get_sound_alignment_result(input, res) {
    // CALL PYTHON MODULE TO GET THE RESULT
    input = JSON.stringify(input);
    console.log('[SERVER] Trimitem ca parametru fisierul primit catre modulul:' + path.join(process.cwd(), 'dummy.py'));
    const pythonProcess = spawn("py", [path.join(process.cwd(), 'dummy.py'), input]);
    let response = "";

    pythonProcess.stdout.on("data", (data) => {
        response += data
    });
    pythonProcess.stdout.on("error", (err) => {
        res.json(err)
    });

    pythonProcess.stdout.on("end", () => {
        console.log('[SERVER] Am primit de la modulul de python urmatorul raspuns:');
        if(response) {
            response = JSON.parse(response);
        }
        console.log(response);
        res.json(response)
    });
}
