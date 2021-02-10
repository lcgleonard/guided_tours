import React, { Component } from 'react';
import { GoogleApiWrapper, InfoWindow, Map, Marker } from 'google-maps-react';


export class MapContainer extends Component {

constructor(props) {
    super(props);

    this.state = {
      latitude: "",
      longitude: "",
      tours: [],
      handleRedirectToTour: "",
      isLoading: true
    };
  }

  componentDidMount = async () => {
    this.setState({
      latitude: this.props.latitude,
      longitude: this.props.longitude,
      tours: this.props.tours,
      handleRedirectToTour: this.props.handleRedirectToTour,
      isLoading: false
    });
  }

  onMarkerClick = (props, marker, e) => {
    // redirect to the tour clicked on
    this.state.handleRedirectToTour(props.tour_id);
  }

  fetchMarkers = () => {
  let tours = this.state.tours;
  let onMarkerClickFunction = this.onMarkerClick;

    return tours.map(function(tour) {
      return (
        <Marker key={tour.title}
          tour_id={tour.tour_id}
          title={tour.title}
          name={tour.title}
          position={{lat: tour.latitude, lng: tour.longitude}}
          draggable={false}
          onClick={onMarkerClickFunction}
        />
      )
    });
  }
  
  render = () => {
    return (
      <div>
      {
        this.state.isLoading
          ? <i className="fa fa-spinner fa-spin"></i>
          :

        <Map
          style={{ height: "100vh", width: "75%" }}
          google={this.props.google}
          initialCenter={{
            lat: this.state.latitude,
            lng: this.state.longitude
          }}
          >

          {this.fetchMarkers()}

          <InfoWindow onClose={this.onInfoWindowClose}>
            <div>
              <h1>Tours Near You</h1>
            </div>
          </InfoWindow>
        </Map>
      }
      </div>

    )
  }
}

const GoogleApiWrapperMultiLocations = GoogleApiWrapper({
  apiKey: (process.env.REACT_APP_GOOGLE_MAPS_API_KEY)
})(MapContainer)


export default GoogleApiWrapperMultiLocations;