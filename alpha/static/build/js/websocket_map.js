/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */



$(document).ready(function () {
    $('.ui-pnotify').remove();
    var map;
    var lat, long, alt, tm, speed, sat, course, marker, ws, infowindow;
    var myLongitude, myLatitude;
    myLatitude = -11.673898;
    myLongitude = 27.478447;
    myAltitude = '1325.8M';
    initialise = false;
    marker = null;
    function makeInfo() {
        var contentString = '<div id="content">' +
                '<div id="siteNotice">' +
                '</div>' +
                '<h5 id="firstHeading" class="firstHeading">Position information</h5>' +
                '<hr>' +
                '<div id="bodyContent">' +
                '<b>Lat:</b>' + myLatitude +
                '<br><b>Long:</b>' + myLongitude +
                '<br><b>Alt:</b>' + 11.566666 +
                '</div>' +
                '</div>';
        //info
        infowindow = new google.maps.InfoWindow({
            content: contentString
        });
        infowindow.open(map, marker);
    }
    function makeMarker() {
        if (marker === null) {
            marker = new google.maps.Marker({
                position: {lat: myLatitude, lng: myLongitude},
                map: map,
                title: 'The drone location!',
                animation: google.maps.Animation.BOUNCE,
            });
            makeInfo();
        } else {

            marker.setMap(null);
            marker = null;
            infowindow.close();
            makeMarker();
        }


    }
    function initMap() {
        //enabling new cartography and theme

        google.maps.visualRefresh = true;
        var myLatLng = {lat: myLatitude, lng: myLongitude};
        //seting start options of map
        var mapTypeIds = ["roadmap", "satellite", "hybrid", "terrain", "OSM"];
        var mapOptions = {
            center: new google.maps.LatLng(myLatitude, myLongitude),
            zoom: 15,
            mapTypeId: 'OSM',
            mapTypeControlOptions: {
                mapTypeIds: mapTypeIds,
                style: google.maps.MapTypeControlStyle.DROPDOWN_MENU
            },
            scaleControl: true,
            rotateControl: true,
            streetViewControl: true,
        };
        //Getting map DOM element
        var mapElement = document.getElementById('map');
        //creating a map with DOM element
        map = new google.maps.Map(mapElement, mapOptions);
        //open

        map.mapTypes.set("OSM", new google.maps.ImageMapType({
        getTileUrl: function (coord, zoom) {
        // "Wrap" x (logitude) at 180th meridian properly
        // NB: Don't touch coord.x because coord param is by reference, and changing its x property breakes something in Google's lib 
        var tilesPerGlobe = 1 << zoom;
                var x = coord.x % tilesPerGlobe;
                if (x < 0) {
        x = tilesPerGlobe + x;
        }
        // Wrap y (latitude) in a like manner if you want to enable vertical infinite scroll

        return "http://tile.openstreetmap.org/" + zoom + "/" + x + "/" + coord.y + ".png";
        },
                tileSize: new google.maps.Size(256, 256),
                name: "OpenStreetMap",
        maxZoom: 18
    }
    ));
//make marker
    makeMarker();
    //Events

    google.maps.event.addListener(marker, 'click', function () {
    makeMarker();
            console.log({lat: myLatitude, lng: myLongitude});
    });
    }
    ;







//url of websocket server

    ws = new ReconnectingWebSocket("ws://localhost:8001/ws");
    //on open a connexion
    ws.onopen = function (evt) {
        $('#connexion_status').html('Connected');

        new PNotify({
            title: 'Regular Success',
            text: 'Connection etablie avec succes!',
            type: 'success',
            styling: 'bootstrap3'
        });

    };
    //on close a connexion
    ws.onclose = function (evt) {
        $('#connexion_status').html('Disconnected');
        new PNotify({
            title: 'Perte de connection au serveur!',
            text: 'Veuillez actualiser la page SVP.',
            type: 'error',
            styling: 'bootstrap3'
        });
        
    };
    //on receiving a message 
    ws.onmessage = function (evt) {
        var data = evt.data;
        data = JSON.parse(data);

        myLongitude = parseFloat(data.Long);



        myLatitude = parseFloat(data.Lat);


        lat = $('#lat');
        long = $('#long');
        alt = $('#alt');
        tm = $('#time');
        speed = $('#speed');
        sat = $('#sat');
        course = $('#course');
        lat.html(data.Lat);
        long.html(data.Long);
        alt.html(data.Alt);
        tm.html(data.Moment);
        speed.html(data.Speed);
        sat.html(data.Sat);
        course.html(data.Course);

    };

// A la fermeture de la page
    $(window).on('unload', function () {
        ws.onclose = function () {};
        ws.close();
        console.log('close de connection');
    });
    setTimeout(function () {
        initMap();
        map.setCenter({lat: myLatitude, lng: myLongitude});

        console.log({lat: myLatitude, lng: myLongitude});
    }, 4000);
    setInterval(function () {
        map.setCenter({lat: myLatitude, lng: myLongitude});

        var myCity = new google.maps.Circle({
            center: {lat: myLatitude, lng: myLongitude},
            radius: 0.1,
            strokeColor: "#345e82",
            strokeOpacity: 0.8,
            strokeWeight: 2,
            fillColor: "#345e82",
            fillOpacity: 0.4
        });
        myCity.setMap(map);

        //console.log({lat: myLatitude, lng: myLongitude});
    }, 2000);
// Action on modal
    var siteName, captureType, comment, btnCaptureModal,txtComment,cbxCaptureType,txtSiteName;
    btnCaptureModal = $('#btnCaptureModal');
    cbxCaptureType=$('#cbxCaptureType');
    txtSiteName=$('#txtSiteName');
    txtComment=$('#txtComment');
    btnCaptureModal.on('click',function(){
        siteName=txtSiteName.val();
        captureType=cbxCaptureType.val();
        comment=txtComment.val();
        console.log(siteName,captureType,comment);
        if (txtSiteName.val()===''   ) {
            txtSiteName.css('borderColor','red');
        }
        else if(txtComment.val()===''){
            txtComment.css('borderColor','red');
        }
        else{
            message={'siteName':siteName,'captureType':captureType,'comment':comment};
            ws.send('message');
            console.log(message);
        }
    });
});
