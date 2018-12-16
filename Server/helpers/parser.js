import path from 'path'

export async function getRootPath(root,cb) {
    root = root.split('\\')
    let str = "";
    for (let i = 0; i < root.length; i++) {
        if (i !== root.length - 1) {
            if (i === 0) {
                str += root[i]
            } else {
                str += ('/' + root[i])
            }
        }
    }
    str = path.join(str,'/')
    cb(str)
}