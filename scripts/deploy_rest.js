path = require('path')
fs = require('node:fs/promises')


async function deploy_rest(ipynb_file_path,target_dir,tool_dir)
{
    // create dir
    await fs.rm(target_dir, options = { recursive: true, force: true })
    await fs.mkdir(target_dir)

    // copy deploy artifacts of tool
    await fs.cp(path.resolve(tool_dir,'.deploy/'),target_dir, options = { recursive: true })

    // generate source code
    await fs.mkdir(path.resolve(target_dir,'service','src'))
    await fs.copyFile(path.resolve(__dirname,"..","artifacts","main.py"), path.resolve(target_dir,'service','src','main.py'))

    generate_source = require('./generate_source')
    generate_source(path.resolve(target_dir,'service','src'), ipynb_file_path)

    // copy aitoolbox wheel
    await fs.mkdir(path.resolve(target_dir,'service','wheels'))
    await fs.copyFile(path.resolve(__dirname,"..","aitoolbox_aims_lib","dist","aitoolbox_aims-0.0.1-py3-none-any.whl"),
        path.resolve(target_dir,'service','wheels','aitoolbox_aims-0.0.1-py3-none-any.whl'))
}


if (require.main === module) { 
    if(process.argv.length < 4) {
        console.error("Usage: deploy_rest.js <ipynb file> <target_dir> <tool_dir>")
        process.exit(1)
    }

    ipynb_file_path = process.argv[2]
    target_dir = process.argv[3]
    deploy_rest(ipynb_file_path, target_dir, '.')
} else {
    module.exports = deploy_rest
}
