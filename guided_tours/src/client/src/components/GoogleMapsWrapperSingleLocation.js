import React, { Component } from 'react';
import { GoogleApiWrapper, InfoWindow, Map, Marker } from 'google-maps-react';


export class MapContainer extends Component {

  constructor(props) {
    super(props);

    this.state = {
      showingInfoWindow: false,
      activeMarker: {},
      selectedPlace: {},
      lat: this.props.myLatitude,
      lng: this.props.myLongitude
    }

    if (this.state.lat === "" || this.state.lng === "") {
       // defaulting to Dublin - Ha'penny Bridge
      this.setState(
        {
          lat: 53.3463231,
          lng: -6.263098
        }
      );
    }
  }
  
  onMarkerClick = (props, marker, e) => {
      this.setState({
        selectedPlace: props,
        activeMarker: marker,
        showingInfoWindow: true,
        lat: e.latLng.lat(),
        lng: e.latLng.lng()
    });
  }

  onMapClicked = (props) => {
    if (this.state.showingInfoWindow) {
      this.setState({
          showingInfoWindow: false,
          activeMarker: null
      });
    }
  };


  moveMarker = (props, marker, e) => {

    let _latitude = e.latLng.lat();
    let _longitude = e.latLng.lng();

    this.setState({
      selectedPlace: props,
      activeMarker: marker,
      lat: _latitude,
      lng: _longitude
    });

    this.props.getLocationOfTour(_latitude, _longitude);
  }
  
  render() {

      return (
      <Map 
          style={{ height: "100vh", width: "75%"}}
          google={this.props.google}
          initialCenter={{
            lat: this.state.lat,
            lng: this.state.lng
          }}
          onClick={this.onMapClicked}>

        <Marker
          title="Location"
          id={1}
          draggable={true}
          onDragend={this.moveMarker.bind(this)}
          onClick={this.onMarkerClick}
          >
          <InfoWindow
            visible={this.state.showingInfoWindow}
            >
              <div>
                <p>Click on the map or drag the marker to select location where the incident occurred</p>
              </div>
          </InfoWindow>
        </Marker>
      </Map>
      )
    }
}

export default GoogleApiWrapper({
  apiKey: (process.env.REACT_APP_GOOGLE_MAPS_API_KEY)
})(MapContainer)
