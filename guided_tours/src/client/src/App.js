import React, { Component, Fragment } from "react";
import { Link } from "react-router-dom";
import { Nav, Navbar, NavItem } from "react-bootstrap";
import { LinkContainer } from "react-router-bootstrap";
import Routes from "./Routes";
import "./styles/App.css";


class App extends Component {
  /*
    This authentication code is based on this tutorial:
    https://serverless-stack.com/chapters/add-the-session-to-the-state.html
  */
  constructor(props) {
    super(props);

    this.state = {
      username: null,
      isAuthenticated: false,
      latitude: "",
      longitude: "",
      tours: [],
      socket: "",
      isLoading: true
    };
  }

  componentDidMount = async () => {
    let load_app = false;

    try {
      load_app = await this.getLocation();
    } catch(err) {
      console.log(err.message);
    }

    if (!load_app) {
      // I haven't been able to connect to connect to DIT's WiFi on the
      // Linux partition of my laptop which is where I do any development
      // work.  For the purposes of the demostration I am hard coding
      // the geolocation to be the Ha'penny Bridge
      // https://www.htmlgoodies.com/html5/navigating-html5-geolocation.html
      let latitude = 53.3463231;
      let longitude = -6.263098;

      this.setState({
        latitude: latitude,
        longitude: longitude
      });
    }

    let tours = await this.fetchTours();

    this.setState({
      tours: tours
    });

    let socket = new WebSocket(process.env.REACT_APP_WEBSOCKET_SERVER);

    socket.onopen = async () => this.handleWsOpen(socket);

    socket.onmessage = ({data}) => this.handleWsData(data);

    this.setState({
      socket: socket,
      isLoading: false
    });
  }

  fetchTours = async () => {
    let params =`latitude=${this.state.latitude}&longitude=${this.state.longitude}`;
    let url = `api/v1/tours/?${params}`;
    let response = await fetch(url);

    if (response.status === 200) {
      let data = await response.json();
      return data.tours;
    } else {
      return [];
    }
  }

  // https://stackoverflow.com/questions/51843227/how-to-use-async-wait-with-html5-geolocation-api
  getLocation = async () => {
    const position = await this.getCoordinates();

    let latitude = position.coords.latitude;
    let longitude = position.coords.longitude;

    this.setState({
        latitude: latitude,
        longitude: longitude
    });

    return true;
  }

  getCoordinates = () => {
    return new Promise(function(resolve, reject) {
      navigator.geolocation.getCurrentPosition(resolve, reject);
    });
  }

  userHasAuthenticated = authenticated => {
    this.setState({ isAuthenticated: authenticated });
  }

  setUsername = username_ => {
    this.setState({
      username: username_
    });
  }

  handleLogout = async event => {
    try {
      await fetch("/api/v1/logout", {
        method: "POST",
        body: JSON.stringify({
          "username": this.state.username
        })
      });

    } catch(err) {
      console(err);
    } finally {
      this.state.username = null;
      this.userHasAuthenticated(false);
    }
  }

  addTour = tour => {
    let tours = this.state.tours;

    this.setState({ tours: tours.push(tour) });
  }

  updateTour = tour => {
    this.removeTour(tour.id);
    this.addTour(tour);
  }

  removeTour = tour_id => {
    let tours = this.state.tours;

    if (Array.isArray(tours) && tours.length > 0) {
      let filtered_tours = tours.filter(_tour => _tour.tour_id === tour_id);

      this.setState({ tours: filtered_tours });
    }
  }

  handleWsOpen = async socket => {

    let url = "api/v1/tokens";

    let response = await fetch(url);

    if (response.status === 201) {
      let data = await response.json();

      let msg = {
        "action": "register",
        "token": data.token,
        "latitude": this.state.latitude,
        "longitude": this.state.longitude
      }

      socket.send(JSON.stringify(msg));
    } else {
      socket.close();
    }

  }

  handleWsData = data => {
    // for debugging purposes
    console.log(`Received Web Socket Data: ${data}`);

    let result = JSON.parse(data);

    if (result.action === "tour_added") {
      this.addTour(result.tour);
    } else if (result.action === "tour_updated") {
      this.updateTour(result.tour);
    } else if (result.action === "tour_deleted") {
      this.removeTour(result.tour_id);
    } else {
      console.log("Unknown web socket action: " + result.action)
    }
  }

  /*
    This render is based on this tutorial:
    https://serverless-stack.com/chapters/adding-links-in-the-navbar.html
  */

  render = () => {
    const childProps = {
      username: this.state.username,
      setUsername: this.setUsername,
      isAuthenticated: this.state.isAuthenticated,
      userHasAuthenticated: this.userHasAuthenticated,
      latitude: this.state.latitude,
      longitude: this.state.longitude,
      tours: this.state.tours,
      fetchTours: this.fetchTours
    };

    return (
      <div>
      {
          this.state.isLoading
            ? <i className="fa fa-spinner fa-spin"></i>
            :
          <div className="App container">
            <Navbar fluid collapseOnSelect>
              <Navbar.Header>
                <Navbar.Brand>
                  <Link to="/">Guided Tours</Link>
                </Navbar.Brand>
                <Navbar.Toggle />
              </Navbar.Header>
              <Navbar.Collapse>
                <Nav pullRight>
                  <Fragment>
                    <LinkContainer to="/tours/nearby">
                      <NavItem>Nearby Tours</NavItem>
                    </LinkContainer>
                  </Fragment>
                {this.state.isAuthenticated
                  ? <Fragment>
                      <LinkContainer to={"/user/" + this.state.username + "/tours/upload"}>
                        <NavItem>Upload Tours</NavItem>
                      </LinkContainer>
                      <LinkContainer to={"/user/" + this.state.username + "/tours"}>
                        <NavItem>Manage Tours</NavItem>
                      </LinkContainer>
                      <LinkContainer to={"/user/" + this.state.username + "/account"}>
                        <NavItem>Manage Account</NavItem>
                      </LinkContainer>
                      <NavItem onClick={this.handleLogout}>Logout</NavItem>
                    </Fragment>
                  : <Fragment>
                      <LinkContainer to="/registration">
                        <NavItem>Registration</NavItem>
                      </LinkContainer>
                      <LinkContainer to="/login">
                        <NavItem>Login</NavItem>
                      </LinkContainer>
                    </Fragment>
                }
                </Nav>
              </Navbar.Collapse>
            </Navbar>
            <Routes childProps={childProps} />
          </div>
        }
      </div>

    );
  }
}


export default App;
