// import Joi from 'joi'

require('dotenv').config();

// const envVarsSchema = Joi.object({
//     NODE_ENV: Joi.string()
//         .default('development'),
//     SERVER_PORT: Joi.number()
//         .default(8080),
//     DB_HOST: Joi.string().required()
//         .description('DB host'),
// }).unknown()
//     .required();
//
// const {error, value: envVars} = Joi.validate(process.env, envVarsSchema);

const config = {
    env: process.env.NODE_ENV,
    port: process.env.SERVER_PORT,
    sound_alignment_file_path: process.env.SOUND_ALIGNMENT_FILE_PATH
};

module.exports= {
    config:config
}
