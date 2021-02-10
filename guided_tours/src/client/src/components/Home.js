import React, { Component } from "react";
import SearchBar from "./SearchBar";
import "../styles/Home.css";


export default class Home extends Component {

  constructor() {
    super();

    this.state = {
      tours: [],
      isLoading: true
    };

  }


  componentDidMount = async () => {
    let tours = [];

    if (Array.isArray(this.props.tours) && this.props.tours.length > 0) {
      tours = this.props.tours;
    } else {
      tours = await this.props.fetchTours();
    }
    this.setState({
      tours: tours,
      isLoading: false
    });
  }

  render = () => {

    return (
      <div>
      {
        this.state.isLoading
          ? <i className="fa fa-spinner fa-spin"></i>
          :
        <div className="Home" id="homePage">
          <div id="searchBarContainer">
            <SearchBar
              tours={this.state.tours}
            />
          </div>
          <br></br>
          <div className="lander">
            <h1>Guided Tours</h1>
            <p>The app that takes you on a tour</p>
          </div>
        </div>
      }
      </div>
    );
  }
}