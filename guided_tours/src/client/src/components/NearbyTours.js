import React, { Component } from "react";
import GoogleApiWrapperMultiLocations from "./GoogleMapsWrapperMultiLocations";


export default class NearbyTours extends Component {

  constructor() {
    super();

    this.state = {
      tours: [],
      latitude: "",
      longitude: "",
      isLoading: true
    };

    this.handleRedirectToTour = this.handleRedirectToTour.bind(this);

  }

  componentDidMount = async () => {
    let tours = [];

    if (Array.isArray(this.props.tours) && this.props.tours.length > 0) {
      tours = this.props.tours;
    }

    this.setState({
      tours: tours,
      latitude: this.props.latitude,
      longitude: this.props.longitude,
      isLoading: false
    });
  }

  handleRedirectToTour = tour_id => {
    //window.location.replace(`http://localhost:3000/tours/${tour_id}`);
    if (tour_id === null) {
      alert("Error lookuping up tour");
      return null;
    }
    this.props.history.push({
      pathname: `/tours/${tour_id}`
   })

  }

  render = () => {

    return (
      <div>
      {
        this.state.isLoading
          ? <i className="fa fa-spinner fa-spin"></i>
          :
        <div>
          <h3>Tours Near You</h3>
          <br></br>
          <div className="nearbyToursMap">
            <GoogleApiWrapperMultiLocations
              tours={this.state.tours}
              latitude={this.state.latitude}
              longitude={this.state.longitude}
              handleRedirectToTour={this.handleRedirectToTour}
            />
          </div>
        </div>
      }
      </div>
    );
  }
}
