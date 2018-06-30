function requestUserLocation(callback){
    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(function(position) {
            return callback(null, position.coords);
        });
    } else {
        return callback("Geolocation is not supported.");
    }
}

function reverseGeocode(coords, callback) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4) {
            if (xhttp.status == 200) {
                var obj = JSON.parse(xhttp.responseText);
                return callback(null, obj);
            } else {
                return callback("Could not reverse geocode");
            }
        } else {
            // still processing
        }
    };
    var url = "https://nominatim.openstreetmap.org/reverse.php?format=json&lat=" + coords.latitude + "&lon=" + coords.longitude;
    xhttp.open("GET", url, true);
    xhttp.send();
}

function buildDescription(geocodeResponse) {
    var address = geocodeResponse['address'];

    var description = address['state'];
    if (address['city']) {
        description = address['city'] + ", " + description;
    }
    if (address['neighbourhood']) {
        description = address['neighbourhood'] + ", " + description;
    }

    return description;
}

function saveUserLocation(location, description, callback) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4) {
            if (xhttp.status == 200) {
                var obj = JSON.parse(xhttp.responseText);
                return callback(null, obj);
            } else {
                return callback("Could not save location to database");
            }
        } else {
            // still processing
        }
    };

    var data = {
        "lon" : location.longitude,
        "lat" : location.latitude,
        "description" : description
    };

    xhttp.open("POST", '/locations/me', true);
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhttp.send(JSON.stringify(data));
}

function updateUserLocation(e) {
    requestUserLocation(function(err, location) {
        if (err) {
            console.log("No user location: " + err);
            return;
        }

        reverseGeocode(location, function(err, geocode) {
            if (err) {
                console.log(err);
                return;
            }

            var description = buildDescription(geocode);
            saveUserLocation(location, description, function(err, response) {
                if (err) {
                    console.log(err);
                    return;
                }

                console.log("Successfully saved user location.");

                locationsLayer.loadURL(locationsURL());
            });
        });
    });
}

function locationsURL(){
    var locations_url = '/locations.geojson';
    if(team_id){
        locations_url += '?team_id=' + team_id;
    }
    return locations_url;
}

L.mapbox.accessToken = 'pk.eyJ1IjoidG9sYXIiLCJhIjoiY2luMXVndGw1MGI0cHdibHU1OXFtMGxkNyJ9.89FDP3XpLOwyWxmU-OA1Kw';
//currently centering to the middle of the US
var map = L.mapbox.map("map")
    .setView([39.962, -94.806], 4)
    .addLayer(L.mapbox.tileLayer('mapbox.streets'))
    .whenReady(updateUserLocation);

var clusterGroup = new L.MarkerClusterGroup();

var locationsLayer = L.mapbox.featureLayer(locationsURL())
    .on('ready', function(e) {
        // Apply some local styling
        e.target.eachLayer(function(marker) {
            marker.setPopupContent('<div><img width="75" src="' + marker.feature.properties.avatar + '"/><br/><strong>'+marker.feature.properties.name+'</strong></div>');
            marker.setIcon(L.icon({
                "iconUrl": marker.feature.properties.avatar,
                "iconSize": [30, 30],
                "iconAnchor": [15, 30],
                "popupAnchor": [0, -30],
                "className": "dot"
            }));
        });

        // Hook up the cluster group
        clusterGroup.clearLayers();
        e.target.eachLayer(function(marker) {
            clusterGroup.addLayer(marker);
        });
        map.addLayer(clusterGroup);

        // Put the names in the browser
        var names = [];
        locationsLayer.eachLayer(function(marker) {
            names.push(marker.feature.properties.name);
        });
        names.sort();
        document.getElementById('people').innerHTML = names.join('<br/>');
    });
