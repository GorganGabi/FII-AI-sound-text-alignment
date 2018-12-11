const assert = require('assert');
const mockery = require('mockery');
const uploading = require('../../Controllers/upload.controller').uploading;

const req = {headers:{'transfer-encoding': 1}};
const res = {};

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
    it("should return ok", (done) => {
        const mock_config = {
            config: function () {
                console.log('config')
            }
        };
        mockery.registerMock("config", mock_config)
        uploading(req, res);
        done();
    });
});