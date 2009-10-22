function setMapCookie(map) {
	document.cookie = 'googlemaplng=' + map.getCenter().lng();
	document.cookie = 'googlemaplat=' + map.getCenter().lat();
	var zoom = map.getZoom();
	document.cookie = 'googlemapzoom=' + zoom;
	document.layoutform.scaling_factor.value =+ zoom;
}

function readCookie(name) {
	var nameEQ = name + "=";
	var ca = document.cookie.split(';');
	for(var i=0;i < ca.length;i++) {
		var c = ca[i];
		while (c.charAt(0)==' ') c = c.substring(1,c.length);
		if (c.indexOf(nameEQ) == 0) {
			c=c.substring(nameEQ.length,c.length);
			while (c.substring(c.length-1, c.length) == ' ')
				c = c.substring(0,c.length-1);
			return c;
		}
	}
	return null;
}

function createMarker(hostname, comment, lat, long, state) {
	var point = new GLatLng(lat,long);
	var marker;
	if (state == "Up") {
		var baseIcon = new GIcon();
		baseIcon.shadow = gstatusmap.images_url + "shadow50.png";
		baseIcon.iconSize = new GSize(20, 34);
		baseIcon.shadowSize = new GSize(37, 34);
		baseIcon.iconAnchor = new GPoint(9, 34);
		baseIcon.infoWindowAnchor = new GPoint(9, 2);
		baseIcon.infoShadowAnchor = new GPoint(18, 25);
		var okicon = new GIcon(baseIcon);
		okicon.image = gstatusmap.images_url + "marker.png";
		marker = new GMarker(point, okicon);
	} else {
		marker = new GMarker(point);
	}
	GEvent.addListener(marker, "click", function() { 
		marker.openInfoWindowHtml("<b>" + hostname + "</b><br/>" + comment + "<br/>State: " + state + "");
	});
	return marker;
}

function load() {
	if (!GBrowserIsCompatible()) {
		return
	}

	var map = new GMap2(document.getElementById("map"));
	map.addControl(new GLargeMapControl3D());
	map.addControl(new GOverviewMapControl());
	map.addControl(new GMenuMapTypeControl());

	GEvent.addListener(map, "click", function () {
		setMapCookie(map);
	});
	GEvent.addListener(map, "move", function () {
		setMapCookie(map);
	});
	GEvent.addListener(map, "zoom", function () {
		setMapCookie(map);
	});
	var googlemaplat = readCookie('googlemaplat');
	var googlemaplng = readCookie('googlemaplng');
	var centerPoint;
	if (googlemaplng != null && googlemaplat != null) {
		centerPoint = new GLatLng(googlemaplat, googlemaplng);
	} else {
		centerPoint = new GLatLng(gstatusmap.lat, gstatusmap.lng);
	}

	var scale = readCookie('googlemapzoom') || gstatusmap.scale || 100;
	map.setCenter(centerPoint, parseInt(scale));
	document.layoutform.scaling_factor.value = scale;

	// insert markers
	for (var i in gstatusmap.markers) {
		var marker = gstatusmap.markers[i];
		if (marker) {
			map.addOverlay(createMarker(marker[0], marker[1], marker[2], marker[3], marker[4]));
		}
	}
}
