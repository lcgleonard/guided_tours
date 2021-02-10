/*
  This file is based on this tutorial:
  https://serverless-stack.com/chapters/create-a-signup-page.html
*/
import React, { Component } from "react";
import { Button } from "react-bootstrap";


export default class Account extends Component {

  handleLogout = () => {
    return fetch("/api/v1/logout", {
        method: "POST",
        body: JSON.stringify({
          "username": this.props.username
        })
      }
    )
  }

  closeSession = () => {
    this.props.userHasAuthenticated(false);
  }

  handleSuspend = async event => {
    event.preventDefault();

    try {
      let res = await fetch(`/api/v1/accounts/${this.props.username}`, {
        method: "PATCH"
      });

      if (res.status === 200) {
        return this.handleLogout();
      } else {
        throw new Error("Account suspension failed");
      }
    } catch(err) {
      alert(err.message);
    } finally {
      // TODO: logout not working correctly here - user isn't redirected to
      // logged out view
      this.closeSession();
    }
  }

  handleClose = async event => {
    event.preventDefault();

    try {
      let response = await fetch(`/api/v1/accounts/${this.props.username}`, {
        method: "PUT"
      });

      if (response.status === 200) {
        return this.handleLogout();
      } else {
        throw new Error("Account closure failed");
      }
    } catch(err) {
      alert(err.message);
    } finally {
      // TODO: logout not working correctly here - user isn't redirected to
      // logged out view
      this.closeSession();
    }
  }

  render() {
    return (
      <div className="Account">
        <p>Suspend your account.
          You can unsuspend at anytime by logging back in.
          Any content you have uploaded will not longer be
          accessible to other users while you account is suspended:
        </p>
        <Button
          block
          bsSize="large"
          type="button"
          onClick={this.handleSuspend}
        >
          Suspend
        </Button>

        <p>Close your account.
          Your account will be scheduled to be deleted in 7 days.
          You can cancel the deletion of your account by logging back in within those 7 days:
        </p>
        <Button
          block
          bsSize="large"
          type="button"
          onClick={this.handleClose}
        >
          Close
        </Button>
      </div>
    );
  }
}
