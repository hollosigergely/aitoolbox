const fs = require('fs')

function generate_source(target_dir, ipynb_file_path)
{
    console.info('Opening file ' + ipynb_file_path)
    
    ipynb_file = fs.readFileSync(ipynb_file_path, 'utf8')
    ipynb_json = JSON.parse(ipynb_file)
    cells_array = ipynb_json.cells

    setup_idx = cells_array.findIndex((element) => {
        return element.cell_type == 'markdown' && element.source.length > 0  && element.source[0] == "# Setup"
    })
    service_idx = cells_array.findIndex((element) => {
        return element.cell_type == 'markdown' && element.source.length > 0  && element.source[0] == "# Service"
    })
    console.info('Setup index: ' + setup_idx)
    console.info('Service index: ' + service_idx)

    if(service_idx == -1 || setup_idx == -1)
        throw RangeError('No service or setup markdown entry can be found!')

    if(service_idx < setup_idx)
    {
        throw RangeError('service_idx < setup_idx')
    }

    setup_file = fs.createWriteStream(target_dir + '/setup.py', {flags: 'w'})
    lines = cells_array.slice(setup_idx+1, service_idx).filter((cell) => cell.cell_type == 'code').map((cell) => cell.source)
    lines.forEach(element => {
       element.forEach(line => setup_file.write(line))
       setup_file.write('\n\n') 
    });
    setup_file.end()

    service_file = fs.createWriteStream(target_dir + '/service.py', {flags: 'w'})
    lines = cells_array.slice(service_idx+1, -1).filter((cell) => cell.cell_type == 'code').map((cell) => cell.source)
    lines.forEach(element => {
       element.forEach(line => service_file.write(line))
       service_file.write('\n\n') 
    });
    service_file.end()
}


if(process.argv.length < 4) {
    console.error("Usage: generate_source.js <ipynb file> <target_dir>")
    process.exit(1)
}

ipynb_file_path = process.argv[2]
target_dir = process.argv[3]
generate_source(target_dir, ipynb_file_path)