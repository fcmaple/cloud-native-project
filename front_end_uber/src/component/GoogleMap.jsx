import React, { useState, useEffect } from 'react'
import GoogleMapReact from 'google-map-react';
import {IoIosPin} from "react-icons/io"

import { async } from 'regenerator-runtime';

const AnyReactComponent = ({ text }) => 
<div 
  style={{
    minWidth:"150px",
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
    fontWeight: "bolder"
  }}><IoIosPin className='flag' color="#FF5733" />{ text }</div>;

const handleApiLoaded = (map, maps) => {
    // use map and maps objects
    console.log('載入完成!') // 印出「載入完成」
};

function createMapOptions(maps) {
  // next props are exposed at maps
  // "Animation", "ControlPosition", "MapTypeControlStyle", "MapTypeId",
  // "NavigationControlStyle", "ScaleControlStyle", "StrokePosition", "SymbolPath", "ZoomControlStyle",
  // "DirectionsStatus", "DirectionsTravelMode", "DirectionsUnitSystem", "DistanceMatrixStatus",
  // "DistanceMatrixElementStatus", "ElevationStatus", "GeocoderLocationType", "GeocoderStatus", "KmlLayerStatus",
  // "MaxZoomStatus", "StreetViewStatus", "TransitMode", "TransitRoutePreference", "TravelMode", "UnitSystem"
  // console.log(maps)
  return {
    zoomControlOptions: {
      position: maps.ControlPosition.RIGHT_CENTER,
      style: maps.ZoomControlStyle.SMALL
    },
    mapTypeControlOptions: {
      position: maps.ControlPosition.TOP_RIGHT
    },
    mapTypeControl: true
  };
}

// Map
const GoogleMap = (props) => {
  const {checkPointList, gkey, center, zoom} = props
  // const [currentZoom, setZoom] = useState(zoom)
  // const [currentCenter, setCenter] = useState(center)

  // const hangehandler = (e) => {
  //   // console.log(e)
  //   // setCenter(center)
  //   if(currentCenter !== center){
  //     setZoom(e.zoom)
  //     setCenter(e.center)
  //     console.log(currentCenter, currentZoom)
  //   }
  // }

  return (
    // Important! Always set the container height explicitly
    <div style={{ height: '90vh', width: '100%' }}>
      <GoogleMapReact
        bootstrapURLKeys={{ "key": gkey }}
        center={center}
        zoom={zoom}
        options={createMapOptions}
        // onChange={(e) => hangehandler(e)}
        yesIWantToUseGoogleMapApiInternals
      >
        {
          checkPointList && checkPointList.map((cp)=>{
            return(
            <AnyReactComponent
              key = {cp.loaction}
              lat = {cp.lat}
              lng = {cp.lng}
              text = {cp.location}
            />)
          })
        }
      </GoogleMapReact>
    </div>
  );
}



export default GoogleMap;