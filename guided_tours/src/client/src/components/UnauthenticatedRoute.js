import React from "react";
import { Route, Redirect } from "react-router-dom";

/*
  This un authenticated route code is based on this tutorial:
  https://serverless-stack.com/chapters/create-a-route-that-redirects.html
*/

export default ({ component: C, props: cProps, ...rest }) =>
  <Route
    {...rest}
    render={props =>
      !cProps.isAuthenticated
        ? <C {...props} {...cProps} />
        : <Redirect to="/" />}
  />;
