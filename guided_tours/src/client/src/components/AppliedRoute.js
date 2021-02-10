import React from "react";
import { Route } from "react-router-dom";

/*
    This component code is based on this tutorial:
    https://serverless-stack.com/chapters/add-the-session-to-the-state.html
*/

/* 
   returns "a Route where the child that it renders contains the passed in props."

   "Spread syntax (...) allows an iterable such as an array expression or string to be expanded
   in places where zero or more arguments (for function calls) or elements (for array literals)
   are expected, or an object expression to be expanded in places where zero or more key-value
   pairs (for object literals) are expected."
   See: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax
*/
export default ({ component: C, props: cProps, ...rest }) =>
  <Route {...rest} render={props => <C {...props} {...cProps} />} />;
