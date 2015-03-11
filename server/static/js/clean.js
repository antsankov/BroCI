//this function takes in an object, converts its data attribute to an array of ints and returns it.
function clean(object){
    var ints = [];
    object.data.forEach(function(measure){
        ints.push(parseInt(measure))
    })
    object.data = ints;
    return object;
}

//this takes an array of objects, cleans each of their data attributes and returns them as an array.
function cleaner(objects){
    var cleaned_objects = [];
    objects.forEach(function(object){
        //create a new attribute and delete id. This is so naming works with highcharts
        object.name = object._id;
        delete object._id;
     
        clean_object = clean(object);
        cleaned_objects.push(clean_object);
    })

    return cleaned_objects;
}
