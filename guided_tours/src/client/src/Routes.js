/*
  This file is based on this tutorial:
  https://serverless-stack.com/chapters/handle-routes-with-react-router.html
*/
import React from "react";
import { Route, Switch } from "react-router-dom";
import Home from "./components/Home";
import Login from "./components/Login";
import Registration from "./components/Registration";
import Account from "./components/Account";
import UploadTour from "./components/ManageUploadTour";
import UserTours from "./components/ManageUserTours";
import Tour from "./components/Tour";
import NearbyTours from "./components/NearbyTours";
import NotFound from "./components/NotFound";
import AppliedRoute from "./components/AppliedRoute";
import AuthenticatedRoute from "./components/AuthenticatedRoute";
import UnauthenticatedRoute from "./components/UnauthenticatedRoute";


export default ({ childProps }) =>
  <Switch>
    <AppliedRoute path="/" exact component={Home} props={childProps} />
    <UnauthenticatedRoute path="/login" exact component={Login} props={childProps} />
    <UnauthenticatedRoute path="/registration" exact component={Registration} props={childProps} />
    <AppliedRoute path="/tours/nearby" exact component={NearbyTours} props={childProps} />
    <AppliedRoute path="/tours/:tour_id" exact component={Tour} props={childProps} />
    <AuthenticatedRoute path="/user/:username/tours" exact component={UserTours} props={childProps} />
    <AuthenticatedRoute path="/user/:username/tours/upload" exact component={UploadTour} props={childProps} />
    <AuthenticatedRoute path="/user/:username/tours/upload/:tour_id" exact component={UploadTour} props={childProps} />
    <AuthenticatedRoute path="/user/:username/account" exact component={Account} props={childProps} />
    <Route component={NotFound} />
  </Switch>;
