function clean(object){
    var ints = []
    object.data.forEach(function(measure){
        ints.push(parseInt(measure))
    })
 
    object.data = ints;
    console.log(object.data)
    return object
}


function cleaner(objects){
    var cleaned_objects = []
    objects.forEach(function(object){
        clean_object = clean(object)
        console.log(clean_object)   
        cleaned_objects.push(clean_object)
    })
   return cleaned_objects 
}

