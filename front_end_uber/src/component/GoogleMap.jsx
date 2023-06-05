import React, { useState, useEffect } from 'react'
import GoogleMapReact from 'google-map-react';
import {IoIosPin} from "react-icons/io"

import { async } from 'regenerator-runtime';

const AnyReactComponent = () => <div><IoIosPin className='flag' color="#FF5733" /></div>;

const handleApiLoaded = (map, maps) => {
    // use map and maps objects
    console.log('載入完成!') // 印出「載入完成」
};


// Map
const GoogleMap = (props) => {
  const [center, setCenter] = useState({lat: 24.787075,lng: 120.997217})
  const [zoom, setZoom] = useState(15)

  return (
    // Important! Always set the container height explicitly
    <div style={{ height: '90vh', width: '100%' }}>
      <GoogleMapReact
        bootstrapURLKeys={{ "key": props.gkey }}
        defaultCenter={center}
        defaultZoom={zoom}
        yesIWantToUseGoogleMapApiInternals
        onGoogleApiLoaded={({ map, maps }) => handleApiLoaded(map, maps)}
      >
        <AnyReactComponent
          lat={24.787075}
          lng={120.997217}
        />
      </GoogleMapReact>
    </div>
  );
}

export default GoogleMap;