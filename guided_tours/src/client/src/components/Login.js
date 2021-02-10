/*
  This file is based on this tutorial:
  https://serverless-stack.com/chapters/create-a-login-page.html
*/
import React, { Component } from "react";
import { Button, FormGroup, FormControl, ControlLabel } from "react-bootstrap";


export default class Login extends Component {
  constructor(props) {
    super(props);

    this.state = {
      usernameOrEmail: "",
      password: ""
    };
  }

  validateForm() {
    return ( 
      this.state.usernameOrEmail.length > 0 &&
      this.state.password.length > 0
    );
  }

  handleChange = event => {
    this.setState({
      [event.target.id]: event.target.value
    });
  }

  isEmailAddress = maybeEmail => {
    // email regular expression take from:
    // https://www.w3resource.com/javascript/form/email-validation.php
    if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(maybeEmail)) {
      return true;
    } else {
      return false;
    }
  }

  handleLoginResponse = async response => {
    if (response.status === 200) {
      this.props.userHasAuthenticated(true);

      let data = await response.json();

      this.props.setUsername(data.username);
    } else if (response.status === 401 || response.status === 403) {
      let data = await response.json();

      alert(data.message);
    } else {
      alert("Login failed");
    }
  }

  handleSubmit = async event => {
    event.preventDefault();

    let requestBody = {
      "password": this.state.password
    };

    if (this.isEmailAddress(this.state.usernameOrEmail)) {
      requestBody["email"] = this.state.usernameOrEmail;
    } else {
      requestBody["username"] = this.state.usernameOrEmail;
    }

    try {
      let response = await fetch("/api/v1/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestBody)
      });

      this.handleLoginResponse(response);
    } catch(err) {
      alert(err.message);
    }
  }

  render() {
    return (
      <div className="Login">
        <form onSubmit={this.handleSubmit}>
          <FormGroup controlId="usernameOrEmail" bsSize="large">
            <ControlLabel>Username or Email</ControlLabel>
            <FormControl
              autoFocus
              type="text"
              value={this.state.usernameOrEmail}
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
          <Button
            block
            bsSize="large"
            disabled={!this.validateForm()}
            type="submit"
          >
            Login
          </Button>
        </form>
      </div>
    );
  }
}

