import React, {Component} from 'react';
import GoogleMapReact from 'google-map-react';
import {IoIosPin} from "react-icons/io"
import {Key} from "../key.js";

const AnyReactComponent = () => <div><IoIosPin className='flag' color="#FF5733" /></div>;

const handleApiLoaded = (map, maps) => {
    // use map and maps objects
    console.log('載入完成!') // 印出「載入完成」
};

// Map
class GoogleMap extends Component {
  static defaultProps = {
    center: {
      lat: 24.787075,
      lng: 120.997217
    },
    zoom: 15
  };

  render() {
    return (
      // Important! Always set the container height explicitly
      <div style={{ height: '90vh', width: '100%' }}>
        <GoogleMapReact
          bootstrapURLKeys={{ key: Key }}
          defaultCenter={this.props.center}
          defaultZoom={this.props.zoom}
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
}

export default GoogleMap;