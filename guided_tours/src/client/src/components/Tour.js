import React, { Component } from "react";
import GoogleApiWrapper from "./GoogleMapsWrapperSingleLocation";
import { Carousel } from "react-bootstrap";


export default class Tour extends Component {
    constructor(props) {
    super(props);

    this.state = {
      title: "",
      description: "",
      content: [],
      latitude: "",
      longitude: "",
      isLoading: true
    };
  }

  componentDidMount = () => {
    let tour_id = this.props.location.pathname.split("/").slice(-1)[0];
    let url = `/api/v1/tours/${tour_id}`;
    fetch(url)
      .then(res => res.json())
      .then(data => {
        this.setState({
            title: data.title,
            description: data.description,
            content: data.content,
            latitude: data.latitude,
            longitude: data.longitude,
            isLoading: false
          });
      })
  }

  getLocationOfTour = (lat, long) => {
    console.log("Warning cannot set location of tour for this view.");
  }

  getAudioLocation = () => {
    let file_location = "";
    this.state.content.forEach(function(_file) {
      if (_file.extension === ".mp3") {
        file_location = `../content/audio/${_file.server_filename}`;
      }
    });

    // TODO: handle file location not found
    return file_location;
  }

  getImageCarousel = () => {
    return this.state.content.map(function(_file) {
      if (_file.extension === ".mp3") {
        return "";
      }

      let file_location = `../content/images/${_file.server_filename}`;

      return (
        <Carousel.Item key={file_location}>
          <img
            className="d-block w-100"
            src={file_location}
            alt={_file.key}
          />
        </Carousel.Item>
      )
    });
  }

  render = () => {

    return(
      <div>
        {
          this.state.isLoading
            ? <i className="fa fa-spinner fa-spin"></i>
            : <div>
                <h3>
                  {this.state.title}
                </h3>

                <div>
                  {this.state.description}
                </div>

                <div style={{ height: "100vh", width: "80%" }}>
                  <GoogleApiWrapper
                    myLongitude={this.state.longitude}
                    myLatitude={this.state.latitude}
                    getLocationOfTour={this.getLocationOfTour}
                  />
                </div>

                <audio controls>
                  <source src={this.getAudioLocation()} type="audio/mpeg"/>
                  Your browser does not support the audio element.
                </audio>

                <Carousel>
                  {this.getImageCarousel()}
                </Carousel>

            </div>
        }
      </div>
    )
  
  }
}
