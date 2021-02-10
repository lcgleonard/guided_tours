import React, { Component } from "react";
import {
  Button,
  FormGroup,
  FormControl,
  ControlLabel
} from "react-bootstrap";
import GoogleApiWrapper from "./GoogleMapsWrapperSingleLocation";
import Dropzone from 'react-dropzone'
import "../styles/FormStyles.css";


export default class UploadTour extends Component {

  constructor(props) {
    super(props);

    this.state = {
      title: "",
      description: "",
      latitude: "",
      longitude: "",
      audioFile: "",
      // TODO: refactor this, images should be collection with the rule of
      // only 3 allowed, rather than a state attribute for each image.
      // I wrote this code because it was quick and dirty and I was under
      // pressure for time.
      image0: "",
      image1: "",
      image2: "",
      tour_id: "",
      isLoading: true,
      tours: []
    }
  }

  componentDidMount = async () => {
    let maybe_tour_id = this.props.location.pathname.split("/").slice(-1)[0];

    if (maybe_tour_id !== "upload") {
      try {
        maybe_tour_id = parseInt(maybe_tour_id, 10);
      } catch(err) {
        console.log(err);
      }
    }

    // check if maybe_tour_id is a number
    if (Number.isInteger(maybe_tour_id)) {
      let url = `/api/v1/tours/${maybe_tour_id}`;

      let response = await fetch(url);
      let data = await response.json();


      let audioContent = "";
      let image0 = "";
      let image1 = "";
      let image2 = "";

      data.content.forEach(function(_content) {
        if (_content.key === "audioContent") {
          audioContent = _content;
        } else if (_content.key === "image0") {
          image0 = _content;
        } else if (_content.key === "image1") {
          image1 = _content;
        } else if (_content.key === "image2") {
          image2 = _content;
        }
      });

      this.setState({
        tour_id: maybe_tour_id,
        title: data.title,
        description: data.description,
        audioFile: audioContent,
        image0: image0,
        image1: image1,
        image2: image2,
        latitude: data.latitude,
        longitude: data.longitude,
      });
    }

    this.setState({
      tours: this.props.tours,
      isLoading: false
    });
  }

  handleChange = event => {
    this.setState({
      [event.target.id]: event.target.value
    });
  }

  handleUpsert = async () => {
    let url = "/api/v1/tours/";
    let request_body = {
      "username": this.props.username,
      "title": this.state.title,
      "description": this.state.description,
      "latitude": this.state.latitude,
      "longitude": this.state.longitude
    }

    let http_method = "POST";

    if (this.state.tour_id !== "") {
      url = url + this.state.tour_id;
      http_method = "PUT";
    }

    try {
      let response = await fetch(url, {
        method: http_method,
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(request_body)
      });

      if (response.status === 200 || response.status === 201) {
        let data = await response.json();

        if (this.state.tour_id === "") {
          this.setState({
            tour_id: data.tour_id
          });
        }
      }

      return response;
    } catch(err) {
      console.log(err.message);
      return null;
    }
  }

  handleUpsertOfAudioAndImages = async () => {
    const formData = new FormData();
    formData.append("audioContent", this.state.audioFile);

    let images = [this.state.image0, this.state.image1, this.state.image2];

    images.forEach((image, i) => {
      if (image !== "") {
        formData.append(`image${i}`, image)
      }
    })

    if (this.state.tour_id === "") {
        console.log("Error uploading content");
        return;
    }

    try {
      let response = await fetch(`/api/v1/tours/${this.state.tour_id}`, {
        method: "PATCH",
        headers: {},
        body: formData
      });
      return response;

    } catch(err) {
      console.log(err.message);
    }
  }

  handleSubmit = async event => {
    event.preventDefault();

    let response = await this.handleUpsert();
    if (response.status === 200 || response.status === 201) {
      response = await this.handleUpsertOfAudioAndImages();
    } else {
      await this.handleRollback();
    }

    this.handlePostUploadRedirect(response);

  }

  handlePostUploadRedirect = response => {
    if (response.status === 200 || response.status === 201) {
        alert("Tour content uploaded");
      } else {
        alert("Tour content upload failed");   
      }
      this.props.history.push({
        pathname: "/"
      });
  }

  handleRollback = async tour_id => {
    try {
      let response = await fetch(`/api/v1/tours/${tour_id}`, {
        method: "DELETE",
      });

      if (response.status !== 200) {
        console.log(`Tour ${tour_id} deletion failed`);
      }

    } catch(err) {
      console.log(err.message);
    }
  }

  validateForm = () => {
    if (this.state.latitude === "" || this.state.longitude === "") {
      return false;
    }

    if (this.state.title < 3 || this.state.title > 50) {
      return false;
    }

    if (this.state.description < 5 || this.state.title > 255) {
      return false;
    }

    if (this.state.audioFile === "" || this.state.image0 === "") {
      return false;
    }

    return true;
  }

  getLocationOfTour = (lat, lng) => {
    this.setState({
        latitude: lat,
        longitude: lng
    });
  }

  removeUploadFileClientSide = identifier => {
    // TODO: refactor code in order to clean up this difficult to
    // maintain 'if else if' statement.  I wrote this awkward code
    // because of time pressures
    
    if (identifier === "thisAudioFile") {
      this.setState({
        audioFile: "",
      });
    } else if (identifier === "thisImage0") {
      this.setState({
        image0: "",
      });
    } else if (identifier === "thisImage1") {
      this.setState({
        image1: "",
      });
    } else if (identifier === "thisImage2") {
      this.setState({
        image2: "",
      });
    } else {
      console.log(`Unrecognised identifier ${identifier}`);
    }
  }

  removeUploadFileServerSide = async identifier => {
    let url = "/api/v1/tours/" + this.state.tour_id;

    // TODO: refactor code in order to clean up this difficult to
    // maintain 'if else if' statement.  I wrote this awkward code
    // because of time pressures
    if (identifier === "thisAudioFile") {
      url = url + "/audio";
    } else if (identifier === "thisImage0") {
      url = url + "/images/" + 0;
    } else if (identifier === "thisImage1") {
      url = url + "/images/" + 1;
    } else if (identifier === "thisImage2") {
      url = url + "/images/" + 2;
    } else {
      console.log(`Unrecognised identifier ${identifier}`);
      return false;
    }

    try {
      let response = await fetch(url, {
        method: "DELETE",
        headers: {}
      });

      if (response.status === 200) {
        return true;
      } else {
        return false;
      }
    } catch(err) {
      alert(err.message);
      return false;
    }
  }

  removeUploadedFile = async event => {
    let identifier = event.target.id;

    if (this.state.tour_id === "") {
      this.removeUploadFileClientSide(identifier);
    } else {
      let result = await this.removeUploadFileServerSide(identifier);

      if (result) {
        this.removeUploadFileClientSide(identifier);
      } else {
        alert("Failed to remove file.");
      }
    }
  }

  handleImageDrop = imageFile => {
    if (this.state.image0 === "") {
      this.setState({
        image0: imageFile,
      });
    } else if (this.state.image1 === "") {
      this.setState({
        image1: imageFile,
      });
    } else if  (this.state.image2 === "") {
      this.setState({
        image2: imageFile,
      });
    } else {
      alert("You cannot upload more than 3 images");
    }
  }

  handleAudioDrop = audioFile => {
    if (this.state.audioFile === "") {
      this.setState({
          audioFile: audioFile
      });
    } else {
      alert("You cannot upload more than 1 audio file");
    }
  }

  onDrop = file => {
    const validImgTypes = ["image/png", "image/jpeg"];
    const maxImageSize = 100000;  // in bytes

    const validAudioTypes = ["audio/mpeg"];
    const maxAudioSize = 5000000;  // in bytes

    if (
      validImgTypes.includes(file[0].type) &&
      file[0].size <= maxImageSize
    ) {
      this.handleImageDrop(file[0]);
    } else if (
      validAudioTypes.includes(file[0].type) &&
      file[0].size <= maxAudioSize
    ) {
      this.handleAudioDrop(file[0]);
    } else {
      alert(
        `Error not a valid audio or image file.
        Valid images are either png or jpeg and can be 0.1 Mb or less.
        Valid audio file are mp3/mpeg only and can be 1 Mb or less.`
      );
    }
  }

  renderForm = () => {
    return (
      <form onSubmit={this.handleSubmit}>
       <FormGroup controlId="title" bsSize="large">
          <ControlLabel>Title</ControlLabel>
          <FormControl
            autoFocus
            type="text"
            value={this.state.title || ""}
            onChange={this.handleChange}
          />
        </FormGroup>

        <FormGroup controlId="description" bsSize="large">
          <ControlLabel>Description</ControlLabel>
          <FormControl
            componentClass="textarea"
            rows={5}
            maxLength={255}
            value={this.state.description || ""}
            onChange={this.handleChange}
          />
        </FormGroup>
        <br></br>

        <ControlLabel>Location of Tour</ControlLabel>
        <div style={{ height: "100vh", width: "75%" }}>
          <GoogleApiWrapper
            myLongitude={this.props.longitude || ""}
            myLatitude={this.props.latitude || ""}
            getLocationOfTour={this.getLocationOfTour}
          />
        </div>

        <div>
          <b>Uploaded Audio: </b>
          {this.state.audioFile !== ""
            ? <div>
                <span>
                  {this.state.audioFile.name} <i id="thisAudioFile" onClick={this.removeUploadedFile}>(remove)</i>
                </span>
              </div>
            : <div></div>
          }
        </div>

        <div>
          <b>Uploaded Images: </b>
          {this.state.image0 !== ""
            ? <div>
                <span>
                  {this.state.image0.name} <i id="thisImage0" onClick={this.removeUploadedFile}>(remove)</i>
                </span>
              </div>
            : <div></div>
          }

          {this.state.image1 !== ""
            ? <div>
                <span>
                  {this.state.image1.name} <i id="thisImage1" onClick={this.removeUploadedFile}>(remove)</i>
                </span>
              </div>
            : <div></div>
          }

          {this.state.image2 !== ""
            ? <div>
                <span>
                  {this.state.image2.name} <i id="thisImage2" onClick={this.removeUploadedFile}>(remove)</i>
                </span>
              </div>
            : <div></div>
          }
        </div>

        <Dropzone onDrop={this.onDrop}>
          {({getRootProps, getInputProps}) => (
            <section>
              <div className="dropzone_area"  {...getRootProps()}>
                <p><br></br><b>Add your audio content and pictures here</b></p>
                <input {...getInputProps()} />
              </div>
            </section>
          )}
        </Dropzone>

        <br></br>

        <Button
            block
            bsSize="large"
            disabled={!this.validateForm()}
            type="submit"
          >
            Submit
          </Button>
      </form>
   )
  }

  render() {
    return (
      <div className="UploadContent">
        {this.renderForm()}
      </div>
    );
  }
}
