import React, { Component } from "react";
import { Button } from "react-bootstrap";
import "../styles/FormStyles.css";


export default class UserTours extends Component {
    constructor(props) {
    super(props);

    this.state = {
      username: "",
      tours: [],
      isLoading: true
    };
  }

  componentDidMount = async () => {

    let url = `/api/v1/tours/?username=${this.props.username}`;
    let response = await fetch(url);

    if (response.status === 200) {

      let data = await response.json();

      this.setState({
        username: this.props.username,
        tours: data.tours,
        isLoading: false
      });
    }
  }

  handleEdit = event => {
    let tour_id = event.target.value;

    this.props.history.push({
      pathname: `/user/${this.state.username}/tours/upload/${tour_id}`
    });
  }

  // TODO: duplicated from App.js - need to extract into lib
  removeTour = tour_id => {
    let tours = this.state.tours;
    let filtered_tours = tours.filter(_tour => _tour.tour_id === tour_id);

    this.setState({ tours: filtered_tours });
  }

  handleDelete = async event => {
    let tour_id = event.target.value;

    try {
      let response = await fetch(`/api/v1/tours/${tour_id}`, {
        method: "DELETE",
      });

      if (response.status === 200) {
        this.removeTour(tour_id);
        alert(`Tour ${tour_id} deleted`);
      } else {
        alert(`Tour ${tour_id} deletion failed`);
      }

    } catch(err) {
      alert(err.message);
    }
  }

  getTours = () => {
    let handleEditFunction = this.handleEdit;
    let handleDeleteFunction = this.handleDelete;
    return this.state.tours.map(function(tour) {
      return (
        <li key={tour.tour_id}>
          <h3>{tour.title}</h3>
          <div>
            <Button
              block
              bsSize="large"
              type="button"
              id={"edit_tour_" + tour.tour_id}
              value={tour.tour_id}
              onClick={handleEditFunction}
            >
              Edit
          </Button>
          <Button
              block
              bsSize="large"
              type="button"
              id={"delete_tour_" + tour.tour_id}
              value={tour.tour_id}
              onClick={handleDeleteFunction}
            >
              Delete
          </Button>
          </div>
        </li>
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
                {this.getTours()}
            </div>
        }
      </div>
    )
  
  }
}
