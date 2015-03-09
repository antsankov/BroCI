function clean(input){
    var output = []
    input.forEach(function(measure){
        output.push(parseInt(measure))
    })
    console.log(output)
    return output
}
