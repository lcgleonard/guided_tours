/*
  This file is based on this tutorial:
  https://serverless-stack.com/chapters/create-a-signup-page.html
*/
import React, { Component } from "react";
import {
  Button,
  FormGroup,
  FormControl,
  ControlLabel
} from "react-bootstrap";
import "../styles/FormStyles.css";


export default class Registration extends Component {
  constructor(props) {
    super(props);

    this.state = {
      username: "",
      email: "",
      password: "",
      confirmPassword: ""
    };
  }

  validateForm() {
    const minUsernameLength = 3;
    const maxUsernameLength = 16;
    const minEmailLength = 3;
    const minPasswordLength = 3
    const maxPasswordLength = 16;

    // NOTE: that the backend performs stricter validation on the user's password
    // the reason for the less strict password validation on the frontend is the
    // regular expressions which operater on the password string are cpu bound and
    // may block the UI leading to bad user experience.
    return (
      this.state.username.length > minUsernameLength &&
      this.state.username.length <= maxUsernameLength &&
      this.state.email.length > minEmailLength &&
      this.state.password.length > minPasswordLength &&
      this.state.password.length <= maxPasswordLength &&
      this.state.password === this.state.confirmPassword
    );
  }


  handleChange = event => {
    this.setState({
      [event.target.id]: event.target.value
    });
  }

  handleSubmit = async event => {
    event.preventDefault();

    try {
      let res = await fetch("/api/v1/users/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          "email": this.state.email,
          "username": this.state.username,
          "password": this.state.password
        })
      });

      if (res.status === 201) {
        this.props.userHasAuthenticated(true);
        let data = await res.json();
        this.props.setUsername(data.username);
      } else {
        throw new Error("Registration failed");
      }

    } catch(err) {
      alert(err.message);
    }
  }

  renderForm() {
    return (
      <form onSubmit={this.handleSubmit} className="myFormStyle">
        <FormGroup controlId="username" bsSize="large">
          <ControlLabel>Username</ControlLabel>
          <FormControl
            autoFocus
            type="text"
            value={this.state.username}
            onChange={this.handleChange}
          />
        </FormGroup>
        <FormGroup controlId="email" bsSize="large">
          <ControlLabel>Email</ControlLabel>
          <FormControl
            type="email"
            value={this.state.email}
            onChange={this.handleChange}
          />
        </FormGroup>
        <FormGroup controlId="password" bsSize="large">
          <ControlLabel>Password</ControlLabel>
          <FormControl
            value={this.state.password}
            onChange={this.handleChange}
            type="password"
          />
        </FormGroup>
        <FormGroup controlId="confirmPassword" bsSize="large">
          <ControlLabel>Confirm Password</ControlLabel>
          <FormControl
            value={this.state.confirmPassword}
            onChange={this.handleChange}
            type="password"
          />
        </FormGroup>
        <Button
            block
            bsSize="large"
            disabled={!this.validateForm()}
            type="submit"
          >
            Sign Up
          </Button>
   
      </form>
    );
  }

  render() {
    return (
      <div className="Signup">
        {this.renderForm()}
      </div>
    );
  }
}

