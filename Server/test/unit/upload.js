const assert = require('assert');
const mockery = require('mockery');
const uploading = require('../../Controllers/upload.controller').uploading;

const req = {headers: {'transfer-encoding': 1}};
const res = {
    json: function (err) {
        assert(!err)
    }
};
const mock_config = {
    config: function () {
        console.log('config')
    }
};
const mock_fileFilter = {
    fileFilter: function (req, file, cb) {
        cb('eroare')
    }
};
describe("/api/upload UNIT TESTS", () => {


    beforeEach(() => mockery.enable({
        "warnOnUnregistered": false,
        "warnOnReplace": false,
        "useCleanCache": true
    }));

    afterEach(() => {
        mockery.deregisterAll();
        mockery.disable();
    });

    before(function (done) {
        setTimeout(() => {
            done()
        }, 1000)
    });
    it("should return ok with response undefined", (done) => {
        mockery.registerMock("config", mock_config)
        uploading(req, res);
        done();
    });

    it("should return ok with image object", (done) => {
        mockery.registerMock("config", mock_config);
        req.file = {name: "fisier"};
        uploading(req, res);
        done();
    });

    it("should return error", (done) => {
        mockery.registerMock("config", mock_config);
        mockery.registerMock("fileFilter", mock_fileFilter);
        req.file = {name: "fisier"};
        uploading(req, res);
        done();
    });
});