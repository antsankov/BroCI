//this function takes in an object, converts its data attribute to an array of ints and returns it.
function clean(object){
    var ints = [];
    object.data.forEach(function(measure){
        ints.push(parseInt(measure))
    })
    object.data = ints;
    return object;
}

function cleanSpeed(object){
    var sizes = [];
    object.data.forEach(function(measure){ 
        sizes.push(parseFloat(measure));
    })
    object.data = sizes;
    return object;
}

function cleanRam(object){
    var sizes = [];
    object.data.forEach(function(measure){
        //sizes.push(humanFileSize(parseInt(measure),false))
        sizes.push(parseInt(measure));
    })
    object.data = sizes;
    return object;
}

function cleanSuccess(object){
    var sizes = [];
    object.data.forEach(function(measure){ 
        sizes.push(parseFloat(measure));
    })
    object.data = sizes;
    return object;
}

function timeCleaner(timeArray){
    var cleanedTimes = []
    timeArray.forEach(function(timestamp){
        cleanedTimes.push(new Date(timestamp*1000))
    })
    return cleanedTimes
}


function humanFileSize(bytes, si) {
    var thresh = si ? 1000 : 1024;
    if(bytes < thresh) return bytes + ' B';
    var units = si ? ['kB','MB','GB','TB','PB','EB','ZB','YB'] : ['KiB','MiB','GiB','TiB','PiB','EiB','ZiB','YiB'];
    var u = -1;
    do {
        bytes /= thresh;
        ++u;
    } while(bytes >= thresh);
    return bytes.toFixed(1)+' '+units[u];
};


//this takes an array of objects, cleans each of their data attributes and returns them as an array.
function objectsCleaner(objects,type){
    var cleaned_objects = [];
    objects.forEach(function(object){
        //create a new attribute and delete id. This is so naming works with highcharts
        object.name = object._id;
        delete object._id;

        if (type === "cpu"){ 
            clean_object = clean(object);
        }
        if (type === "ram"){
            clean_object = cleanRam(object);
        }
        if (type === "success"){
            clean_object = cleanSpeed(object);
        } 
        if (type === "speed"){
            clean_object = cleanSpeed(object);
        } 
        else {
            clean_object = clean(object);
        } 
        cleaned_objects.push(clean_object);
    })

    return cleaned_objects;
}
