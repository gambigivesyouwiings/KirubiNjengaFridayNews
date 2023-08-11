async function initMap() {
  // Request needed libraries.
  const { Map, InfoWindow } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement, PinElement } = await google.maps.importLibrary(
    "marker"
  );
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 3,
    center: { lat:-1.3307347749614684, lng:36.924976050146164 },
    mapId: "DEMO_MAP_ID",
  });
  const infoWindow = new google.maps.InfoWindow({
    content: "",
    disableAutoPan: true,
  });
  // Create an array of alphabetical characters used to label the markers.
  const labels = ["Naishola", "JKIA", "Tribe"];
  // Add some markers to the map.
  const markers = locations.map((position, i) => {
    const label = labels[i % labels.length];
    const pinGlyph = new google.maps.marker.PinElement({
      glyph: label,
      glyphColor: "white",
    });
    const marker = new google.maps.marker.AdvancedMarkerElement({
      position,
      content: pinGlyph.element,
    });

    // markers can only be keyboard focusable when they have click listeners
    // open info window when marker is clicked
    marker.addListener("click", () => {
      infoWindow.setContent(position.lat + ", " + position.lng);
      infoWindow.open(map, marker);
    });
    return marker;
  });

   const markerCluster = new markerClusterer.MarkerClusterer({ map, markers });

  // Add a marker clusterer to manage the markers.
  new MarkerClusterer({ markers, map });
}

const locations = [
  { lat:-1.1389411789832375, lng:36.66066449468048 },
  { lat:-1.3307347749614684, lng:36.924976050146164 },
  { lat:-1.2266714723684797, lng:36.80558994255637 }
  ];

//// Initialize and add the map
//let map;
//
//async function initMap() {
//  // The location of Uluru
//  const position = { lat:-1.1389411789832375, lng:36.66066449468048 };
//  // Request needed libraries.///
//  //@ts-ignore
//  const { Map } = await google.maps.importLibrary("maps");
//  const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");
//
//  // The map, centered at Limuru
//  map = new Map(document.getElementById("map"), {
//    zoom: 4,
//    center: position,
//    mapId: "DEMO_MAP_ID",
//  });
//
//  // The marker, positioned at Limuru
//  const marker = new AdvancedMarkerElement({
//    map: map,
//    position: position,
//    title: "Limuru",
//  });
//
//  // The marker, positioned at Jomo Kenyatta International Airport
//  const marker2 = new AdvancedMarkerElement({
//    map: map,
//    position: { lat:-1.3307347749614684, lng:36.924976050146164 },
//    title: "JKIA",
//    label: "airport"
//  });
//}
//
initMap();
